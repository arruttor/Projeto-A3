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

