from functools import wraps


def base_query_string_validator(f):
    @wraps(f)
    def wrapper(self, request):
        """
        This method will intercept the request and validate whether token includes in query parameter or not
        :param self: 
        :param request: 
        :return: 
        """
        if self.get_query_arguments("limit", True) or self.get_query_arguments("page",
                                                                               True):  # check whether querystring is empty or not
            # Process the request
            limit = self.get_argument("limit", True)
            page = self.get_argument("page", True)
            try:

                if int(limit) <= 100:
                    f(self, request)
                    return None
                else:
                    self.respond("Limit size should be lower than 100", 400)
            except Exception as e:
                self.respond("Invalid Param", 400)

        # Redirect to Home Page
        elif self.get_query_arguments("id", True):
            f(self, request)
            return None
        else:
            self.respond("Invalid id or limit", 400)

    return wrapper
