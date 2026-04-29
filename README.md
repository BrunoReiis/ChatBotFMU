# 💳 ChatBot NexusBank

Trabalho acadêmico desenvolvido para a disciplina de **Inteligência Artificial e Aprendizado de Máquina**, utilizando Flask, SQLite e aprendizado de máquina para construir um chatbot interativo de operadora de cartão de crédito.

---

## 👨‍🎓 Alunos

| Nome | RA |
|---|---|
| Bruno Dos Reis Ferreira Santos | 2564952 |
| Matheus Francisco da Silva Costa | 2693112 |

---

## 📋 Descrição do Projeto

O **ChatBot NexusBank** é uma aplicação web desenvolvida em Python com o framework **Flask**. Ele simula o atendimento virtual de uma operadora de cartão de crédito, permitindo que o usuário:

- Se identifique pelo **CPF**
- Realize **cadastro** de cliente e cartão diretamente pelo chat
- Consulte informações como **fatura, limite, saldo, extrato, parcelamento**, entre outros
- **Adicione transações** ao seu cartão via chat
- **Registre o pagamento da fatura**, zerando o saldo de transações

O chatbot utiliza um modelo de **Machine Learning** (TF-IDF + Naive Bayes) treinado com mais de 270 frases em português, organizadas em 25 categorias de atendimento.

---

## 🗂️ Estrutura do Projeto

```
ChatBot/
├── app/
│   ├── __init__.py          # Fábrica da aplicação Flask (create_app)
│   ├── routes.py            # Rotas e endpoints da API
│   ├── chatbot.py           # Lógica do chatbot (modelo ML)
│   ├── models.py            # Modelos do banco de dados (SQLAlchemy)
│   ├── db.py                # Inicialização do SQLAlchemy
│   ├── templates/
│   │   └── index.html       # Interface do chatbot (HTML)
│   └── static/
│       ├── css/
│       │   └── styles.css   # Estilos da interface
│       └── js/
│           └── chat.js      # Máquina de estados do chat (JavaScript)
├── data/
│   ├── app.db               # Banco de dados SQLite
│   ├── perguntas.csv        # Frases de treinamento do modelo
│   └── respostas.json       # Respostas por categoria
├── sql/
│   └── Estruturas/
│       ├── create_tables.sql
│       ├── seed_data.sql
│       └── Tabelas/
│           ├── Cliente.sql
│           ├── Cartao.sql
│           └── Transacoes.sql
├── scripts/
│   ├── init_db.py           # Inicializa o banco via SQL
│   ├── check_db.py          # Diagnóstico do banco
│   └── check_app.py         # Diagnóstico da aplicação
├── tests/
│   └── test_app.py          # Testes automatizados
├── config.py                # Configurações da aplicação
├── run.py                   # Ponto de entrada da aplicação
└── requirements.txt         # Dependências Python
```

---

## 🗃️ Banco de Dados

O projeto utiliza **SQLite** com as seguintes tabelas:

| Tabela | Descrição |
|---|---|
| `CLIENTE` | Armazena nome, idade, endereço e CPF do cliente |
| `CARTAO` | Armazena número, vencimento e CPF do titular |
| `TRANSACOES` | Armazena todas as transações realizadas por cartão/CPF |
| `perguntas` | Frases de treinamento do modelo ML |
| `respostas` | Respostas cadastradas por categoria |

---

## 🤖 Modelo de Machine Learning

- **Vetorização:** `TfidfVectorizer` com `ngram_range=(1,2)`
- **Classificador:** `MultinomialNB` com `alpha=0.5`
- **Pipeline:** scikit-learn `Pipeline`
- **Treinamento:** 270+ frases em português, 25 categorias
- **Categorias:** limite, fatura, pagamento, taxas, desbloqueio, saldo, extrato, bloqueio, fraude, cashback, pontos, senha, parcelamento, viagem, cancelamento, segunda_via, seguro, pix, entre outras

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- pip

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Inicializar o banco de dados (opcional)

```bash
python scripts/init_db.py
```

> O banco também é criado automaticamente ao iniciar a aplicação via `db.create_all()`.

### 3. Executar a aplicação

```bash
python run.py
```

### 4. Acessar no navegador

```
http://127.0.0.1:5000
```

---

## 💬 Funcionalidades do Chat

| Ação do usuário | Comportamento |
|---|---|
| Informa o CPF | Verifica cadastro; se novo, inicia wizard de cadastro |
| Cadastro guiado | Coleta nome, idade, endereço, número e vencimento do cartão |
| Perguntas gerais | Resposta do modelo ML (fatura, limite, saldo, etc.) |
| `"Qual o valor da minha fatura?"` | Retorna a soma real das transações do CPF no banco |
| `"Quero adicionar uma transação"` | Inicia fluxo de registro de transação (valor + data) |
| `"Paguei a fatura"` | Zera todas as transações do cartão (simula pagamento) |

---

## 📦 Dependências

```
Flask
Flask-SQLAlchemy
pandas
scikit-learn
numpy
gunicorn
python-dotenv
```

---

## 🏫 Informações Acadêmicas

- **Curso:** Análise e Desenvolvimento de Sistemas
- **Disciplina:** Banco de Dados
- **Ano/Semestre:** 2026 — 1º Semestre