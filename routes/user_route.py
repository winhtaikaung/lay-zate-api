from handlers.user.user_handler import UserHandler

user_routes = [
    (r'/api/v1/user/([^/]+)', UserHandler)
]
