from flask import Flask
from .db import init_db, db
from .routes import main as main_routes


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    init_db(app)

    # Cria todas as tabelas dos modelos SQLAlchemy no banco configurado
    from . import models  # garante que os modelos estão registrados
    with app.app_context():
        db.create_all()

    # initialize chatbot at app startup (direct instantiation)
    from .chatbot import ChatBot
    try:
        app.chatbot = ChatBot()
    except Exception as e:
        print('Warning initializing ChatBot:', e)
        app.chatbot = None

    app.register_blueprint(main_routes)

    return app