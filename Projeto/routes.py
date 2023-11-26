from Projeto import app
from flask import Flask, render_template, request, redirect, url_for
from Projeto.lista_filmes import resultado_filmes
from Projeto.models import livros
from Projeto import db



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
    page = request.args.get('page', 1, type=int)
    per_page = 4
    todos_livros = livros.query.paginate(page=page, per_page=per_page)
    return render_template(
        'livros.html',
        liv = todos_livros
    )

@app.route('/add_livro', methods=['GET','POST'])
def adiciona_livro():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    valor = request.form.get('valor')
    if request.method == 'POST':
        livro_add = livros( 
            nome,
            descricao,
            valor
        )
        db.session.add(livro_add)
        db.session.commit()
        return redirect(url_for('lista_livros'))
    return render_template("novo_livro.html")

@app.route('/<int:id>/atualiza_livro', methods=['GET', 'POST'])
def atualiza_livro(id):
    livro_bd = livros.query.filter_by(id=id).first()
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = request.form['valor']

        livros.query.filter_by(id=id).update({
            "nome": nome,
            "descricao" : descricao,
            "valor" : valor
        })
        db.session.commit()
        return redirect(url_for('lista_livros'))
    return render_template(
        "atualiza_livro.html",
        livro = livro_bd
    )

@app.route('/<int:id>/remove_livro')
def remove_livro(id):
    livro_bd = livros.query.filter_by(id=id).first()
    db.session.delete(livro_bd)
    db.session.commit()
    return redirect(url_for('lista_livros'))