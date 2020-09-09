from constants.sports import SPORTS
from key_store import KeyStore


class Validator:
    def __init__(self, resource_type, args):
        self.sport = args['sport']
        self.key_store = KeyStore(resource_type, args)
        self.valid = self.validate_args()

    def validate_args(self):
        if self.sport is None or self.sport not in SPORTS:
            self.error_message = 'Missing sports argument'
            return False
        for key in self.key_store.required_keys:
            if key not in self.key_store.arg_keys:
                self.error_message = f'Required arguments {self.key_store.required_keys}'
                return False
        return True