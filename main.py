#!/usr/bin/env python3

import socket
import yaml
import json
import urllib.request
import urllib
import redis
import sys
from argparse import ArgumentParser
from entity.dns import Dns
from entity.https import CustomHTTPSConnection


redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)


def filter_dict_list(dict_list, condition):
    return list(filter(condition, dict_list))


def resolve_hostname_by_dns_server(hostname, dns_server):
    return Dns(30, 30).resolve(dns_server, hostname)


def is_server_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except Exception as e:
        return False


def resolve(domain):
    
    with open("config/edge_locations.yaml") as f:
        config = yaml.safe_load(f)
    
    results = {}
    for region, countries in config['edge_locations'].items():
        for country, edge_locations in countries.items():
            with urllib.request.urlopen(f'https://public-dns.info/nameserver/{country}.json') as url:
                dns_servers = json.load(url)
            
            dns_servers_stable_list = []
            for edge_location in edge_locations:
                dns_servers_filtered_by_city = filter_dict_list(dns_servers, lambda c: c['city'] == f"{edge_location}")
                
                if not dns_servers_filtered_by_city or len(dns_servers_filtered_by_city) < 2: # too few or no DNS servers, try another way
                    dns_servers_filtered_by_city = filter_dict_list(dns_servers, lambda c: f"{edge_location}".lower() in c['as_org'].lower())
                    print(country, edge_location, dns_servers_filtered_by_city)
                
                for city in dns_servers_filtered_by_city:
                    if is_server_open(city['ip'], 53):
                        try:
                            ips = resolve_hostname_by_dns_server(domain, city['ip'])
                            if not ips:
                                raise Exception(f'Resolve failed when using the dns server.')
                            
                            pops = []
                            for ip in ips:
                                connection = CustomHTTPSConnection(domain, ip)
                                try:
                                    connection.request("GET", '/', headers={"Host": domain})
                                    response = connection.getresponse()
                                    
                                    pop = response.getheader('X-Amz-Cf-Pop')
                                    if pop in pops:
                                        raise Exception(f'same pop {pop}, not necessary')
                                    
                                    key = f"{domain}:{region}:{ip}"
                                    if redis_client.exists(key) == 1:
                                        continue
                                    
                                    pops.append(pop)
                                    redis_client.hset(key, mapping={"pop": pop, "country": country, "city": edge_location, "resolved_by": city['ip']})
                                except Exception as e:
                                    print(e)
                                    pass
                                finally:
                                    connection.close()
                            dns_servers_stable_list.append(city['ip'])
                            break
                        except Exception as e:
                            print(country, edge_location, city['ip'], e)
                            pass
            
            print(country, dns_servers_stable_list)
            if (len(dns_servers_stable_list) > 0):
                results[country] = dns_servers_stable_list
            
    with open('config.yml', 'w') as cf:
        yaml.dump(results, cf, default_flow_style=False)


if __name__ == '__main__':
    
    parser = ArgumentParser(description="A script that requires a domain option.")

    parser.add_argument(
        '--domain',
        type=str,
        required=True,
        action='append',
        help='The domain to process. Can be specified multiple times (e.g., --domain=d2war8dgdphhhw.cloudfront.net --domain=mek2s8dgdpieoa.cloudfront.net).'
    )

    args = parser.parse_args()

    for domain in args.domain:
        if not domain or not is_server_open(domain, 443):
            sys.exit('Domain value is invalid!')
        resolve(domain)
