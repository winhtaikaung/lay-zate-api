import os

from sqlalchemy import create_engine

from entity.base import Base as model_base
from entity.base import DBSession

url = os.environ["DB_URL_FORMAT"]
url = url.format(os.environ["DB_USER_NAME"], os.environ["DB_PASSWORD"], os.environ["DB_HOST"], os.environ["DB_PORT"],
                 os.environ["DB_NAME"])

# db_engine = create_engine(options.db_connection_str) for sqlite
db_engine = create_engine(url, echo=False)


class DBHelper:
    def __init__(self):
        DBSession.configure(bind=db_engine)

        pass

    def gen_events(self):
        with db_engine.connect() as con:
            con.execute("SET GLOBAL event_scheduler = `ON`;")
            con.execute("DROP EVENT IF EXISTS `CLEAN_RAW`;")
            con.execute(
                "CREATE EVENT `CLEAN_RAW` ON SCHEDULE EVERY 60 SECOND DO DELETE FROM raw WHERE updated_timestamp < DATE_SUB(NOW(),  INTERVAL 6e+7 MINUTE_MICROSECOND)")
            con.execute("DROP EVENT IF EXISTS `CLEAN_ARRIVAL`;")
            con.execute(
                "CREATE EVENT `CLEAN_ARRIVAL` ON SCHEDULE EVERY 60 SECOND DO DELETE FROM arrival WHERE updated_timestamp < DATE_SUB(NOW(),  INTERVAL 6e+7 MINUTE_MICROSECOND)")
            con.execute("DROP EVENT IF EXISTS `CLEAN_DEPARTURE`;")
            con.execute(
                "CREATE EVENT `CLEAN_DEPARTURE` ON SCHEDULE EVERY 60 SECOND DO DELETE FROM departure WHERE updated_timestamp < DATE_SUB(NOW(),  INTERVAL 6e+7 MINUTE_MICROSECOND)")

    def gen_schema(self):
        model_base.metadata.create_all(db_engine)
        self.gen_events()


def generate_meta(table_view_name, limit, page, page_count):
    """
    This method help to generate links and metadata object
    :param table_view_name:
    :param limit:
    :param page:
    :param page_count:
    :return:
    """
    meta_object = {"links": {}, "current": None, "first": 1}
    page_count = (page_count % limit) is 0 and int(page_count / limit) or int(page_count / limit) + 1

    url = "/api/v1/%s?page=%d&limit=%d"
    links = {"self": url % (table_view_name, page, limit),
             "first": url % (table_view_name, 1, limit)}
    meta_object["current"] = page
    if page > 1:
        links.update({"previous": url % (table_view_name, page - 1, limit)})
        meta_object.update({"previous_page": page - 1})
    if page < page_count:
        links.update({"next": url % (table_view_name, page + 1, limit)})
        meta_object.update({"next_page": page + 1})

    links.update({"last": url % (table_view_name, page_count, limit)})
    meta_object.update({"last_page": page_count})
    meta_object["links"] = links

    return meta_object


def gen_offset_from_page(page, limit):
    page = int(page)
    limit = int(limit)
    if page is 0:
        page = 1
    return (page * limit) - limit


def serialize_alchemy(alchemy_object_list):
    user_dictionary = [];

    for row in alchemy_object_list:
        fields = {}
        for field in [x for x in dir(row) if not x.startswith('_') and x != 'metadata' and x != 'query']:
            fields[field] = row.__getattribute__(field)
        user_dictionary.append(fields)
    return user_dictionary
