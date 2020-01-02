from database.postgres import Postgres
from common.constants import CREATE_FOODS_TABLE, CREATE_ORDERS_TABLE, CREATE_USERS_TABLE, INSERT_RESTAURANT_SQL

pg = Postgres()


def create_restaurant_domain(restaurant_name):
    pg.create_database(restaurant_name)
    pg.insert_into_db(CREATE_USERS_TABLE, {}, restaurant_name)
    pg.insert_into_db(CREATE_FOODS_TABLE, {}, restaurant_name)
    pg.insert_into_db(CREATE_ORDERS_TABLE, {}, restaurant_name)
    pg.insert_into_db(INSERT_RESTAURANT_SQL, {'name': restaurant_name})

