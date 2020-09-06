from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from scrapers import ScraperFactory
from nested_mem_cache import NestedMemCache

app = Flask(__name__)
api = Api(app)
scraper_factory = ScraperFactory()


def abort_if_keys_dont_exist(args, keys):
    args = {k: v for k, v in args.items() if v is not None}
    arg_keys = list(args.keys())
    for key in keys:
        if key not in arg_keys:
            abort(404, message="Required arguments %s" % keys)


parser = reqparse.RequestParser()
parser.add_argument('sport', type=str, location='args')
parser.add_argument('season', type=int, location='args')
parser.add_argument('team', type=str, location='args')
parser.add_argument('game_url', type=str, location='args')
parser.add_argument('away_team', type=str, location='args')
parser.add_argument('home_team', type=str, location='args')

TEAMS = NestedMemCache(['sport', 'season'])


class TeamResource(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, TEAMS.keys)
        if TEAMS.check(args):
            return TEAMS.get(args)

        scraper = scraper_factory.get_scraper(args['sport'])
        teams = scraper.get_teams(args)
        TEAMS.set(args, teams)
        return teams


PLAYERS = NestedMemCache(['sport', 'season', 'team'])


class PlayerResource(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, PLAYERS.keys)
        if PLAYERS.check(args):
            return PLAYERS.get(args)

        scraper = scraper_factory.get_scraper(args['sport'])
        teams = scraper.get_teams(args)
        PLAYERS.set(args, teams)
        return teams


GAMES = NestedMemCache(['sport', 'season'])


class GameResource(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, GAMES.keys)

        if GAMES.check(args):
            return GAMES.get(args)

        scraper = scraper_factory.get_scraper(args['sport'])
        games = scraper.get_games(args)
        GAMES.set(args, games)
        return games


STATS = NestedMemCache(['sport', 'game_url', 'home_team', 'away_team'])


class StatResource(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, GAMES.keys)

        if STATS.check(args):
            return STATS.get(args)

        scraper = scraper_factory.get_scraper(args['sport'])
        stats = scraper.get_stats(args)
        STATS.set(args, stats)
        return stats


##
# Actually setup the Api resource routing here
##
api.add_resource(TeamResource, '/teams')
api.add_resource(PlayerResource, '/players')
api.add_resource(GameResource, '/games')
api.add_resource(StatResource, '/stats')


if __name__ == '__main__':
    app.run(debug=True)
