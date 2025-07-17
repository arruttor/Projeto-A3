from flask import current_app
from sqlalchemy import inspect
from ..db import db
from ..models.user import User
from ..models.produtos import Produto


def verifica_tabela_criada():
    with current_app.app_context():
        inspector = inspect(db.engine)
        if not(inspector.has_table(Produto.__tablename__) and inspector.has_table(User.__tablename__)):
            db.create_all()
            print('criando tabelas')
        else:
            print('tabelas já criadas')