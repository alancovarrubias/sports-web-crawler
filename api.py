from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from const.models import TEAM, PLAYER, GAME, STAT
from resources import Resources
from store.keys import KeyStore

app = Flask(__name__)
api = Api(app)

def abort_if_invalid(key_store):
    if not key_store.valid:
        abort(404, message=key_store.error_message)
        
parser = reqparse.RequestParser()
parser.add_argument('sport', type=str, location='args')
parser.add_argument('season', type=int, location='args')
parser.add_argument('team', type=str, location='args')
parser.add_argument('teams', type=str, location='args')
parser.add_argument('game_url', type=str, location='args')
parser.add_argument('away_team', type=str, location='args')
parser.add_argument('home_team', type=str, location='args')

def get_resource(resource_type):
    args = parser.parse_args()
    key_store = KeyStore(resource_type, args)
    abort_if_invalid(key_store)
    resources = Resources(key_store)
    return resources.fetch()

class TeamResources(Resource):
    def get(self):
        return get_resource(TEAM)

class PlayerResources(Resource):
    def get(self):
        return get_resource(PLAYER)

class GameResources(Resource):
    def get(self):
        return get_resource(GAME)

class StatResources(Resource):
    def get(self):
        return get_resource(STAT)

api.add_resource(TeamResources, '/teams')
api.add_resource(PlayerResources, '/players')
api.add_resource(GameResources, '/games')
api.add_resource(StatResources, '/stats')


if __name__ == '__main__':
    app.run(debug=True)
