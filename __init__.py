from application import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

__all__ = ['celery_app']
