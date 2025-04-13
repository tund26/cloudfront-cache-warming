import os
import redis
import socket
import requests
from celery import shared_task
from http.client import HTTPException

from entity.https import CustomHTTPSConnection

redis_client = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, decode_responses=True)


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
def notify(results, pipeline_url):
    pipeline_urls = pipeline_url.split('/')
    pipeline_id = pipeline_urls[len(pipeline_urls) - 1]
    send_to_mattermost(f"@all\nAll cache warming tasks with pipeline [#{pipeline_id}]({pipeline_url}) completed")


@shared_task(ignore_result=False)
def trigger(results, branch):
    try:
        send_to_mattermost(f"@all\nTrigger deployment to the {branch} branch after the warming tasks completes")
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
        print(response)
    except Exception as e:
        print(f"Error sending notify to mattermost: {e}")
