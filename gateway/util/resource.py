import pkgutil


def load_resource(mod_name, resource: str) -> str:
    data = pkgutil.get_data(mod_name, resource)
    if data is None:
        raise TypeError(
            f"TypeGuard: couldn't resolve {resource} relative to {mod_name}"
        )
    return data.decode("utf-8")
