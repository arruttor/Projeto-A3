from flask import Blueprint, render_template, session, redirect, url_for, request, current_app, flash
from app.models.user import User
from werkzeug.utils import secure_filename  
from app import db
from flask_login import login_user, logout_user, login_required
import os
auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'static/imagens/usuarios'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        senha = request.form['password']

        # Busca o usuário no banco de dados
        user = User.query.filter_by(login=login).first()

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
            new_user = User(login=login, senha=senha, nome=nome, imagem=f'/usuarios/{filename}', cidade = endereco, telefone = telefone)
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

