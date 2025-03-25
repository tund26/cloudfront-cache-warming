import http.client
import socket

class CustomHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, ip, port=443, **kwargs):
        self.ip = ip
        super().__init__(host, port, **kwargs)

    def connect(self):
        self.sock = socket.create_connection((self.ip, self.port), self.timeout)
        if self._tunnel_host:
            self._tunnel()

        self.sock = self._context.wrap_socket(self.sock, server_hostname=self.host)
