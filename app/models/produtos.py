from app import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id_produto = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(45), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', name='fkusuario'), nullable=False) 
    imagem_prod = db.Column(db.String(255), nullable=False)
    reservado = db.Column(db.Integer, nullable=False)
    reserv_user = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable = False)

    # Define a relação com a tabela Usuarios
    usuario = db.relationship('User', backref='produtos')
    def set_reservado(self, R):
        self.reservado = R
    
    def set_reserv_user(self, id):
        self.reserv_user = id




    def __repr__(self):
        return f'<Produtos {self.titulo}>'
    