import socket

from meshweaver.serializer import serialize_task


def add_numbers(a, b):
    return a + b


def send_task(host, port):
    print(f"Sending task to {host}:{port}")

    data = serialize_task(add_numbers, 10, 20)

    print("Task serialized successfully.")
    print("Sending task...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.settimeout(5)

    try:
        sock.sendto(data, (host, port))

        response, address = sock.recvfrom(4096)

        result = response.decode()

        print(f"Response from {address}: {result}")

    except socket.timeout:
        print("No response received from the node.")

    finally:
        sock.close()


if __name__ == "__main__":
    send_task("127.0.0.1", 9002)