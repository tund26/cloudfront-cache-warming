def register_tasks(celery):
    from src.tasks.task import send_request_with_paths
    