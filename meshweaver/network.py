import asyncio
import json
import sys

from meshweaver.peer import Peer, generate_node_id
from meshweaver.routing_table import RoutingTable


class DiscoveryProtocol(asyncio.DatagramProtocol):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.node_id = generate_node_id(host, port)

        self.routing_table = RoutingTable(self.node_id)

        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        print("\nMeshWeaver node started")
        print(f"Node ID: {self.node_id}")
        print(f"Listening on {self.host}:{self.port}")

    def datagram_received(self, data, addr):
        try:
            message = json.loads(data.decode())

            message_type = message.get("type")

            if message_type == "JOIN":
                self.handle_join(message, addr)

            elif message_type == "PEER_LIST":
                self.handle_peer_list(message)

            elif message_type == "PING":
                self.handle_ping(addr)

        except Exception as error:
            print(f"Message error: {error}")

    def handle_join(self, message, addr):

        peer = Peer(
            node_id=message["node_id"],
            host=message["host"],
            port=message["port"]
        )

        self.routing_table.add_peer(peer)

        print(f"\nPeer joined: {peer.address()}")
        print(f"Known peers: {self.routing_table.peer_count()}")

        peers = []

        for known_peer in self.routing_table.get_all_peers():
            peers.append({
                "node_id": known_peer.node_id,
                "host": known_peer.host,
                "port": known_peer.port
            })

        response = {
            "type": "PEER_LIST",
            "peers": peers
        }

        self.transport.sendto(
            json.dumps(response).encode(),
            addr
        )

    def handle_peer_list(self, message):

        peers = message.get("peers", [])

        for peer_data in peers:

            peer = Peer(
                node_id=peer_data["node_id"],
                host=peer_data["host"],
                port=peer_data["port"]
            )

            self.routing_table.add_peer(peer)

        print("\nPeer discovery completed.")
        print(f"Known peers: {self.routing_table.peer_count()}")

        for peer in self.routing_table.get_all_peers():
            print(
                f"  {peer.node_id[:8]}... "
                f"{peer.address()}"
            )

    def handle_ping(self, addr):

        self.transport.sendto(
            b"PONG",
            addr
        )

        print(f"PING received from {addr}")
        print(f"PONG sent to {addr}")


async def start_discovery_node(host="127.0.0.1", port=9002):

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: DiscoveryProtocol(host, port),
        local_addr=(host, port)
    )

    try:
        await asyncio.Future()

    finally:
        transport.close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9002

    asyncio.run(
        start_discovery_node(
            host="127.0.0.1",
            port=port
        )
    )