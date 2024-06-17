from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import current_app
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename  
from model import db, Usuarios, Produtos
import os
auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'static/imagens/usuarios'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        senha = request.form['password']

        # Busca o usuário no banco de dados
        user = Usuarios.query.filter_by(login=login).first()

        if user and user.senha == senha:
            # Autenticação bem-sucedida - Redirecione para a página de home
            session['user_id'] = user.id
            session['username'] = user.login
            session['user_image'] = user.imagem  # Adicione a imagem à sessão
            session['user_telefone'] = user.telefone  # Adicione o telefone à sessão
            session['user_cidade'] = user.cidade  # Adicione a cidade à sessão
            session['user_nome'] = user.nome  # Adicione a nome à sessão
            return redirect(url_for('home'))
        else:
            # Autenticação falhou
            flash('Usuário ou senha inválidos', 'error')
            return render_template('login.html')

    return render_template('login.html')

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    app = current_app._get_current_object()
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        login = request.form['ra']
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        if not email or not senha or not login or not nome:
            flash('Preencha todos os campos', 'error')
            return render_template('registro.html', error="Preencha todos os campos")
        file = request.files['imagem']
        if file.filename == '':
            flash('Nenhuma imagem selecionada', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/imagens/usuarios', filename))
            # Crie o novo usuário com o caminho da imagem
            new_user = Usuarios(login=login, senha=senha, nome=nome, imagem=f'/usuarios/{filename}', cidade = endereco, telefone = telefone)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Usuário cadastrado com sucesso!', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash('Erro ao registrar o usuário', 'error')
                return render_template('registro.html', error="Erro ao registrar o usuário")
        else:
            flash('Tipo de arquivo não permitido', 'error')
            return redirect(request.url)
    return render_template('registro.html')

@auth.route('/cadProd', methods=['GET', 'POST'])
def cadProd():
    app = current_app._get_current_object()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        id_usuario = session['user_id']
        if not titulo or not descricao:
            flash('Preencha todos os campos', 'error')
            return render_template('cadProd.html', error="Preencha todos os campos")
        file = request.files['imagem']
        if file.filename == '':
            flash('Nenhuma imagem selecionada', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/imagens/produtos', filename))
            # Crie o novo usuário com o caminho da imagem
            new_prod = Produtos(titulo=titulo, descricao=descricao, usuario_id=id_usuario,
                                 imagem_prod=f'/produtos/{filename}', reservado = 0, reserv_user=0, likes = 0)
            try:
                db.session.add(new_prod)
                db.session.commit()
                flash('Produto cadastrado com sucesso!', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                flash('Erro ao registrar o produto', 'error')
                return render_template('cadProd', error="Erro ao registrar o usuário")
        else:
            flash('Tipo de arquivo não permitido', 'error')
            return redirect(request.url)
    return render_template('cadProd.html')


