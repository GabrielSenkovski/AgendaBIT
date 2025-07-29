# AgendaBIT
Criação de Agenda Web funcional para apresentar no processo seletivo da Bit Code.


# Proposta de Projeto: Agenda Web Funcional

## Status do Projeto

:hourglass: **Em fase de Planejamento/Proposta.**

## Objetivo Técnico

Desenvolver uma aplicação web CRUD (Create, Read, Update, Delete) para o gerenciamento de agendamentos, utilizando Python e o ecossistema Flask.

* **Backend:**
    * **Python 3:** Linguagem principal do projeto.
    * **Flask:** Microframework web para o roteamento de URLs e lógica de negócio. Escolhido por sua leveza e controle granular.

* **Persistência de Dados:**
    * **SQLite:** SGBD embutido para agilidade no desenvolvimento e ausência de configuração de servidor.
    * **Flask-SQLAlchemy:** Camada de abstração (ORM) para mapear objetos Python para o banco de dados.
    * 
* **Frontend & Formulários:**
    * **Jinja2:** Motor de templates para renderização dinâmica do HTML no servidor.
    * **Bootstrap:** Framework CSS para a criação rápida de uma interface limpa e responsiva.
    * **Flask-WTF:** Biblioteca para validação segura de formulários.

## Arquitetura Planejada

A aplicação seguirá uma arquitetura simples. O Flask será responsável por receber as requisições HTTP, processar a lógica de negócio, interagir com o banco de dados através da ORM e renderizar os templates HTML para o cliente.

## Funcionalidades Planejadas

- [ ] Criação de novos agendamentos através de um formulário web.
- [ ] Listagem de todos os agendamentos existentes na página principal.
- [ ] Edição de agendamentos existentes.
- [ ] Exclusão de agendamentos com confirmação.
