from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.produto_service import ProdutoService

main_bp = Blueprint('main', __name__)


@main_bp.route('/home')
def home():
    produtos = ProdutoService.listar_produtos()
    return render_template('home.html', produtos=produtos)


@main_bp.route('/produto/<int:produto_id>')
def detalhe_produto(produto_id):
    produto = ProdutoService.buscar_produto_por_id(produto_id)
    if not produto:
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('main.home'))
    return render_template('detalhe_produto.html', produto=produto)


@main_bp.route('/produto/novo', methods=['GET', 'POST'])
def criar_produto():
    if request.method == 'POST':
        dados_formulario = request.form
        arquivo_imagem = request.files.get('imagem')

        produto, error = ProdutoService.criar_produto(dados_formulario, arquivo_imagem)

        if produto:
            flash('Produto criado com sucesso!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(error, 'error')
            return render_template('form_produto.html')

    return render_template('form_produto.html')


@main_bp.route('/produto/editar/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = ProdutoService.buscar_produto_por_id(produto_id)

    if not produto:
        flash('Produto não encontrado.', 'error')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        dados_formulario = request.form
        arquivo_imagem = request.files.get('imagem')

        produto_atualizado, error = ProdutoService.atualizar_produto(produto_id, dados_formulario, arquivo_imagem)

        if produto_atualizado:
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash(error, 'error')

    return render_template('form_produto.html', produto=produto)


@main_bp.route('/produto/deletar/<int:produto_id>', methods=['POST'])
def deletar_produto(produto_id):
    sucesso, error = ProdutoService.deletar_produto(produto_id)

    if sucesso:
        flash('Produto deletado com sucesso!', 'success')
    else:
        flash(error, 'error')

    return redirect(url_for('main.home'))
