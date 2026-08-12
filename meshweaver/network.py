import asyncio

from meshweaver.serializer import deserialize_task


class TaskProtocol(asyncio.DatagramProtocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

        address = transport.get_extra_info("sockname")

        print("Task receiver started")
        print(f"Listening on {address[0]}:{address[1]}")

    def datagram_received(self, data, addr):
        print(f"\nTask received from {addr}")

        try:
            task = deserialize_task(data)

            function = task["function"]
            args = task["args"]
            kwargs = task["kwargs"]

            print(f"Executing function: {function.__name__}")
            print(f"Arguments: {args}")

            result = function(*args, **kwargs)

            print(f"Result: {result}")

            response = str(result).encode()

            self.transport.sendto(response, addr)

            print(f"Result sent back to {addr}")

        except Exception as error:
            print(f"Task execution failed: {error}")

            response = f"ERROR: {error}".encode()

            self.transport.sendto(response, addr)


async def start_task_receiver(host="127.0.0.1", port=9002):

    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: TaskProtocol(),
        local_addr=(host, port)
    )

    try:
        await asyncio.Future()
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(start_task_receiver())