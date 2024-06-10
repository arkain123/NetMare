import socket


class DNSLookup:
    def __init__(self, host):
        self.host = host

    def run(self):
        try:
            ip = socket.gethostbyname(self.host)
            return {'host': self.host, 'ip': ip}
        except socket.gaierror as e:
            return {'host': self.host, 'error': str(e)}

