from app import app
from waitress import serve

if __name__ == "__main__":
    app.run()
    # serve(app, port=8080)
