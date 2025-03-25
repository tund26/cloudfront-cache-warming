import dns.resolver

class Dns:
    def __init__(self, timeout=10.0, lifetime=10.0):
        self.dns_cache = {}
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = lifetime

    def resolve(self, nameserver, host):
        if nameserver not in self.dns_cache:
            self.dns_cache[nameserver] = {}

        if host not in self.dns_cache[nameserver]:
            self.resolver.nameservers = [nameserver]
            ips = []
            try:
                answers = self.resolver.resolve(host, 'A')
                ips.extend([str(ip) for ip in answers])
            except dns.resolver.NoAnswer as e:
                print(e)
                pass
            except dns.resolver.NoNameservers as e:
                print(e)
                pass
            except dns.resolver.LifetimeTimeout as e:
                print(e)
                pass

            self.dns_cache[nameserver][host] = ips

        return self.dns_cache[nameserver][host]
