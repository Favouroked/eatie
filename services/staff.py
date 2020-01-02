import os

import bcrypt
import jwt

from common.constants import INSERT_STAFF_SQL, GET_STAFF_BY_USERNAME_SQL
from database.postgres import Postgres

pg = Postgres()

JWT_SECRET = os.getenv('JWT_SECRET')


def create_staff(body, db):
    password = body['password'].encode()  # converts str to bytes
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
    body['password'] = hashed.decode()
    return pg.insert_into_db(INSERT_STAFF_SQL, body, db)


def login_staff(body, db):
    status, res = pg.execute_query(GET_STAFF_BY_USERNAME_SQL, {'username': body['username']}, db)
    if not status:
        return False, str(res)
    if len(res) < 1:
        return False, 'Staff does not exist'
    staff = res[0]
    hashed_password = staff.get('password')
    if bcrypt.checkpw(body['password'].encode(), hashed_password.encode()):
        return True, staff
    else:
        return False, 'Invalid crendentials'


def encode_jwt(body):
    token = jwt.encode(body, JWT_SECRET, algorithm='HS256')
    return token.decode()


def decode_jwt(token):
    body = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    return body
