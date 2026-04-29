from flask import Blueprint, render_template, request, jsonify, current_app
from .chatbot import ChatBot
from .models import Cliente, Cartao, Transacao
from .db import db
import random
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/check_cpf', methods=['POST'])
def check_cpf():
    cpf = (request.json or {}).get('cpf', '').strip()
    if not cpf:
        return jsonify({'error': 'cpf required'}), 400

    cliente = Cliente.query.filter_by(cpf=cpf).first()
    if not cliente:
        return jsonify({'exists': False})

    # Retorna também o cartão vinculado ao CPF
    cartao = Cartao.query.filter_by(cpf_do_cliente=cpf).first()
    return jsonify({
        'exists'    : True,
        'nome'      : cliente.nome,
        'card_numero': cartao.numero    if cartao else None,
        'card_venc' : cartao.vencimento if cartao else None,
    })


@main.route('/ask', methods=['POST'])
def ask():
    data       = request.json or {}
    user_input = data.get('message', '')
    cpf        = data.get('cpf', '').strip()
    chatbot    = current_app.chatbot

    if not chatbot:
        return jsonify({'response': 'Chatbot indisponível no momento.'}), 503

    # Detecta categoria para personalizar resposta de fatura
    categoria = chatbot.get_category(user_input)

    if categoria == 'fatura' and cpf:
        # Soma real das transações do cliente pelo CPF
        total = db.session.query(
            db.func.coalesce(db.func.sum(Transacao.valor_da_transacao), 0.0)
        ).filter(Transacao.cpf_do_cliente == cpf).scalar() or 0.0

        cartao = Cartao.query.filter_by(cpf_do_cliente=cpf).first()
        venc   = cartao.vencimento if cartao else 'N/A'

        response_text = (
            f"O total da sua fatura é R$ {float(total):.2f}, "
            f"com vencimento em {venc}. "
            f"Você pode pagar via PIX, boleto, app ou internet banking."
        )
        return jsonify({'response': response_text})

    # Resposta padrão do chatbot
    result = chatbot.get_response(user_input)
    response_text = result if isinstance(result, str) else result.get('resposta', str(result))
    return jsonify({'response': response_text})


@main.route('/add_transacao', methods=['POST'])
def add_transacao():
    """Salva uma transação para o CPF/cartão do cliente autenticado."""
    data  = request.json or {}
    cpf   = data.get('cpf', '').strip()
    valor = data.get('valor')
    data_str = data.get('data')  # AAAA-MM-DD ou None

    if not cpf or valor is None:
        return jsonify({'error': 'cpf e valor são obrigatórios'}), 400

    # Busca o cartão vinculado ao CPF do cliente
    cartao = Cartao.query.filter_by(cpf_do_cliente=cpf).first()
    if not cartao:
        return jsonify({'error': 'Nenhum cartão encontrado para este CPF'}), 404

    # Data da transação
    try:
        data_dt = datetime.strptime(data_str, '%Y-%m-%d') if data_str else datetime.now()
    except ValueError:
        data_dt = datetime.now()

    trans = Transacao(
        numero_do_cartao    = cartao.numero,
        vencimento          = cartao.vencimento,
        cpf_do_cliente      = cpf,
        valor_da_transacao  = float(valor),
        data_da_transacao   = data_dt,
        id_transacao        = random.randint(100000, 999999),
        limite_cartao       = 0.0,
    )
    db.session.add(trans)
    db.session.commit()

    return jsonify({'message': 'Transação salva com sucesso', 'id': trans.id}), 201


@main.route('/cliente', methods=['POST'])
def create_cliente():
    data = request.json or request.form
    nome = data.get('nome')
    idade = data.get('idade')
    endereco = data.get('endereco')
    cpf = data.get('cpf')

    if not cpf or not nome:
        return jsonify({'error': 'cpf and nome are required'}), 400

    existing = Cliente.query.filter_by(cpf=cpf).first()
    if existing:
        return jsonify({'message': 'Cliente já existe', 'id': existing.id}), 200

    cliente = Cliente(nome=nome, idade=int(idade or 0), endereco=endereco or '', cpf=cpf)
    db.session.add(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente criado', 'id': cliente.id}), 201


@main.route('/cartao', methods=['POST'])
def create_cartao():
    data = request.json or request.form
    nome = data.get('nome')
    numero = data.get('numero')
    vencimento = data.get('vencimento')
    cpf = data.get('cpf')

    if not all([nome, numero, vencimento, cpf]):
        return jsonify({'error': 'nome, numero, vencimento, cpf required'}), 400

    existing = Cartao.query.filter_by(numero=numero).first()
    if existing:
        return jsonify({'message': 'Cartão já existe', 'id': existing.id}), 200

    cartao = Cartao(nome_do_cliente=nome, numero=numero, vencimento=vencimento, cpf_do_cliente=cpf)
    db.session.add(cartao)
    db.session.commit()
    return jsonify({'message': 'Cartão criado', 'id': cartao.id}), 201


@main.route('/pagar_fatura', methods=['POST'])
def pagar_fatura():
    """Deleta todas as transações do cartão vinculado ao CPF (simula pagamento da fatura)."""
    cpf = (request.json or {}).get('cpf', '').strip()
    if not cpf:
        return jsonify({'error': 'cpf obrigatório'}), 400

    cartao = Cartao.query.filter_by(cpf_do_cliente=cpf).first()
    if not cartao:
        return jsonify({'error': 'Nenhum cartão encontrado para este CPF'}), 404

    deleted = Transacao.query.filter_by(cpf_do_cliente=cpf).delete()
    db.session.commit()

    return jsonify({'message': f'{deleted} transação(ões) removida(s). Fatura zerada!'})


@main.route('/transacao', methods=['POST'])
def create_transacao():
    data = request.json or request.form
    cpf = data.get('cpf')
    numero = data.get('numero')
    valor = data.get('valor')
    vencimento = data.get('vencimento')
    id_trans = data.get('id_trans')
    limite = data.get('limite')

    # Basic validation
    if not all([cpf, numero, valor, vencimento, id_trans, limite]):
        return jsonify({'error': 'cpf, numero, valor, vencimento, id_trans, limite are required'}), 400

    # Check cliente exists
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    if not cliente:
        return jsonify({'error': 'cliente_not_found', 'message': 'CPF não encontrado'}), 404

    # Check card exists
    cartao = Cartao.query.filter_by(numero=numero).first()
    if not cartao:
        return jsonify({'error': 'cartao_not_found', 'message': 'Cartão não encontrado'}), 404

    # Calculate used amount for this card
    used = db.session.query(db.func.coalesce(db.func.sum(Transacao.valor_da_transacao), 0)).filter(Transacao.numero_do_cartao == numero).scalar() or 0
    novo_total = used + float(valor)
    if novo_total > float(limite):
        return jsonify({'error': 'exceeds_limit', 'used': used, 'limit': float(limite)}), 400

    trans = Transacao(
        numero_do_cartao=numero,
        vencimento=vencimento,
        cpf_do_cliente=cpf,
        valor_da_transacao=float(valor),
        id_transacao=int(id_trans),
        limite_cartao=float(limite)
    )
    db.session.add(trans)
    db.session.commit()

    return jsonify({'message': 'Transação criada', 'id': trans.id}), 201