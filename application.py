from flask import Flask

from celery import Celery, Task

from extensions.routes_extension import register_routes
from extensions.tasks_extension import register_tasks


def celery_init(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.name, task_cls=FlaskTask)
    celery.config_from_object(app.config["CELERY"])
    celery.set_default()
    
    # celery.conf.task_default_exchange = 'broadcast'
    # celery.conf.task_default_routing_key = 'broadcast'
    
    app.extensions["celery"] = celery
    return celery


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis",
            result_backend="redis://redis",
            task_ignore_result=True,
            task_serializer = 'json',
            result_serializer = 'json',
            accept_content = ['json']
        ),
    )
    
    app.config.from_prefixed_env()
    celery_init(app)
    
    register_routes(app)
    register_tasks(app.extensions["celery"])
    
    return app
