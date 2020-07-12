import falcon
from routes.ping import Ping
from routes.mail import Mail

api = falcon.API()
api.add_route('/ping', Ping())
api.add_route('/api/v1/message/send', Mail())
