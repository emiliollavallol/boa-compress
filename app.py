from app import create_app  # Importa la función create_app de app/__init__.py

app = create_app()  # Crea la aplicación Flask

if __name__ == '__main__':
    app.run(debug=True)  # Ejecuta el servidor si este archivo se ejecuta directamente
