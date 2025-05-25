from app import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(45), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', name='fkusuario'), nullable=False)
    imagem_prod = db.Column(db.String(255), nullable=False)

    reservado = db.Column(db.Integer, default=0, nullable=False)  # 0 = não reservado, 1 = reservado
    reserv_user = db.Column(db.Integer, default=0, nullable=False)  # id do usuário que reservou
    likes = db.Column(db.Integer, default=0, nullable=False)

    # Relacionamento com usuário
    usuario = db.relationship('User', backref='produtos')

    def set_reservado(self, status):
        self.reservado = status

    def set_reserv_user(self, user_id):
        self.reserv_user = user_id

    def __repr__(self):
        return f'<Produto {self.titulo}>'
