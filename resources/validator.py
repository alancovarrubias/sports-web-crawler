from const.sports import SPORTS
def validate_args(key_store):
    if key_store.sport is None or key_store.sport not in SPORTS:
        return False, 'Missing sports argument'
    for key in key_store.required_keys:
        if key not in key_store.args.keys():
            return False, f'Required arguments {key_store.required_keys}'
    return True, None

class Validator:
    def __init__(self, key_store):
        self.valid, self.error_message = validate_args(key_store)
