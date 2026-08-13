class RoutingTable:
    def __init__(self, local_node_id):
        self.local_node_id = local_node_id
        self.peers = {}

    def add_peer(self, peer):
        if peer.node_id == self.local_node_id:
            return

        self.peers[peer.node_id] = peer

    def remove_peer(self, node_id):
        self.peers.pop(node_id, None)

    def get_peer(self, node_id):
        return self.peers.get(node_id)

    def get_all_peers(self):
        return list(self.peers.values())

    def peer_count(self):
        return len(self.peers)