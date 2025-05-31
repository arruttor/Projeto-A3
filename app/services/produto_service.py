import os
from werkzeug.utils import secure_filename
from flask import session, current_app
from app.models.produtos import Produto
from auth_service import AuthService
from app import db


class ProdutoService:

    @staticmethod
    def listar_produtos_by_filter(*filter):
        return Produto.query.filter(*filter).all

    @staticmethod
    def buscar_produto_por_id(produto_id):
        return Produto.query.filter_by(id_produto=produto_id).first()
    

    @staticmethod
    def buscar_produtos_por_titulo(search_term, user_id):
        if search_term:
            produtos = Produto.query.filter(
                Produto.usuario_id != user_id,
                Produto.titulo.ilike(f'%{search_term}%')
            ).all()
            return produtos
        return []
    

    @staticmethod
    def cadastrar_produto(dados_formulario, arquivo_imagem):
        titulo = dados_formulario.get('titulo')
        descricao = dados_formulario.get('descricao')
        id_usuario = session.get('user_id')

        if not titulo or not descricao:
            return None, "Preencha todos os campos obrigatórios."

        if arquivo_imagem.filename == '':
            return None, "Nenhuma imagem selecionada."

        if arquivo_imagem and AuthService.allowed_file(arquivo_imagem.filename):
            filename = secure_filename(arquivo_imagem.filename)
            caminho_pasta = os.path.join(current_app.root_path, 'static/imagens/produtos')

            os.makedirs(caminho_pasta, exist_ok=True)  # Garante que a pasta exista

            caminho_arquivo = os.path.join(caminho_pasta, filename)
            arquivo_imagem.save(caminho_arquivo)

            novo_produto = Produto(
                titulo=titulo,
                descricao=descricao,
                usuario_id=id_usuario,
                imagem_prod=f'/produtos/{filename}',
                reservado=0,
                reserv_user=0,
                likes=0
            )

            try:
                db.session.add(novo_produto)
                db.session.commit()
                return novo_produto, None
            except Exception as e:
                db.session.rollback()
                return None, "Erro ao cadastrar o produto no banco de dados."
        else:
            return None, "Tipo de arquivo não permitido."
        
        
        
    @staticmethod
    def reservar_produto(produto_id, user_id):
        produto = Produto.query.get(produto_id)

        if not produto:
            return None, "Produto não encontrado."

        if produto.reservado == 1:
            return None, "Este produto já está reservado."

        try:
            produto.reservado = 1
            produto.reserv_user = user_id
            db.session.commit()
            return produto, None
        except Exception as e:
            db.session.rollback()
            return None, "Erro ao reservar o produto. Tente novamente."


    @staticmethod
    def deletar_produto(produto_id):
        produto = Produto.query.get(produto_id)

        if not produto:
            return False, "Produto não encontrado."

        try:
            db.session.delete(produto)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar produto: {e}")
            return False, "Erro ao deletar o produto."

    @staticmethod
    def allowed_file(filename):
        extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in extensoes_permitidas
