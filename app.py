# app.py

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# --- CONFIGURAÇÃO DA APLICAÇÃO ---
app = Flask(__name__)

# Configuração do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'agenda.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sanshdu12312bh2bh3b1h2' # Necessário para mensagens flash

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)


# --- MODELO DO BANCO DE DADOS ---
# Define a estrutura da tabela de agendamentos
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    data_evento = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Agendamento {self.titulo}>'


# --- ROTAS DA APLICAÇÃO (As "páginas" da agenda) ---

# Rota principal: Lista todos os agendamentos
@app.route('/')
def index():
    # Busca todos os agendamentos no banco, ordenados pela data
    agendamentos = Agendamento.query.order_by(Agendamento.data_evento).all()
    # Renderiza o template 'index.html' passando a lista de agendamentos
    return render_template('index.html', agendamentos=agendamentos)


# Rota para adicionar um novo agendamento
@app.route('/add', methods=['GET', 'POST'])
def add():
    # Se o formulário for enviado (método POST)
    if request.method == 'POST':
        titulo = request.form['titulo']
        # Converte a string da data do formulário para um objeto date do Python
        data_evento_str = request.form['data_evento']
        data_evento = datetime.strptime(data_evento_str, '%Y-%m-%d').date()
        descricao = request.form['descricao']

        # Cria um novo objeto Agendamento com os dados do formulário
        novo_agendamento = Agendamento(titulo=titulo, data_evento=data_evento, descricao=descricao)

        try:
            # Adiciona o novo agendamento ao banco de dados
            db.session.add(novo_agendamento)
            db.session.commit()
            flash('Agendamento adicionado com sucesso!', 'success')
            # Redireciona para a página principal
            return redirect(url_for('index'))
        except:
            flash('Ocorreu um erro ao adicionar o agendamento.', 'danger')
            return redirect(url_for('add'))

    # Se a requisição for GET, apenas mostra a página com o formulário
    return render_template('form.html', titulo_pagina="Novo Agendamento", agendamento=None)


# Rota para editar um agendamento existente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Busca o agendamento pelo ID ou retorna um erro 404 se não encontrar
    agendamento = Agendamento.query.get_or_404(id)

    if request.method == 'POST':
        # Atualiza os dados do agendamento com as informações do formulário
        agendamento.titulo = request.form['titulo']
        agendamento.data_evento = datetime.strptime(request.form['data_evento'], '%Y-%m-%d').date()
        agendamento.descricao = request.form['descricao']
        
        try:
            db.session.commit()
            flash('Agendamento atualizado com sucesso!', 'success')
            return redirect(url_for('index'))
        except:
            flash('Ocorreu um erro ao atualizar o agendamento.', 'danger')
            return redirect(url_for('edit', id=id))

    # Se a requisição for GET, mostra o formulário preenchido com os dados do agendamento
    return render_template('form.html', titulo_pagina="Editar Agendamento", agendamento=agendamento)


# Rota para excluir um agendamento
@app.route('/delete/<int:id>')
def delete(id):
    agendamento_para_deletar = Agendamento.query.get_or_404(id)
    try:
        db.session.delete(agendamento_para_deletar)
        db.session.commit()
        flash('Agendamento excluído com sucesso!', 'success')
        return redirect(url_for('index'))
    except:
        flash('Ocorreu um erro ao excluir o agendamento.', 'danger')
        return redirect(url_for('index'))

# --- INICIALIZAÇÃO DA APLICAÇÃO ---
if __name__ == "__main__":
    # Cria o banco de dados e as tabelas se eles não existirem
    with app.app_context():
        db.create_all()
    # Roda a aplicação em modo de desenvolvimento (debug)
    app.run(debug=True)