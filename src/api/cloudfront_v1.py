from flask import Blueprint
from flask_restx import Api

from .cloudfront.controllers.api import api as request

blueprint = Blueprint('cloudfront_api', __name__, url_prefix='/v1')

api = Api(blueprint,
        doc='/doc/',
        title='Resource API - Cloudfront',
        version='1.0',
        description='A description'
    )

api.add_namespace(request)
