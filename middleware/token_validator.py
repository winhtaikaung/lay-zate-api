from functools import wraps


def token_validator(f):
    @wraps(f)
    def wrapper(self, request):
        """
        This method will intercept the request and validate whether token includes in query parameter or not
        :param self: 
        :param request: 
        :return: 
        """
        if self.get_query_arguments("token", True):  # check whether querystring is empty or not
            # Process the request
            f(self, request)
            return None
        # Redirect to Home Page
        self.respond("Invalid Request", 400)

    return wrapper
