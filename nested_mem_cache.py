class NestedMemCache:
    def __init__(self, keys):
        self.keys = keys
        self.datastore = {}

    def get(self, args):
        data = self.datastore
        for key in self.keys:
            arg_key = args[key]
            data = data[arg_key]
        return data

    def set(self, args, data):
        datastore = self.datastore
        for key in self.keys:
            arg_key = args[key]
            if key == self.keys[-1]:
                datastore[arg_key] = data
            elif arg_key not in datastore:
                datastore[arg_key] = {}
            datastore = datastore[arg_key]

    def check(self, args):
        datastore = self.datastore
        for key in self.keys:
            arg_key = args[key]
            if arg_key not in datastore:
                return False
            datastore = datastore[arg_key]
        return True
