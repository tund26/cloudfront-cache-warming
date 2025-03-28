
import socket
from http.client import HTTPException
from celery import shared_task
from entity.https import CustomHTTPSConnection


@shared_task(ignore_result=False)
def send_request_with_paths(hostname, ip, paths):    
    results = []
    for path in paths:
        connection = CustomHTTPSConnection(hostname, ip)
        connection.timeout = 10
        headers = {"Host": hostname}
        
        try:
            print(f'requesting to: https://{hostname}{path} using ip {ip}')
            connection.request("GET", path, headers=headers)
            response = connection.getresponse()
            
            status = response.status
            xpop = response.getheader('X-Amz-Cf-Pop')
            xcache = response.getheader('X-Cache')
            
            results.append({path: status, 'x-cache': xcache, 'x-amz-cf-pop': xpop})
            print('.', end='', flush=True)
        except socket.timeout:
            results.append({path: 'timeout'})
        except HTTPException as e:
            results.append({path: f'HTTP error: {str(e)}'})
        except Exception as e:
            results.append({path: f'error: {str(e)}'})
        finally:
            connection.close()
            
    return results
