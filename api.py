from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from scraper import Scraper

app = Flask(__name__)
api = Api(app)
scraper = Scraper()


def abort_if_keys_dont_exist(args, keys):
    args = {k: v for k, v in args.items() if v is not None}
    if list(args.keys()) != keys:
        abort(404, message="Missing keys %s" % (keys))


parser = reqparse.RequestParser()
parser.add_argument('season', type=int, location='args')
parser.add_argument('team', type=str, location='args')

# TeamList
TEAMS = {}


class TeamList(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_keys_dont_exist(args, ['season'])
        season = args['season']
        if TEAMS.get(season):
            return TEAMS[season]

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

        games = scraper.get_games(season)
        GAMES[season] = games
        return games


##
# Actually setup the Api resource routing here
##
api.add_resource(TeamList, '/teams')
api.add_resource(PlayerList, '/players')
api.add_resource(GameList, '/games')


if __name__ == '__main__':
    app.run(debug=True)
