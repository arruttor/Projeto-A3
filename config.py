import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/projetoa3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "basesql.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Banco em memória para testes
    WTF_CSRF_ENABLED = False  # Desativa CSRF nos testes se estiver usando formulários