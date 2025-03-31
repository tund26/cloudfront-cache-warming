
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
