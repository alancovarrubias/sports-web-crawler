SPORTS = ['NBA', 'MLB']
KEYS = {
    'NBA': {
        'Team': ['sport', 'season'],
        'Player': ['sport', 'season', 'team'],
        'Game': ['sport', 'season'],
        'Stat': []
    },
    'MLB': {
        'Team': ['sport', 'season'],
        'Player': ['sport', 'season', 'team'],
        'Game': ['sport', 'season', 'teams'],
        'Stat': []
    }
}


class Datastore:
    def __init__(self, model):
        self.model = model
        self.datastore = {}

    def validate_args(self, args):
        if args['sport'] not in SPORTS:
            return False
        keys = self.required_keys(args)
        args = {k: v for k, v in args.items() if v is not None}
        arg_keys = list(args.keys())
        for key in keys:
            if key not in arg_keys:
                return False
        return True

    def required_keys(self, args):
        return KEYS[args['sport']][self.model]

    def get(self, args):
        data = self.datastore
        keys = self.required_keys(args)
        for key in keys:
            arg_key = args[key]
            data = data[arg_key]
        return data

    def set(self, args, data):
        datastore = self.datastore
        keys = self.required_keys(args)
        for key in keys:
            arg_key = args[key]
            if key == keys[-1]:
                datastore[arg_key] = data
            elif arg_key not in datastore:
                datastore[arg_key] = {}
            datastore = datastore[arg_key]

    def exists(self, args):
        datastore = self.datastore
        keys = self.required_keys(args)
        for key in keys:
            arg_key = args[key]
            if arg_key not in datastore:
                return False
            datastore = datastore[arg_key]
        return True
