from constants.sports import SPORTS
from key_store import KeyStore


class Validator:
    def __init__(self, key_store):
        self.required_keys = key_store.required_keys
        self.arg_keys = key_store.args.keys()
        self.sport = key_store.sport

    def validate_args(self):
        if self.sport is None or self.sport not in SPORTS:
            self.error_message = 'Missing sports argument'
            return False
        for key in self.required_keys:
            if key not in self.arg_keys:
                self.error_message = f'Required arguments {self.required_keys}'
                return False
        return True