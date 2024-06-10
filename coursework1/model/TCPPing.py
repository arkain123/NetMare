import socket
import time


class TCPPing:
    def __init__(self, host, port, timeout=1):
        self.host = host
        self.port = int(port)
        self.timeout = float(timeout)

    def run(self):
        start_time = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.host, self.port))
            sock.close()
            end_time = time.time()
            return {'host': self.host, 'port': self.port, 'status': 'open', 'response_time': (end_time - start_time) * 1000}
        except socket.timeout:
            return {'host': self.host, 'port': self.port, 'status': 'closed', 'response_time': None}
        except Exception as e:
            return {'host': self.host, 'port': self.port, 'status': 'error', 'response_time': None, 'error': str(e)}
