from app import create_app

app = create_app()

if __name__ == '__main__':
    # Executa o servidor Flask em modo debug para facilitar o desenvolvimento
    app.run(host='0.0.0.0', port=5000, debug=True)
