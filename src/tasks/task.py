import os
import redis
import socket
import requests
import json
from celery import shared_task
from http.client import HTTPException

from entity.https import CustomHTTPSConnection

redis_client = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, decode_responses=True)
api_url = os.environ.get('GITLAB_PROJECT_API_URL')


@shared_task(ignore_result=False)
def send_request_with_paths(hostname, ip, paths):
    results = []
    for path in paths:
        connection = CustomHTTPSConnection(hostname, ip)
        connection.timeout = 10
        headers = {"Host": hostname}
        
        try:
            print(f'GET: https://{hostname}{path} using ip {ip}')
            connection.request("GET", path, headers=headers)
            response = connection.getresponse()
            
            status = response.status
            x_pop = response.getheader('X-Amz-Cf-Pop')
            x_cache = response.getheader('X-Cache').lower()
            
            results.append({path: status, 'x-cache': x_cache, 'x-amz-cf-pop': x_pop})
            
            cache_key = f'cache:{path}:{x_pop}'
            if 'error' in x_cache:
                redis_client.setbit(cache_key, 1, 1)
            elif 'hit' in x_cache or 'miss' in x_cache:  # bundle file with same name after build, cache for 1 hour
                redis_client.setbit(cache_key, 0, 1)
            else:
                print(f'other state: {x_cache}')
                pass
            
            if redis_client.exists(cache_key) == 1:
                redis_client.expire(cache_key, 3600)
                
        except socket.timeout:
            results.append({path: 'timeout'})
        except HTTPException as e:
            results.append({path: f'HTTP error: {str(e)}'})
        except Exception as e:
            results.append({path: f'error: {str(e)}'})
        finally:
            connection.close()
            
    return results


@shared_task(ignore_result=False)
def trigger(results, pipeline_url, project_id):
    try:
        pipeline_id = get_pipeline_id_in_url(pipeline_url)
        job_id = get_deploy_job_id(project_id, pipeline_id)
        if not job_id:
            raise Exception("Deploy job id not found")
        
        # Trigger deploy job on stage deploy_cache
        headers = {
            "PRIVATE-TOKEN": os.environ.get('GITLAB_PRIVATE_TOKEN')
        }
        response = requests.post(f"{api_url}/{project_id}/jobs/{job_id}/play", headers=headers)
        data = json.loads(response.text)
        if not data:
            raise Exception(f'Send trigger job failed with job_id = {job_id}')
        
        send_to_mattermost(f"@all\nAll cache warming tasks with pipeline [#{pipeline_id}]({pipeline_url}) completed\nTriggerred the job [#{job_id}]({data['web_url']}): :rocket: - {data['status'].upper()}")
        return data
    except Exception as e:
        print(f"Error triggering webhook: {e}")


def send_to_mattermost(message):
    payload = {
        "channel_id": os.environ.get('NOTIFY_CHANNEL_ID'),
        "message": message
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('NOTIFY_API_TOKEN')}"
    }
    try:
        response = requests.post(os.environ.get("NOTIFY_API_ENDPOINT"), json=payload, headers=headers)
        return response.text
    except Exception as e:
        print(f"Error sending notify to mattermost: {e}")


def get_pipeline_id_in_url(pipeline_url) -> str:
    pipeline_lst = pipeline_url.split('/')
    return pipeline_lst[len(pipeline_lst) - 1]


def get_deploy_job_id(project_id, pipeline_id):
    headers = {
        "PRIVATE-TOKEN": os.environ.get('GITLAB_PRIVATE_TOKEN')
    }
    try:
        jobs = requests.get(f"{api_url}/{project_id}/pipelines/{pipeline_id}/jobs", headers=headers)
        data = json.loads(jobs.text)
        id = None
        for job in data:
            if job['stage'] == 'deploy_cache' and job['status'] == 'manual':
                id = job['id']
                break
        return id
    except Exception as e:
        print(e)
        return None
