import re
from functools import wraps


def base_passport_validator(f):
    @wraps(f)
    def wrapper(self, request):
        """
        This method will intercept the request and validate whether token includes in query parameter or not
        :param self: 
        :param request: 
        :return: 
        """
        if self.path_args[0]:  # check whether querystring is empty or not
            # Process the request

            match_obj = re.match('^(?!^0+$)[a-zA-Z0-9]{3,20}$', self.path_args[0], re.M | re.I)
            if match_obj:
                f(self, request)
                return None
            else:
                self.respond("Please enter correct passport Number", 400)
        else:
            self.respond("Invalid Passport", 400)

    return wrapper
