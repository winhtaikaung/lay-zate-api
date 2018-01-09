from _blake2 import blake2b

import tornado.web
from tornado import gen

from db.user_repo import UserRepository
from handlers.base_handler import BaseHandler


class UserHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    # @base_passport_validator
    @gen.engine
    def get(self, params):
        fin_number = self.get_argument("fin")
        passport_number = self.get_argument("ppNo")

        hashed_fin = blake2b(str(fin_number).encode('utf8')).hexdigest()
        hash_passport = blake2b(str(passport_number).encode('utf8')).hexdigest()
        pass_status = "Issued"

        user_repo = UserRepository()
        response = yield gen.Task(user_repo.upsert_user, '123123123213', 'EMPLOYMENT_PASS', hashed_fin, hash_passport,
                                  pass_status, '12/04/2017')
        self.respond({"msg": "retrieved"}, {}, 200)
