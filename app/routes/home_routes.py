from app.services.produto_service import ProdutoService
from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from app.services.home_service import HomeService

home_bp = Blueprint('home', __name__)


@home_bp.route('/home/search_products')
def search_products():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    username = session.get('username')
    user_image = session.get('user_image', 'usuario_padrao.png')

    search_term = request.args.get('searchTerm')

    produtos = ProdutoService.buscar_produtos_por_titulo(search_term, user_id)

    return render_template('home.html',
                           produtos=produtos,
                           username=username,
                           user_image=user_image)

@home_bp.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    username = session.get('username')
    user_image = session.get('user_image', 'usuario_padrao.png')

    produtos = HomeService.listar_produtos_disponiveis(user_id)

    return render_template('home.html',
                           username=username,
                           user_image=user_image,
                           produtos=produtos)

@home_bp.route('/excluir')
def excluir():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    username = session.get('user_nome')
    user_image = session.get('user_image', 'usuario_padrao.png')
    user_telefone = session.get('user_telefone')

    # Busca os produtos que o usuário postou
    produtos = HomeService.listar_produtos_do_usuario(user_id)

    # Busca os produtos que o usuário reservou
    reserva_produtos = HomeService.listar_reservas_do_usuario(user_id)

    total_produtos = len(produtos)
    total_reservas = len(reserva_produtos)

    return render_template(
        'excluir.html',
        produtos=produtos,
        username=username,
        user_image=user_image,
        user_telefone=user_telefone,
        total_produtos=total_produtos,
        reserva_produtos=reserva_produtos,
        total_reservas=total_reservas
    )


    