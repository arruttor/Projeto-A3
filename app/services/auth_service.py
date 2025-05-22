import os
from werkzeug.utils import secure_filename
from flask import current_app
from app.models.user import User
from app import db


class AuthService:
    @staticmethod
    def autenticar_usuario(login, senha):
        user = User.query.filter_by(login=login).first()
        if user and user.senha == senha:
            return user
        return None

    @staticmethod
    def registrar_usuario(dados_formulario, arquivo_imagem):
        email = dados_formulario.get('email')
        senha = dados_formulario.get('senha')
        login = dados_formulario.get('ra')
        nome = dados_formulario.get('nome')
        endereco = dados_formulario.get('endereco')
        telefone = dados_formulario.get('telefone')

        if not email or not senha or not login or not nome:
            return None, "Preencha todos os campos obrigatórios."

        if arquivo_imagem.filename == '':
            return None, "Nenhuma imagem selecionada."

        if arquivo_imagem and AuthService.allowed_file(arquivo_imagem.filename):
            filename = secure_filename(arquivo_imagem.filename)
            caminho = os.path.join('static/imagens/usuarios', filename)
            arquivo_imagem.save(caminho)

            novo_usuario = User(
                login=login,
                senha=senha,
                nome=nome,
                imagem=f'/usuarios/{filename}',
                cidade=endereco,
                telefone=telefone
            )

            try:
                db.session.add(novo_usuario)
                db.session.commit()
                return novo_usuario, None
            except Exception as e:
                db.session.rollback()
                return None, "Erro ao registrar o usuário no banco de dados."
        else:
            return None, "Tipo de arquivo não permitido."

    @staticmethod
    def allowed_file(filename):
        extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in extensoes_permitidas


































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