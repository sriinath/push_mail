import falcon
from routes.ping import Ping

api = falcon.API()
api.add_route('/ping', Ping())
