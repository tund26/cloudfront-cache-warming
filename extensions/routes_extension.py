from src.api.cloudfront_v1 import blueprint as cloudfront_api


def register_routes(app):
    """
    Register routes with blueprint and namespace
    """
    app.register_blueprint(cloudfront_api)
