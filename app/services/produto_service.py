import os
from werkzeug.utils import secure_filename
from models.produtos import Produto
from app import db


class ProdutoService:

    @staticmethod
    def listar_produtos():
        return Produto.query.all()

    @staticmethod
    def buscar_produto_por_id(produto_id):
        return Produto.query.get(produto_id)

    @staticmethod
    def criar_produto(dados_formulario, arquivo_imagem):
        nome = dados_formulario.get('nome')
        descricao = dados_formulario.get('descricao')
        preco = dados_formulario.get('preco')

        if not nome or not preco:
            return None, "Nome e preço são obrigatórios."

        if arquivo_imagem and ProdutoService.allowed_file(arquivo_imagem.filename):
            filename = secure_filename(arquivo_imagem.filename)
            caminho = os.path.join('static/imagens/produtos', filename)
            arquivo_imagem.save(caminho)
            imagem_url = f'/produtos/{filename}'
        else:
            imagem_url = None  # Pode ser opcional

        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            imagem=imagem_url
        )

        try:
            db.session.add(novo_produto)
            db.session.commit()
            return novo_produto, None
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar produto: {e}")
            return None, "Erro ao salvar o produto no banco de dados."

    @staticmethod
    def atualizar_produto(produto_id, dados_formulario, arquivo_imagem):
        produto = Produto.query.get(produto_id)

        if not produto:
            return None, "Produto não encontrado."

        produto.nome = dados_formulario.get('nome')
        produto.descricao = dados_formulario.get('descricao')
        produto.preco = dados_formulario.get('preco')

        if arquivo_imagem and ProdutoService.allowed_file(arquivo_imagem.filename):
            filename = secure_filename(arquivo_imagem.filename)
            caminho = os.path.join('static/imagens/produtos', filename)
            arquivo_imagem.save(caminho)
            produto.imagem = f'/produtos/{filename}'

        try:
            db.session.commit()
            return produto, None
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar produto: {e}")
            return None, "Erro ao atualizar o produto."

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
