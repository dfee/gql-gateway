from functools import wraps

from promise import Promise
from promise.dataloader import DataLoader


def wrap_promise(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return Promise.resolve(f(*args, **kwargs))

    return wrapper


def unwrap_promise(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        rv = f(*args, **kwargs).get()
        return rv.get() if isinstance(rv, Promise) else rv

    return wrapper
