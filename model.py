from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Crie uma instância do SQLAlchemy aqui



class Entidade:
    def salvar(self):
        db.session.add(self)
        db.session.commit()

    def excluir(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def buscar_por_id(cls, id):
        return cls.query.get_or_404(id)
    @classmethod
    def filtar_tabela(cls,*filtro):
        return cls.query.filter(*filtro).all()


class Usuarios(db.Model, Entidade):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, auto_increment=True)
    login = db.Column(db.String(45), unique=True, nullable=False)
    senha = db.Column(db.String(45), nullable=False)
    nome = db.Column(db.String(45), nullable=False)
    imagem = db.Column(db.String(255), nullable=True)  
    cidade = db.Column(db.String(45), nullable = False)
    telefone = db.Column(db.String(45), nullable = False)

    def __repr__(self):
        return f'<Usuarios {self.login}>'
    
class Produtos(db.Model, Entidade):#define o objeto com as propriedades do produto
    id_produto = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, auto_increment=True)
    titulo = db.Column(db.String(45), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', name='fkusuario'), nullable=False) 
    imagem_prod = db.Column(db.String(255), nullable=False)
    reservado = db.Column(db.Integer, nullable=False)
    reserv_user = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable = False)

    # Define a relação com a tabela Usuarios
    usuario = db.relationship('Usuarios', backref='produtos')
    def set_reservado(self, R):
        self.reservado = R
    
    def set_reserv_user(self, id):
        self.reserv_user = id
    


    def __repr__(self):
        return f'<Produtos {self.titulo}>'
    
