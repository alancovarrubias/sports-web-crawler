from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from scrapers import ScraperFactory
from datastore import Datastore

app = Flask(__name__)
api = Api(app)
scraper_factory = ScraperFactory()


def abort_if_invalid(datastore, args):
    if not datastore.validate_args(args):
        abort(404, message="Required arguments %s" %
              datastore.required_keys(args))


parser = reqparse.RequestParser()
parser.add_argument('sport', type=str, location='args')
parser.add_argument('season', type=int, location='args')
parser.add_argument('team', type=str, location='args')
parser.add_argument('teams', type=str, location='args')
parser.add_argument('game_url', type=str, location='args')
parser.add_argument('away_team', type=str, location='args')
parser.add_argument('home_team', type=str, location='args')

TEAMS = Datastore('Team')


class TeamResource(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_invalid(TEAMS, args)
        if TEAMS.exists(args):
            return TEAMS.get(args)

        scraper = scraper_factory.get_scraper(args)
        teams_data = scraper.get_teams(args)
        TEAMS.set(args, teams_data)
        return teams_data


PLAYERS = Datastore('Player')


class PlayerResource(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_invalid(PLAYERS, args)
        if PLAYERS.exists(args):
            return PLAYERS.get(args)

        scraper = scraper_factory.get_scraper(args)
        players_data = scraper.get_players(args)
        PLAYERS.set(args, players_data)
        return players_data


GAME_KEYS = ['sport', 'season']
GAMES = Datastore('Game')


class GameResource(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_invalid(GAMES, args)

        if GAMES.exists(args):
            return GAMES.get(args)

        scraper = scraper_factory.get_scraper(args)
        games_data = scraper.get_games(args)
        GAMES.set(args, games_data)
        return games_data


STAT_KEYS = ['sport', 'game_url', 'home_team', 'away_team']
STATS = Datastore('Stat')


class StatResource(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_invalid(STATS, args)

        if STATS.exists(args):
            return STATS.get(args)

        scraper = scraper_factory.get_scraper(args)
        stats_data = scraper.get_stats(args)
        STATS.set(args, stats_data)
        return stats_data


api.add_resource(TeamResource, '/teams')
api.add_resource(PlayerResource, '/players')
api.add_resource(GameResource, '/games')
api.add_resource(StatResource, '/stats')


if __name__ == '__main__':
    app.run(debug=True)
