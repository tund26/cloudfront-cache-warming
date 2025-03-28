import yaml
import redis
import re
from flask import request, jsonify

from flask_restx import Namespace, Resource
from flask import request
from src.tasks.task import *

from extensions.log_extension import get_logger

api = Namespace('cloudfront', description='Request Endpoints')
logger = get_logger(__name__)

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)


@api.route('/cache')
class Cache(Resource):
    @api.doc('Warm-up Cloudfront Requests')
    def post(self):
        if not dict(request.json):
            return jsonify(message="Data is invalid"), 400
        
        chunk_size = 5
        try:
            with open("config/edge_locations.yaml") as f:
                edge_locations = yaml.safe_load(f)['edge_locations']
                
            ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            for region in edge_locations:
                keys = redis_client.keys(f"{request.json['domain']}:{region}:*")
                if not keys:
                    continue
                
                for key, paths in ((key, paths) for key in keys for paths in batch(request.json['paths'], chunk_size)):
                    ip = ip_pattern.search(key)[0]
                    if not ip:
                        continue
                    
                    send_request_with_paths.apply_async(args=(request.json['domain'], ip, paths))
                    
            return jsonify(message="success")
        except Exception as e:
            print(e)
            return jsonify(message=f"Internal server error"), 500


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def on_raw_message(body):
    print(body)
