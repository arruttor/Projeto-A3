from app.models.produtos import Produto


class HomeService:
    @staticmethod
    def listar_produtos_disponiveis(user_id):
        """
        Lista produtos que não pertencem ao usuário logado.
        """
        produtos = Produto.query.filter(Produto.usuario_id != user_id).all()
        return produtos
    
    @staticmethod
    def listar_produtos_do_usuario(user_id):
        """
        Lista os produtos que o usuário cadastrou.
        """
        return Produto.query.filter(Produto.usuario_id == user_id).all()

    @staticmethod
    def listar_reservas_do_usuario(user_id):
        """
        Lista os produtos que o usuário reservou.
        """
        return Produto.query.filter(Produto.reserv_user == user_id).all()