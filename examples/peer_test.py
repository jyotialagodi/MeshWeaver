from meshweaver.peer import Peer, generate_node_id


host = "127.0.0.1"
port = 9001

node_id = generate_node_id(host, port)

peer = Peer(
    node_id=node_id,
    host=host,
    port=port
)

print("Node ID:", peer.node_id)
print("Address:", peer.address())