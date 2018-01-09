"""
IndicoServer Errors
"""


class CustomError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super(Exception, self).__init__(message)


# 400
class MissingField(CustomError):
    def __init__(self, field):
        CustomError.__init__(self,
                             "%s field was not provided" % field,
                             400
                             )


class WrongFieldType(CustomError):
    def __init__(self, field, _given, _required):
        CustomError.__init__(self,
                             "Field %s - %s is type %s but should be %s" %
                             (field, _given, type(_given), _required),
                             400
                             )


class InvalidJSON(CustomError):
    def __init__(self):
        CustomError.__init__(self,
                             "No JSON object could be decoded.",
                             400
                             )


# 401
class FacebookTokenError(CustomError):
    def __init__(self):
        CustomError.__init__(self,
                             "Facebook Auth Token invalid",
                             401
                             )


class AuthError(CustomError):
    def __init__(self):
        CustomError.__init__(self,
                             "User not authenticated",
                             401
                             )


# 404
class RouteNotFound(CustomError):
    def __init__(self, action):
        CustomError.__init__(self,
                             "%s route could not be found" % action,
                             404
                             )


# 500
class MongoError(CustomError):
    def __init__(self, message):
        CustomError.__init__(self,
                             message,
                             500
                             )


class ServerError(CustomError):
    def __init__(self):
        CustomError.__init__(self,
                             "we screwed up and have some debugging to do",
                             500
                             )
