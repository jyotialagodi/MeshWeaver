from meshweaver.peer import Peer, generate_node_id
from meshweaver.routing_table import RoutingTable


local_host = "127.0.0.1"
local_port = 9001

local_node_id = generate_node_id(
    local_host,
    local_port
)

routing_table = RoutingTable(local_node_id)

peer1 = Peer(
    node_id=generate_node_id("127.0.0.1", 9002),
    host="127.0.0.1",
    port=9002
)

peer2 = Peer(
    node_id=generate_node_id("127.0.0.1", 9003),
    host="127.0.0.1",
    port=9003
)

routing_table.add_peer(peer1)
routing_table.add_peer(peer2)

print("Local Node ID:", local_node_id)
print("Number of peers:", routing_table.peer_count())

print("\nKnown Peers:")

for peer in routing_table.get_all_peers():
    print(
        f"Node ID: {peer.node_id} | "
        f"Address: {peer.address()}"
    )