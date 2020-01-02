from flask import Blueprint, g, request

from common.utils import error_response, validate_body, response
from services.staff import create_staff, encode_jwt, login_staff

staff = Blueprint('staff', __name__)


@staff.before_request
def validate_restaurant_name():
    restaurant_name = g.restaurant_name
    if not restaurant_name:
        return error_response('Invalid route', 'error', 'RO', 404)


@staff.route('/register', methods=['POST'])
def register_staff():
    body = request.get_json()
    db = g.restaurant_name
    status, missing_field = validate_body(body, ['name', 'username', 'password'])
    if not status:
        return error_response(f'{missing_field} missing')
    try:
        status, data = create_staff(body, db)
        if not status:
            raise Exception(str(data))
        token = encode_jwt({'name': body['name'], 'restaurant': db})
        return response(True, 'Staff creation successful', {'token': token, 'restaurant': db})
    except Exception as err:
        return error_response(str(err))


@staff.route('/login', methods=['POST'])
def signin_staff():
    body = request.get_json()
    db = g.restaurant_name
    status, missing_field = validate_body(body, ['username', 'password'])
    if not status:
        return error_response(f'{missing_field} missing')
    try:
        status, data = login_staff(body, db)
        if not status:
            raise Exception(str(data))
        token = encode_jwt({'name': data['name'], 'restaurant': db})
        return response(True, 'Staff login successful', {'token': token, 'restaurant': db})
    except Exception as err:
        return error_response(str(err))
