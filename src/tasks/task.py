
import redis
import socket
from celery import shared_task
from http.client import HTTPException

from entity.https import CustomHTTPSConnection

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)


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
            print('.', end='', flush=True)
            
            if 'error' in x_cache:
                redis_client.hset(f'error:{path}:{x_pop}', mapping={'status': status, 'state': x_cache})
                redis_client.expire(f'error:{path}:{x_pop}', 1800)
            elif 'hit' in x_cache or 'miss' in x_cache:  # bundle file with same name after build, cache for 1 hour
                redis_client.hset(f'cache:{path}:{x_pop}', mapping={'status': status, 'state': x_cache})
                redis_client.expire(f'cache:{path}:{x_pop}', 3600)
            else:
                print(f'other state: {x_cache}')
                pass
        except socket.timeout:
            results.append({path: 'timeout'})
        except HTTPException as e:
            results.append({path: f'HTTP error: {str(e)}'})
        except Exception as e:
            results.append({path: f'error: {str(e)}'})
        finally:
            connection.close()
            
    return results
