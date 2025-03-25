from waitress import serve
from application import create_app

# from dotenv import load_dotenv

# load_dotenv(dotenv_path='.flaskenv')
app = create_app()

celery_app = app.extensions["celery"]


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
