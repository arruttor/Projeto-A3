import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/projetoa3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False