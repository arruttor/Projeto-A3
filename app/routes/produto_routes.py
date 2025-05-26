from app.services.produto_service import ProdutoService
from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from app.services.home_service import HomeService

produto_bp = Blueprint('produto', __name__)


@produto_bp.route('/produto/<int:produto_id>/reservar', methods=['POST'])
def reservar_produto(produto_id):
    if 'user_id' not in session:
        flash('Você precisa estar logado para reservar um produto.', 'error')
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')

    produto = ProdutoService.buscar_produto_por_id(produto_id)
    if not produto:
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('main.home'))

    # Verifica se o produto já está reservado
    if produto.reservado:
        flash('Produto já está reservado.', 'warning')
        return redirect(url_for('produto.detalhe_produto', produto_id=produto_id))

    # Atualiza o produto como reservado
    ProdutoService.reservar_produto(produto_id, user_id)

    flash('Produto reservado com sucesso!', 'success')
    return redirect(url_for('produto.detalhe_produto', produto_id=produto_id))


@produto_bp.route('/produto/<int:produto_id>')
def detalhe_produto(produto_id):
    produto = ProdutoService.buscar_produto_por_id(produto_id)
    if not produto:
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('produto.home'))
    return render_template('produto.html', produto=produto)


@produto_bp.route('/produto/novo', methods=['GET', 'POST'])
def criar_produto():
    if request.method == 'POST':
        dados_formulario = request.form
        arquivo_imagem = request.files.get('imagem')

        produto, erro = ProdutoService.cadastrar_produto(dados_formulario, arquivo_imagem)

        if erro:
            flash(erro, 'error')
            return render_template('cadProd.html')

        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('home.home'))

    return render_template('cadProd.html')


@produto_bp.route('/produto/editar/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = ProdutoService.buscar_produto_por_id(produto_id)

    if not produto:
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        dados_formulario = request.form
        arquivo_imagem = request.files.get('imagem')

        produto_atualizado, error = ProdutoService.atualizar_produto(produto_id, dados_formulario, arquivo_imagem)

        if produto_atualizado:
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('home.home'))
        else:
            flash(error, 'error')

    return render_template('form_produto.html', produto=produto)


@produto_bp.route('/produto/deletar/<int:produto_id>', methods=['POST'])
def deletar_produto(produto_id):
    sucesso, error = ProdutoService.deletar_produto(produto_id)

    if sucesso:
        flash('Produto deletado com sucesso!', 'success')
    else:
        flash(error, 'error')

    return redirect(url_for('home.home'))

