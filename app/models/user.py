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