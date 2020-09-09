from key_store import KeyStore
import os
import json

def get_file_path(resource_type, args):
    key_store = KeyStore(resource_type, args)
    os.makedirs(resource_type, exist_ok=True)
    file_name = ''.join(map(str, key_store.arg_values))
    return os.path.join(resource_type, file_name)

class FileManager:
    def __init__(self, resource_type, key_store):
        self.path = get_file_path(resource_type, key_store)
    
    def file_exists(self):
        return os.path.isfile(self.path)

    def save_json(self, content):
        with open(self.path, 'w') as file:
            json.dump(content, file)

    def read_json(self):
        with open(self.path, 'r') as file:
            return json.load(file)
