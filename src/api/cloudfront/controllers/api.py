import yaml
import redis
import json
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
        
        print(request.json)
        if not dict(request.json):
            return jsonify(message="Data is invalid"), 400
        
        try:
            with open("config/edge_locations.yaml") as f:
                edge_locations = yaml.safe_load(f)['edge_locations']
            
            for region, country in ((region, country) for region in edge_locations for country in edge_locations[region]):
                dataset = redis_client.smembers(f"{request.json['domain']}:{region}:{country}")
                print(dataset)
                if len(dataset) == 0:
                    continue
                
                print(dataset)
                for ip in dataset:
                    # results.append(send_request_with_paths.delay(request.json['domain'], ip, request.json['paths']))
                    send_request_with_paths.apply_async(args=(request.json['domain'], ip, request.json['paths']))
                    # tasks.append(task)
                    # print(task.get(on_message=on_raw_message, propagate=False))
            
            # for task in tasks:
            #     print(task.get(on_message=on_raw_message, propagate=False))
            
            return jsonify(message="success")
        except Exception as e:
            print(e)
            return jsonify(message=f"Internal server error"), 500


def on_raw_message(body):
    print(body)
