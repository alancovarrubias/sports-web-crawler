from constant import NBA, MLB, TEAM, PLAYER, GAME, STAT, SPORTS
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
        sport = args['sport']
        self.required_keys = KEYS[sport][resource_type]
        arg_items = {k: v for k, v in args.items() if v is not None}
        self.arg_keys = list(arg_items.keys())
        self.arg_values = list(arg_items.values())

