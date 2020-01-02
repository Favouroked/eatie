from common.constants import ALL_ORDERS_SQL, UPDATE_DELIVERED_ORDERS_SQL, CANCEL_ORDERS_SQL, INDIVIDUAL_ORDER_SQL, \
    CREATE_ORDER_SQL
from database.postgres import Postgres

pg = Postgres()


def create_order(body, db):
    return pg.insert_into_db(CREATE_ORDER_SQL, body, db)


def deliver_orders(body, db):
    return pg.insert_into_db(UPDATE_DELIVERED_ORDERS_SQL, body, db)


def cancel_orders(body, db):
    return pg.insert_into_db(CANCEL_ORDERS_SQL, body, db)


def all_orders(db):
    return pg.execute_query(ALL_ORDERS_SQL, {}, db)


def view_individual_order(body, db):
    return pg.execute_query(INDIVIDUAL_ORDER_SQL, body, db)
