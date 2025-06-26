


class BaseMemory:
    _instance = None

    memory = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BaseMemory, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # Ensure initialization only happens once
            self._initialized = True


    def get(self, path=None, fields=None):
        """
        General deep get:
        - path: list of keys to reach target dict (default: root)
        - fields: None = all fields, str = one field, list = multiple fields
        """
        current = self.memory
        path = path or []

        # Traverse path
        try:
            for key in path:
                current = current[key]
        except (KeyError, TypeError):
            return None

        # Select fields
        if fields is None:
            return current
        elif isinstance(fields, str):
            return current.get(fields)
        elif isinstance(fields, list):
            return {f: current.get(f) for f in fields}


    def set(self, path=None, value=None):
        if path is None:
            path = []
        elif isinstance(path, str):
            path = [path]

        if not path:
            raise ValueError("Path must contain at least one key to set a value.")

        current = self.memory
        for key in path[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        current[path[-1]] = value