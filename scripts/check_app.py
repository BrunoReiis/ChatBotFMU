from app import create_app
app = create_app()
print('App created. Chatbot:', getattr(app, 'chatbot', None))
print('Config DB URI:', app.config.get('SQLALCHEMY_DATABASE_URI'))
