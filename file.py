import json


class File:
    def __init__(self, path):
        self.path = path

    def save_json(self, content):
        with open(self.path, 'w') as file:
            json.dump(content, file)

    def read_json(self):
        with open(self.path, 'r') as file:
            return json.load(file)
