# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Função 'Application Factory'. Cria e configura a aplicação Flask.
    """
    # 1. Cria a instância principal da aplicação Flask.
    app = Flask(__name__)

    # 2. Carrega as configurações a partir do objeto/classe importado de config.py.
    #    O Flask irá procurar por variáveis em maiúsculas na classe Config.
    app.config.from_object(config_class)

    # 3. Inicializa as extensões, conectando-as à nossa aplicação 'app'.
    db.init_app(app)

    # 4. Importa e registra o Blueprint.
    #    Isso "conecta" o conjunto de rotas definido em routes.py à aplicação principal.
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # 5. Retorna a instância da aplicação, agora totalmente montada e configurada.
    return app