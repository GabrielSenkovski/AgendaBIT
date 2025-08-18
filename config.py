# config.py

import os

# Define o diretório base da aplicação para construir caminhos
basedir = os.path.abspath(os.path.dirname(__file__))
# Base dir contém o endereço completo e exato da pasta raiz do projeto


# Classe importada ao init__.py
class Config:
    """Configurações da aplicação Flask."""

    SECRET_KEY = os.environ.get('Chave-teste') or 'uma-chave-secreta-para-desenvolvimento'

    # URL de conexão com o banco de dados.
    # Lê a URL de uma variável de ambiente ou usa um banco SQLite local.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app/agenda.db')

    # Desativa um recurso de signals do SQLAlchemy para economizar recursos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False