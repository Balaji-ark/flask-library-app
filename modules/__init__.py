from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../templates')  # Explicitly set the template folder
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .models import User, Book

        from .user import user_bp
        from .books import books_bp
        from .chatbot import chatbot_bp

        app.register_blueprint(user_bp)
        app.register_blueprint(books_bp)
        app.register_blueprint(chatbot_bp)

        return app
