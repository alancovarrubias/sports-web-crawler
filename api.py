from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from scrapers import ScraperFactory

app = Flask(__name__)
api = Api(app)
scraper_factory = ScraperFactory()


def abort_if_keys_dont_exist(args, keys):
    args = {k: v for k, v in args.items() if v is not None}
    arg_keys = list(args.keys())
    for key in keys:
        if key not in arg_keys:
            abort(404, message="Missing key %s" % keys)


parser = reqparse.RequestParser()
parser.add_argument('season', type=int, location='args')
parser.add_argument('team', type=str, location='args')
parser.add_argument('game_url', type=str, location='args')
parser.add_argument('away_team', type=str, location='args')
parser.add_argument('home_team', type=str, location='args')

# TeamList
TEAMS = {}


class TeamList(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, ['season'])
        season = args['season']
        if TEAMS.get(season):
            return TEAMS[season]

        scraper = scraper_factory.get_scraper('NBA')
        teams = scraper.get_teams(season)
        TEAMS[season] = teams
        return teams

# PlayerList


PLAYERS = {}


class PlayerList(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, ['season', 'team'])
        season = args['season']
        team = args['team']
        if PLAYERS.get(season, {}).get(team):
            return PLAYERS[season][team]
        elif not PLAYERS.get(season) == {}:
            PLAYERS[season] = {}

        scraper = scraper_factory.get_scraper('NBA')
        players = scraper.get_players(season, team)
        PLAYERS[season][team] = players
        return players

# GameList


GAMES = {}


class GameList(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, ['season'])
        season = args['season']

        if GAMES.get(season):
            return GAMES[season]

        scraper = scraper_factory.get_scraper('NBA')
        games = scraper.get_games(season)
        GAMES[season] = games
        return games


STATS = {}


class StatList(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, ['game_url', 'home_team', 'away_team'])
        game_url = args['game_url']
        home_team = args['home_team']
        away_team = args['away_team']

        if STATS.get(game_url):
            return STATS[game_url]

        scraper = scraper_factory.get_scraper('NBA')
        stats = scraper.get_stats(game_url, home_team, away_team)
        STATS[game_url] = stats
        return stats


##
# Actually setup the Api resource routing here
##
api.add_resource(TeamList, '/teams')
api.add_resource(PlayerList, '/players')
api.add_resource(GameList, '/games')
api.add_resource(StatList, '/stats')


if __name__ == '__main__':
    app.run(debug=True)
