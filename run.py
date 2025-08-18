# run.py

# 1. Importa a função 'create_app' que está dentro do arquivo __init__.py no dir 'app'.
from app import create_app

# 2. Executa a função para criar a instância da nossa aplicação Flask.
#    Neste momento carrega as configurações e registra os Blueprints.
app = create_app()

# 3. Bloco padrão do Python para garantir que o servidor só será executado
#    quando este script 'run.py' for chamado diretamente.
if __name__ == '__main__':
    app.run(debug=True)