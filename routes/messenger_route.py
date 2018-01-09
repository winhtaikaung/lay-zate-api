from handlers.messenger.messenger_handler import MessengerHandler

messenger_routes = [
    # (r'/api/v1/user/(?P<param1>[^\/]+)/?(?P<param2>[^\/]+)?/?(?P<param3>[^\/]+)?', UserHandler),
    (r'/bot/?(.*)', MessengerHandler)
]
