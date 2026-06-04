from app import create_app
from app.database.db import crear_tablas

app = create_app()

crear_tablas()

if __name__ == "__main__":
    app.run(debug=True)