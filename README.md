# ClassTrade

Projeto da A3 onde foi desenvolvido um aplicativo para fazer troca de itens usados dentro da comunidade universitária

## Tecnologias usadas

<p>
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-000000.svg?style=for-the-badge&logo=Flask&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-4479A1.svg?style=for-the-badge&logo=MySQL&logoColor=white"/>
</p>

## Como rodar o código

1. Clonar o repositório para a sua máquina local

```
https://github.com/arruttor/Projeto-A3
```
2. Crirar os sudiretorios "usuarios" e "produtos" dentro do diretório: \static\imagens.


3. Instalar bibliotecas.

```
pip install Flask flask_sqlalchemy mysqlclient

```

4. Criar um banco de dados com as seguintes  comandos.
```
CREATE SCHEMA projetoa3;

CREATE TABLE projetoa3.usuarios (
  id INT NOT NULL AUTO_INCREMENT,
  login VARCHAR(45) NOT NULL,
  senha VARCHAR(45) NOT NULL,
  nome VARCHAR(45) NOT NULL,
  imagem VARCHAR(255) NULL,
  cidade VARCHAR(45) NOT NULL,
  telefone VARCHAR(45) NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE,
  UNIQUE INDEX login_UNIQUE (login ASC) VISIBLE);


CREATE TABLE projetoa3.produtos (
  id_produto INT NOT NULL AUTO_INCREMENT,
  titulo VARCHAR(45) NOT NULL,
  descricao VARCHAR(5000) NOT NULL,
  usuario_id INT NULL,
  imagem_prod VARCHAR(255) NULL,
  reservado INT NOT NULL,
  reserv_user INT NOT NULL,
  likes INT NOT NULL,
  PRIMARY KEY (id_produto),
  INDEX ffkuser_idx (usuario_id ASC) VISIBLE,
  CONSTRAINT fkusuario
    FOREIGN KEY (usuario_id)
    REFERENCES projetoa3.usuarios (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
   
```

5. Mudar o arquivo config.py conectando ao banco dados

```
  SQLALCHEMY_DATABASE_URI = 'mysql://usuário do banco:senha@link:porta/nome do banco'
```

5. Rodar a aplicação pelo arquivo app.py

```
python app.py
```
