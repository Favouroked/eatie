from common.constants import INSERT_FOOD_SQL, UPDATE_FOOD_SQL, DELETE_FOOD_SQL, SEARCH_FOOD_SQL
from database.postgres import Postgres

pg = Postgres()


def insert_food(body, db):
    return pg.insert_into_db(INSERT_FOOD_SQL, body, db)


def update_food(body, db):
    food_id = body.pop('id')
    fields = list(body.keys())
    update_params_list = [f'{field} = %({field})s' for field in fields]
    update_exp = ', '.join(update_params_list)
    sql = UPDATE_FOOD_SQL.format(update_exp=update_exp)
    return pg.insert_into_db(sql, {'id': food_id, **body}, db)


def delete_food(food_id, db):
    return pg.insert_into_db(DELETE_FOOD_SQL, {'id': food_id}, db)


def search_food(args, db):
    fields = list(args.keys())
    exp_list = [f'{field} = %({field})s' for field in fields]
    search_exp = f"WHERE {' AND '.join(exp_list)}" if len(exp_list) > 0 else ''
    sql = SEARCH_FOOD_SQL.format(search_exp=search_exp)
    return pg.execute_query(sql, args, db)
