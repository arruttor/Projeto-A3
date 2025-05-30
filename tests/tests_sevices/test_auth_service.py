import pytest
from app.models.user import User
from app.services.auth_service import AuthService
import io

@pytest.fixture
def usuario_teste(db_setup):
    user = User(
        login="teste123",
        senha="senha123",
        nome="Usuario Teste",
        imagem="/usuarios/teste.png",
        cidade="Cidade Teste",
        telefone="12345678"
    )
    db_setup.session.add(user)
    db_setup.session.commit()
    yield user
    db_setup.session.delete(user)
    db_setup.session.commit()

def test_autenticar_usuario_sucesso(usuario_teste):
    user = AuthService.autenticar_usuario("teste123", "senha123")
    assert user is not None
    assert user.login == "teste123"

def test_autenticar_usuario_falha(usuario_teste):
    user = AuthService.autenticar_usuario("teste123", "senha_errada")
    assert user is None

def test_registrar_usuario_sucesso(db_setup):
    dados = {
        "email": "email@teste.com",
        "senha": "senha123",
        "ra": "novo123",
        "nome": "Novo Usuario",
        "endereco": "Rua Teste",
        "telefone": "987654321"
    }

    class FakeFile:
        filename = "foto.jpg"
        stream = io.BytesIO(b"fake image data")

        def save(self, path):
            with open(path, 'wb') as f:
                f.write(self.stream.read())

    user, erro = AuthService.registrar_usuario(dados, FakeFile())

    assert erro is None
    assert user is not None
    assert user.login == "novo123"
