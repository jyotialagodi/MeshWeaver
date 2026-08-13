from dataclasses import dataclass
import hashlib


def generate_node_id(host, port):
    value = f"{host}:{port}".encode()

    return hashlib.sha1(value).hexdigest()


@dataclass
class Peer:
    node_id: str
    host: str
    port: int

    def address(self):
        return f"{self.host}:{self.port}"