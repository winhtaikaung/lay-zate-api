from sqlalchemy import text
from tornado.ioloop import IOLoop

from entity.base import DBSession
from entity.user import User


class UserRepository(object):
    def __init__(self, io_loop=None):
        self.io_loop = io_loop or IOLoop.instance()
        self.db_session = DBSession
        pass

    def get_user_by_sender_id(self, sender_id, callback=None):
        session = self.db_session
        result = None

        try:
            result = session.query(User).filter(User.sender_id == sender_id).one()
            callback(result)
        except Exception as e:
            result = e
        callback(result)

    def create_user(self, user_model, callback=None):
        """
        Create a user in DB by passing user_orm
        :param user_model:
        :param callback:
        :return:
        """
        session = self.db_session
        result = True
        try:
            session.add(user_model)
            session.commit()
        except Exception as e:
            session.rollback()
            result = e
        session.close()
        callback(result)

    def upsert_user(self, sender_id, pass_type, fin_number, passport_number, pass_status, date_of_application,
                    callback=None):
        session = self.db_session
        result = None
        sql = "SELECT * FROM tb_userpasscheck as user where user.fin_number =:fin_number  LIMIT 0,10"
        try:
            user_list = session.query(User).from_statement(text(sql)).params(fin_number=fin_number).all()

            if len(user_list) is not 0:
                user = user_list[0]
                user.passport_number = passport_number
                user.pass_status = pass_status
                user.fin_number = fin_number
                user.sender_id = sender_id
                user.pass_type = pass_type
                user.date_of_application = date_of_application
                session.commit()
            else:
                user = User()
                user.passport_number = passport_number
                user.pass_status = pass_status
                user.fin_number = fin_number
                user.sender_id = sender_id
                user.pass_type = pass_type
                user.date_of_application = date_of_application
                session.add(user)
                session.commit()

        except Exception as e:
            session.rollback()
            result = e
        session.close()
        callback(result)
