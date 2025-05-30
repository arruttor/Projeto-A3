import os
import pytest
from flask import session
from app import db
from app.models.produtos import Produto
from app.services.produto_service import ProdutoService
from werkzeug.datastructures import FileStorage
from io import BytesIO


@pytest.fixture
def fake_image():
    return FileStorage(
        stream=BytesIO(b"fake image data"),
        filename="teste.jpg",
        content_type="image/jpeg",
    )


@pytest.fixture
def dados_formulario():
    return {
        'titulo': 'Produto Teste',
        'descricao': 'Descrição de teste'
    }


def test_cadastrar_produto_sucesso(app, fake_image, dados_formulario):
    with app.app_context():
        with app.test_request_context():
            session['user_id'] = 1  # Simula um usuário logado

            produto, erro = ProdutoService.cadastrar_produto(dados_formulario, fake_image)

            assert erro is None
            assert produto is not None
            assert produto.titulo == 'Produto Teste'
            assert produto.imagem_prod.endswith('teste.jpg')

            caminho_arquivo = os.path.join(
                app.root_path, 'static/imagens/produtos', 'teste.jpg'
            )
            assert os.path.exists(caminho_arquivo)

            # Limpeza do arquivo criado
            os.remove(caminho_arquivo)


def test_cadastrar_produto_sem_titulo(app, fake_image):
    with app.app_context():
        with app.test_request_context():
            session['user_id'] = 1
            dados = {'titulo': '', 'descricao': 'Descrição'}

            produto, erro = ProdutoService.cadastrar_produto(dados, fake_image)

            assert produto is None
            assert erro == "Preencha todos os campos obrigatórios."


def test_reservar_produto_sucesso(app):
    with app.app_context():
        produto = Produto(
            titulo='Produto Reservar',
            descricao='Descrição',
            usuario_id=1,
            imagem_prod='/produtos/teste.jpg',
            reservado=0,
            reserv_user=0,
            likes=0
        )
        db.session.add(produto)
        db.session.commit()
        db.session.refresh(produto)

        produto_reservado, erro = ProdutoService.reservar_produto(produto.id_produto, 2)

        assert erro is None
        assert produto_reservado is not None
        assert produto_reservado.reservado == 1
        assert produto_reservado.reserv_user == 2


def test_reservar_produto_ja_reservado(app):
    with app.app_context():
        produto = Produto(
            titulo='Produto Reservado',
            descricao='Descrição',
            usuario_id=1,
            imagem_prod='/produtos/teste.jpg',
            reservado=1,
            reserv_user=2,
            likes=0
        )
        db.session.add(produto)
        db.session.commit()
        db.session.refresh(produto)

        produto_reservado, erro = ProdutoService.reservar_produto(produto.id_produto, 3)

        assert produto_reservado is None
        assert erro == "Este produto já está reservado."


def test_reservar_produto_inexistente(app):
    with app.app_context():
        produto_reservado, erro = ProdutoService.reservar_produto(999, 2)

        assert produto_reservado is None
        assert erro == "Produto não encontrado."


def test_deletar_produto_sucesso(app):
    with app.app_context():
        produto = Produto(
            titulo='Produto Deletar',
            descricao='Descrição',
            usuario_id=1,
            imagem_prod='/produtos/teste.jpg',
            reservado=0,
            reserv_user=0,
            likes=0
        )
        db.session.add(produto)
        db.session.commit()
        db.session.refresh(produto)

        sucesso, erro = ProdutoService.deletar_produto(produto.id_produto)

        assert sucesso is True
        assert erro is None
        assert Produto.query.get(produto.id_produto) is None


def test_deletar_produto_inexistente(app):
    with app.app_context():
        sucesso, erro = ProdutoService.deletar_produto(999)

        assert sucesso is False
        assert erro == "Produto não encontrado."


def test_buscar_produtos_por_titulo(app):
    with app.app_context():
        produto = Produto(
            titulo='Cadeira Gamer',
            descricao='Uma cadeira muito confortável',
            usuario_id=1,
            imagem_prod='/produtos/cadeira.jpg',
            reservado=0,
            reserv_user=0,
            likes=0
        )
        db.session.add(produto)
        db.session.commit()

        resultados = ProdutoService.buscar_produtos_por_titulo('cadeira', user_id=2)

        assert len(resultados) == 1
        assert resultados[0].titulo == 'Cadeira Gamer'
