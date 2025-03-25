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
