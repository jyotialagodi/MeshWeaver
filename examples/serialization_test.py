from meshweaver.serializer import serialize_task, deserialize_task


def add_numbers(a, b):
    return a + b


print("Creating task...")

data = serialize_task(add_numbers, 10, 20)

print("Task serialized successfully.")
print("Serialized size:", len(data), "bytes")

task = deserialize_task(data)

function = task["function"]
args = task["args"]
kwargs = task["kwargs"]

result = function(*args, **kwargs)

print("Function:", function.__name__)
print("Arguments:", args)
print("Result:", result)