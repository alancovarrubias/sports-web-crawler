import os
import json

FILES_FOLDER = 'files'

def get_file_path(key_store):
    os.makedirs(FILES_FOLDER, exist_ok=True)
    resource_folder = os.path.join(FILES_FOLDER, key_store.resource_type)
    os.makedirs(resource_folder, exist_ok=True)
    file_name = ''.join(map(str, key_store.args.values()))
    return os.path.join(resource_folder, file_name)

class FileManager:
    def __init__(self, key_store):
        self.path = get_file_path(key_store)
    
    def file_exists(self):
        return os.path.isfile(self.path)

    def save_json(self, content):
        with open(self.path, 'w') as file:
            json.dump(content, file)

    def read_json(self):
        with open(self.path, 'r') as file:
            return json.load(file)
