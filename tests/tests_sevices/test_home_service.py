import pytest
from app import db
from app.models.produtos import Produto
from app.services.home_service import HomeService


def criar_produto(titulo, usuario_id, reservado=0, reserv_user=0):
    produto = Produto(
        titulo=titulo,
        descricao='Descrição teste',
        usuario_id=usuario_id,
        imagem_prod='/produtos/teste.jpg',
        reservado=reservado,
        reserv_user=reserv_user,
        likes=0
    )
    db.session.add(produto)
    db.session.commit()
    db.session.refresh(produto)
    return produto


def test_listar_produtos_disponiveis(app):
    with app.app_context():
        # Cria produtos de dois usuários diferentes
        produto1 = criar_produto('Produto User 1', usuario_id=1)
        produto2 = criar_produto('Produto User 2', usuario_id=2)

        produtos_disponiveis = HomeService.listar_produtos_disponiveis(1)

        assert produto2 in produtos_disponiveis
        assert produto1 not in produtos_disponiveis


def test_listar_produtos_do_usuario(app):
    with app.app_context():
        produto1 = criar_produto('Produto A', usuario_id=1)
        produto2 = criar_produto('Produto B', usuario_id=1)
        produto3 = criar_produto('Produto C', usuario_id=2)

        produtos_usuario = HomeService.listar_produtos_do_usuario(1)

        assert produto1 in produtos_usuario
        assert produto2 in produtos_usuario
        assert produto3 not in produtos_usuario


def test_listar_reservas_do_usuario(app):
    with app.app_context():
        produto1 = criar_produto('Produto Reservado A', usuario_id=2, reservado=1, reserv_user=1)
        produto2 = criar_produto('Produto Reservado B', usuario_id=3, reservado=1, reserv_user=1)
        produto3 = criar_produto('Produto Livre', usuario_id=3)

        reservas = HomeService.listar_reservas_do_usuario(1)

        assert produto1 in reservas
        assert produto2 in reservas
        assert produto3 not in reservas
