# app.py

import os
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Time

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
    hora_inicio = db.Column(db.Time, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Agendamento {self.titulo}>'


# --- ROTAS DA APLICAÇÃO (As "páginas" da agenda) ---

# Rota principal: Lista todos os agendamentos
@app.route('/')
def index():
    # --- 1. Lógica para a Semana Atual (Domingo a Sábado) ---
    hoje = date.today()
    # Encontra o último Domingo. weekday() é Seg=0..Dom=6. Se hoje for Domingo (6), subtrai 0. Se for Seg(0), subtrai 1.
    offset = (hoje.weekday() + 1) % 7
    inicio_semana = hoje - timedelta(days=offset)
    fim_semana = inicio_semana + timedelta(days=6)
    
    # Lista de tradução para os dias da semana (Domingo=0, ..., Sábado=6 para a nossa tabela)
    dias_em_portugues = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]

    # Cria a lista de dias da semana para o cabeçalho
    dias_da_semana = []
    for i in range(7):
        dia_atual = inicio_semana + timedelta(days=i)
        nome_do_dia = dias_em_portugues[i]
        dias_da_semana.append({"data_obj": dia_atual, "nome": nome_do_dia})

    # --- 2. Busca Agendamentos Apenas da Semana Atual ---
    agendamentos_semana = Agendamento.query.filter(
        Agendamento.data_evento.between(inicio_semana, fim_semana)
    ).all()

    # --- 3. Cria a Estrutura de Dados para o Calendário ---
    horas = [f"{h:02d}:00" for h in range(7, 19)] 
    calendario = {hora: [None] * 7 for hora in horas}

    for agendamento in agendamentos_semana:
        # Calcula o índice do dia (0 para Domingo, 1 para Segunda, etc.)
        dia_idx = (agendamento.data_evento - inicio_semana).days
        hora_str = agendamento.hora_inicio.strftime("%H:00")
        
        if hora_str in calendario and 0 <= dia_idx < 7:
            calendario[hora_str][dia_idx] = agendamento

    # --- 4. Busca os Próximos Compromissos ---
    proximos_agendamentos = Agendamento.query.filter(
        Agendamento.data_evento >= hoje
    ).order_by(Agendamento.data_evento, Agendamento.hora_inicio).limit(5).all()

    # --- 5. Renderiza o template ---
    return render_template(
        'index.html', 
        agendamentos=proximos_agendamentos,
        calendario=calendario,
        dias_da_semana=dias_da_semana,
        now=datetime.now()
    )


# Rota para adicionar um novo agendamento
@app.route('/add', methods=['GET', 'POST'])
def add():
    # Se o formulário for enviado (método POST)
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        data_evento_str = request.form.get('data_evento')
        hora_inicio_str = request.form.get('hora_inicio')
        descricao = request.form.get('descricao')

        if not titulo or not data_evento_str or not hora_inicio_str:
            flash('Título, data e hora são campos obrigatórios.', 'warning')
            return redirect(url_for('add'))

        try:
            # Converte a string da data do formulário para um objeto date do Python
            data_evento = datetime.strptime(data_evento_str, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()

            # Cria um novo objeto Agendamento com os dados do formulário
            novo_agendamento = Agendamento(
                titulo=titulo, 
                data_evento=data_evento,
                hora_inicio=hora_inicio,
                descricao=descricao)

            # Adiciona o novo agendamento ao banco de dados
            db.session.add(novo_agendamento)
            db.session.commit()
            flash('Agendamento adicionado com sucesso!', 'success')
            # Redireciona para a página principal
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao adicionar o agendamento: {e}', 'danger')
            return redirect(url_for('add'))

    # Se a requisição for GET, apenas mostra a página com o formulário
    return render_template('form.html', titulo_pagina="Novo Agendamento", agendamento=None)


# Rota para editar um agendamento existente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Busca o agendamento pelo ID ou retorna um erro 404 se não encontrar
    agendamento = Agendamento.query.get_or_404(id)

    if request.method == 'POST':
        try:
            # Atualiza os dados do agendamento com as informações do formulário
            agendamento.titulo = request.form.get('titulo')
            agendamento.data_evento = datetime.strptime(request.form.get('data_evento'), '%Y-%m-%d').date()
            agendamento.hora_inicio = datetime.strptime(request.form.get('hora_inicio'), '%H:%M').time()
            agendamento.descricao = request.form.get('descricao')
            
            db.session.commit()
            flash('Agendamento atualizado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao atualizar o agendamento: {e}', 'danger')
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
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao excluir o agendamento: {e}', 'danger')
        return redirect(url_for('index'))

# --- INICIALIZAÇÃO DA APLICAÇÃO ---
if __name__ == "__main__":
    # Cria o banco de dados e as tabelas se eles não existirem
    with app.app_context():
        db.create_all()
    # Roda a aplicação em modo de desenvolvimento (debug)
    app.run(debug=True)