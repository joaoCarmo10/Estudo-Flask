from flask import Flask, render_template, request
from lista_filmes import resultado_filmes
from flask_sqlalchemy import SQLAlchemy
from livro import livros

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.sqlite3'

db = SQLAlchemy()
db.init_app(app)


#Localhost:5000

conteudos = []
registros = []

@app.route('/', methods=['GET', 'POST'])
def principal():
    if request.method == 'POST':
        if request.form.get('conteudo'):
            conteudos.append(request.form.get('conteudo'))
    return render_template(
        "index.html",
        conteudos = conteudos
    )

@app.route('/diario', methods=['GET', 'POST'])
def diario():
    if request.method == 'POST':
        if request.form.get("aluno") and request.form.get("nota"):
            aluno = request.form.get("aluno")
            nota = request.form.get("nota")
            registros.append(
                {
                    "aluno":aluno,
                    "nota":nota
                }
            )
    return render_template(
        "sobre.html",
        registros=registros
    )

@app.route('/filmes/<propriedade>')
def lista_filmes(propriedade):
    return render_template(
        "filmes.html",
        filmes=resultado_filmes(propriedade)
    )

@app.route('/livros')
def lista_livros():
    return render_template(
        'livros.html',
        liv = livros.query.all()
    )