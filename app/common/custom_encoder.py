from collections.abc import MutableMapping
import json

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MutableMapping):
            return dict(obj)
        return super().default(obj)
