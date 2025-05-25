from app import db

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(45), unique=True, nullable=False)
    senha = db.Column(db.String(45), nullable=False)
    nome = db.Column(db.String(45), nullable=False)
    imagem = db.Column(db.String(255), nullable=True)
    cidade = db.Column(db.String(45), nullable=False)
    telefone = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'
