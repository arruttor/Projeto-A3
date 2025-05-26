from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        senha = request.form['password']

        user = AuthService.autenticar_usuario(login, senha)

        if user:
            session['user_id'] = user.id
            session['username'] = user.login
            session['user_image'] = user.imagem
            session['user_telefone'] = user.telefone
            session['user_cidade'] = user.cidade
            session['user_nome'] = user.nome

            return redirect(url_for('home.home'))

        flash('Usuário ou senha inválidos', 'error')
        return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        dados_formulario = request.form
        arquivo_imagem = request.files.get('imagem')

        user, error = AuthService.registrar_usuario(dados_formulario, arquivo_imagem)

        if user:
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(error, 'error')
            return render_template('registro.html')

    return render_template('registro.html')
