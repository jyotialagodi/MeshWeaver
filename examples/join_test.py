import socket
import json

from meshweaver.peer import generate_node_id


def join_node(target_host, target_port, local_host, local_port):

    node_id = generate_node_id(
        local_host,
        local_port
    )

    message = {
        "type": "JOIN",
        "node_id": node_id,
        "host": local_host,
        "port": local_port
    }

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    sock.settimeout(5)

    try:

        print(
            f"Joining mesh through "
            f"{target_host}:{target_port}"
        )

        sock.sendto(
            json.dumps(message).encode(),
            (target_host, target_port)
        )

        data, address = sock.recvfrom(4096)

        response = json.loads(
            data.decode()
        )

        print(
            f"Response received from {address}"
        )

        print(
            "Message type:",
            response["type"]
        )

        print(
            "Known peers:",
            len(response["peers"])
        )

    except socket.timeout:

        print("No response received.")

    finally:

        sock.close()


if __name__ == "__main__":

    join_node(
        "127.0.0.1",
        9002,
        "127.0.0.1",
        9003
    )