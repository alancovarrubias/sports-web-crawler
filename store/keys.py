from const.sports import NBA, MLB, SPORTS
from const.models import TEAM, PLAYER, GAME, STAT

KEYS = {
    NBA: {
        TEAM: ['sport', 'season'],
        PLAYER: ['sport', 'season', 'team'],
        GAME: ['sport', 'season'],
        STAT: ['sport', 'game_url', 'home_team', 'away_team']
    },
    MLB: {
        TEAM: ['sport', 'season'],
        PLAYER: ['sport', 'season', 'team'],
        GAME: ['sport', 'season', 'teams'],
        STAT: ['sport', 'game_url', 'home_team', 'away_team']
    }
}


class KeyStore:
    def __init__(self, resource_type, args):
        self.resource_type = resource_type
        self.sport = args['sport']
        self.required_keys = KEYS[self.sport][self.resource_type]
        self.args = {k: v for k, v in args.items() if v is not None}
        self.valid, self.error_message = self.validate_args()


    def validate_args(self):
        if self.sport is None or self.sport not in SPORTS:
            return False, 'Missing sports argument'
        for key in self.required_keys:
            if key not in self.args.keys():
                return False, f'Required arguments {self.required_keys}'
        return True, None