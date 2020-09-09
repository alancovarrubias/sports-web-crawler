from validator import Validator
from data_store import DataStore
class Resources:
    def __init__(self, resource_type, args):
        self.valid = True
        self.validator = Validator(resource_type, args)
        self.data_store = DataStore(resource_type, args)

    def get(self):
        resource = self.data_store.get_resource()
        return resource