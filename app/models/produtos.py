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