import os
import yaml
import redis
import re
from flask import request, jsonify
from celery import chord, group

from flask_restx import Namespace, Resource
from flask import request
from src.tasks.task import *

from extensions.log_extension import get_logger

api = Namespace('cloudfront', description='Request Endpoints')
logger = get_logger(__name__)

redis_client = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, decode_responses=True)


@api.route('/cache')
class Cache(Resource):
    @api.doc('Warm-up Cloudfront Requests')
    def post(self):
        if not dict(request.json):
            return jsonify(message="Data is invalid"), 400

        payload = request.json
        try:            
            with open("config/edge_locations.yaml") as f:
                edge_locations = yaml.safe_load(f)['edge_locations']
                
            ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
            chunk_size = os.environ.get('CHUNK_SIZE')
            if not chunk_size:
                raise Exception('CHUNK_SIZE is None')
            
            warming_tasks = []
            for region in edge_locations:
                keys = redis_client.keys(f"{payload['domain']}:{region}:*")
                if not keys:
                    continue
                
                for key, paths in ((key, paths) for key in keys for paths in batch(payload['paths'], int(chunk_size))):
                    valid_paths = filter_valid_paths(key, paths)
                    if not valid_paths:
                        continue
                    
                    ip = ip_pattern.search(key)[0]
                    if not ip:
                        continue

                    task = send_request_with_paths.s(payload['domain'], ip, paths)
                    warming_tasks.append(task)

            chord(warming_tasks)(trigger.s(pipeline_url=payload['pipeline_url'], project_id=payload['project_id']))
            return jsonify({"status": "started"})
        except Exception as e:
            print(e)
            return jsonify(message=f"Internal server error"), 500


def filter_valid_paths(key, paths) -> list:
    data = []
    for path in paths:
        pop = redis_client.hget(key, 'pop')
        cache_key = f'cache:{path}:{pop}'
        if redis_client.getbit(cache_key, 1) == 1:
            print(f'This path has previously failed at {pop}: {path}')
            continue

        if redis_client.getbit(cache_key, 0) == 1:
            print(f'This path has previously cached at {pop}: {path}')
            continue

        data.append(path)
    return data


def batch(iterable, n=1):
    _l = len(iterable)
    for ndx in range(0, _l, n):
        yield iterable[ndx:min(ndx + n, _l)]
