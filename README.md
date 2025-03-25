### A script for warming up cloudfront caches

Config

In the `config.yaml` file we have listed the DNS servers in https://public-dns.info

```yaml
...
ae:
- 217.164.255.37
bh:
- 87.252.99.92
il:
- 82.80.219.220
ke:
- 197.155.92.21
ng:
- 197.253.36.34
om:
- 85.154.37.161
za:
- 105.243.178.87
- 41.23.184.151
...

```

How to use

Generate `config.yaml` and save public ip resolved to redis

```sh
python3 main.py --domain=dom3z7ncawedu.cloudfront.net
```

Launch your workers

```sh
celery -A run.celery_app worker --loglevel INFO
```


```sh
curl -X POST -H "Content-Type: application/json" -d '{"domain": "dom3z7ncawedu.cloudfront.net", "paths": ["/SamplePNGImage_100kbmb.png"]}' http://localhost:5000/pre-warm
```

Outputs

```
................................
country is fi: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.173.5.122
country is fi: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.173.5.45
country is fi: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.173.5.71
country is fi: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.173.5.95
country is pt: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 3.160.132.121
country is pt: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 3.160.132.62
country is pt: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 3.160.132.43
country is pt: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 3.160.132.97
country is gb: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.236.108
country is gb: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.236.112
country is gb: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.18.92
country is gb: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.236.32
country is gb: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.236.88
country is gb: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.18.45
country is gb: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.18.57
country is gb: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.18.123
country is es: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.224.115.31
country is es: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.224.115.93
country is es: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.224.115.76
country is es: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.224.115.120
country is fr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 3.160.188.35
country is fr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 3.160.188.113
country is fr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.236.112
country is fr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.236.108
country is fr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 3.160.188.122
country is fr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 3.160.188.121
country is fr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.236.32
country is fr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.236.88
country is it: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 108.156.2.87
country is it: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 108.156.2.59
country is it: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 108.156.2.16
country is it: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 108.156.2.49
country is no: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.165.140.97
country is no: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.165.140.84
country is no: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.165.140.123
country is no: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.165.140.65
country is cz: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 65.9.95.101
country is cz: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 65.9.95.20
country is cz: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 65.9.95.50
country is cz: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 65.9.95.97
country is bg: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.32.110.107
country is bg: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.32.110.104
country is bg: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.32.110.96
country is bg: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.32.110.27
country is se: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.18.57
country is se: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.18.92
country is se: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.18.123
country is se: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.239.18.45
country is at: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.32.110.107
country is at: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.32.110.104
country is at: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.32.110.96
country is at: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 13.32.110.27
country is pl: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.244.146.50
country is pl: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.244.146.26
country is pl: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.244.146.25
country is pl: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 18.244.146.5
country is hr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 65.9.189.79
country is hr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 65.9.189.59
country is hr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 65.9.189.56
country is hr: dom3z7ncawedu.cloudfront.net returned [{'/SamplePNGImage_100kbmb.png': 200, 'x-cache': 'Miss from cloudfront'}] from 65.9.189.81
```
