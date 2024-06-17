from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import check_password_hash

from config import Config
from model import db, Usuarios, Produtos
from auth import auth  # Importe o Blueprint de autenticação

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'imagens')  # Define a pasta de upload
db.init_app(app)

app.secret_key = 'SECRETO'  # Defina uma chave secreta para sessões


app.register_blueprint(auth, url_prefix='/')# Registrar o Blueprint de autenticação

@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        username = session['username']
        user_image = session['user_image']
        produtos = Produtos.filtar_tabela(Produtos.usuario_id != user_id)
        return render_template('home.html', username=username, user_image=user_image, produtos=produtos)
    else:
        return redirect(url_for('auth.login'))

@app.route('/produto/<int:produto_id>')# define a rota que direciona para a configuração da página produto
def produto(produto_id):
    produto = Produtos.buscar_por_id(produto_id) # faz o select na tabela
    session['produto_id'] = produto_id  # Armazene apenas o ID do produto na sessão
    return render_template('produto.html', produto=produto)  

@app.route('/produto', methods=['GET', 'POST'])# define a rota que direciona para a página produto
def produto_view():
    if 'produto_id' in session:
        produto_id = session['produto_id']  
        if request.method == 'POST':    
            #parte para a reserva
            produto_db = Produtos.buscar_por_id(produto_id)  # Busca o produto do banco de dados
            produto_db.set_reservado(1)  # Define como reservado
            produto_db.set_reserv_user(session['user_id'])
            produto_db.salvar()# update na tebela
            flash('Produto reservado com sucesso!', 'success')
            return redirect(url_for('produto_view'))
        else:
            # Carrega a página pela primeira vez
            produto = Produtos.buscar_por_id(produto_id) 
            return render_template('produto.html', produto=produto)
    else:
        return redirect(url_for('home'))
    
@app.route('/excluir')# define a rota que direciona para a página do menu
def excluir():
    if 'user_id' in session: #verifica o usuário na sessão
        user_id = session['user_id']
        username = session['user_nome']
        user_image = session['user_image']
        user_telefone = session['user_telefone']
        produtos = Produtos.filtar_tabela(Produtos.usuario_id == user_id) #busca os produtos que o usuário postou
        reserva_produtos = Produtos.filtar_tabela(Produtos.reserv_user == user_id)#busca os produtos que o usuário Reservou
        total_produtos = len(produtos)  # Conte o número de produtos
        total_reservas = len(reserva_produtos) # Conte o número de reservas
        return render_template('excluir.html', produtos=produtos, username=username, #abre a tela do menu com os parametros certos
                                user_image=user_image, total_produtos=total_produtos, 
                                reserva_produtos=reserva_produtos,user_telefone = user_telefone, total_reservas = total_reservas)
    else:
        return redirect(url_for('auth.login'))
    

@app.route('/excluir_produto/<int:produto_id>', methods=['GET', 'POST'])
def excluir_produto(produto_id):
    if 'user_id' in session:
        user_id = session['user_id']
        produto = Produtos.query.filter(Produtos.id_produto==produto_id, Produtos.usuario_id==user_id).first()

        if produto:
            produto.excluir()
            flash('Produto excluído com sucesso!', 'success')
            return redirect(url_for('excluir'))
        else:
            flash('Erro ao excluir produto', 'error')
            return redirect(url_for('excluir'))
    else:
        return redirect(url_for('auth.login'))
    

@app.route('/update_like/<int:produto_id>/<action>')
def update_like(produto_id, action):
    if 'user_id' in session:
        user_id = session['user_id']
        produto = Produtos.query.get_or_404(produto_id)

        if produto:
            if action == 'like':
                produto.likes += 1
                flash('Você curtiu o produto!', 'success')
            elif action == 'unlike':
                produto.likes -= 1
                flash('Você descurtiu o produto!', 'success')
            else:
                flash('Ação inválida', 'error')
                return redirect(url_for('produto', produto_id=produto_id))

            db.session.commit()
            return redirect(url_for('produto', produto_id=produto_id))
        else:
            flash('Produto não encontrado', 'error')
            return redirect(url_for('home'))
    else:
        flash('Você precisa estar logado para curtir o produto', 'error')
        return redirect(url_for('auth.login'))
    
@app.route('/search_products')
def search_products():
    searchTerm = request.args.get('searchTerm')
    if searchTerm:
        # Faz a consulta SQL para encontrar produtos com títulos semelhantes
        produtos = Produtos.filtar_tabela(Produtos.titulo.ilike(f'%{searchTerm}%'))
        # direciona o template home.html com os produtos da busca
        return render_template('home.html', produtos=produtos, username=session.get('username'), user_image=session.get('user_image'))
    else:
        # direciona a página home.html normal se não houver termo de pesquisa
        return render_template('home.html', username=session.get('username'), user_image=session.get('user_image'))

if __name__ == '__main__':
    with app.app_context():  # Crie um contexto de aplicativo para inicializar o banco de dados
        db.create_all()  # Crie as tabelas no banco de dados
    app.run(debug=True)