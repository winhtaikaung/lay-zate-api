import re

from functools import wraps


def base_query_string_validator(f):
    @wraps(f)
    async def wrapper(self, airport_code, arv_dep_type, query_time):
        """
        This method will intercept the request and validate whether token includes in query parameter or not
        :param self: 
        :param request: 
        :return: 
        """
        if self.get_query_arguments("limit", True) and self.get_query_arguments("page",
                                                                                True):  # check whether querystring is empty or not
            # Process the request

            try:
                limit = str(self.get_argument("limit", default=10, strip=True))
                page = str(self.get_argument("page", default=1, strip=True))
                limit = re.sub(r"<[^>]*>", "", limit)
                page = re.sub(r"<[^>]*>", "", page)

                if "-" not in limit and "-" not in page:

                    try:

                        limit = int(limit)
                        page = int(page)
                        if int(limit) <= 100:
                            await f(self, airport_code, arv_dep_type, query_time)
                            # return None
                        else:
                            self.respond("Limit size should be lower than 100", 400)
                    except Exception as e:
                        self.error(str(e), 502)
                else:
                    self.respond("Invalid Param", 400)

            except Exception as e:
                self.error(str(e), 500)

        # Redirect to Home Page
        elif self.get_query_arguments("id", True):
            await f(self, airport_code, arv_dep_type, query_time)
            # return None
        else:
            self.respond("Invalid id or limit", 400)

    return wrapper
