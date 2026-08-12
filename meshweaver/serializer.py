import cloudpickle


def serialize_task(function, *args, **kwargs):
    task = {
        "function": function,
        "args": args,
        "kwargs": kwargs
    }

    return cloudpickle.dumps(task)


def deserialize_task(data):
    return cloudpickle.loads(data)