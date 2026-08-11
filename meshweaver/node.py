import asyncio
import sys


class MeshNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def start(self):
        print("MeshWeaver node started")
        print(f"Listening on {self.host}:{self.port}")

        loop = asyncio.get_running_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: NodeProtocol(self),
            local_addr=(self.host, self.port)
        )

        try:
            await asyncio.Future()
        finally:
            transport.close()


class NodeProtocol(asyncio.DatagramProtocol):

    def __init__(self, node):
        self.node = node
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()

        print(f"Received from {addr}: {message}")

        if message == "PING":
            self.transport.sendto(b"PONG", addr)
            print(f"Sent PONG to {addr}")


async def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9001

    node = MeshNode("127.0.0.1", port)
    await node.start()


if __name__ == "__main__":
    asyncio.run(main())