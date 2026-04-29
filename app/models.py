from .db import db


class Pergunta(db.Model):
    __tablename__ = 'perguntas'

    id = db.Column(db.Integer, primary_key=True)
    frase = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String, nullable=False)


class Resposta(db.Model):
    __tablename__ = 'respostas'

    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String, nullable=False)
    resposta = db.Column(db.String, nullable=False)


# Domain models for cliente / cartao / transacoes (match SQL in sql/Estruturas/Tabelas)
class Cliente(db.Model):
    __tablename__ = 'CLIENTE'

    id = db.Column('ID', db.Integer, primary_key=True)
    nome = db.Column('NOME', db.String, nullable=False)
    idade = db.Column('IDADE', db.Integer, nullable=False)
    endereco = db.Column('ENDERECO', db.String, nullable=False)
    cpf = db.Column('CPF', db.String, nullable=False, unique=True)


class Cartao(db.Model):
    __tablename__ = 'CARTAO'

    id = db.Column('ID', db.Integer, primary_key=True)
    nome_do_cliente = db.Column('NOMEDOCLIENTE', db.String, nullable=False)
    numero = db.Column('NUMERODOCARTAO', db.String, nullable=False, unique=True)
    vencimento = db.Column('VENCIMENTO', db.String, nullable=False)
    cpf_do_cliente = db.Column('CPFDOCLIENTE', db.String, nullable=False)


class Transacao(db.Model):
    __tablename__ = 'TRANSACOES'

    id = db.Column('ID', db.Integer, primary_key=True)
    numero_do_cartao = db.Column('NUMERODOCARTAO', db.String, nullable=False)
    vencimento = db.Column('VENCIMENTO', db.String, nullable=False)
    cpf_do_cliente = db.Column('CPFDOCLIENTE', db.String, nullable=False)
    valor_da_transacao = db.Column('VALORDATRANSACAO', db.Float, nullable=False)
    data_da_transacao = db.Column('DATATRANSACAO', db.DateTime)
    id_transacao = db.Column('IDTRANSACAO', db.Integer, nullable=False)
    limite_cartao = db.Column('LIMITECARTAO', db.Float, nullable=False)