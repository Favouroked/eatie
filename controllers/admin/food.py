from flask import Blueprint, g, request

from common.utils import error_response, validate_body, response
from services.food import insert_food, update_food, delete_food
from services.staff import decode_jwt

food = Blueprint('food', __name__)


@food.before_request
def validate_request():
    restaurant_name = g.restaurant_name
    if not restaurant_name:
        return error_response('Invalid route', 'error', 'RO', 404)
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return error_response('Authorization required', 'error', 'RO', 403)
    try:
        token = auth_header.split('Bearer')[-1].strip()
        body = decode_jwt(token)
        if body['restaurant'] != restaurant_name:
            return error_response('Invalid Auth token', 'error', 'RO', 403)
    except Exception as err:
        print(f'=====> Auth Error', err)
        return error_response('Invalid Auth token', 'error', 'RO', 403)


@food.route('/create', methods=['POST'])
def create():
    body = request.get_json()
    db = g.restaurant_name
    status, missing_field = validate_body(body, ['name', 'picture_url', 'price'])
    if not status:
        return error_response(f'{missing_field} is required')
    try:
        status, res = insert_food(body, db)
        if not status:
            return error_response(str(res))
        return response(True, 'Food created successfully', None)
    except Exception as err:
        return error_response(str(err))


@food.route('/update', methods=['PUT'])
def update():
    db = g.restaurant_name
    body = request.get_json()
    status, missing_field = validate_body(body, ['id'])
    if not status:
        return error_response(f'{missing_field} is required')
    try:
        status, data = update_food(body, db)
        if not status:
            return error_response(str(data))
        return response(True, 'Food updated successfully', None)
    except Exception as err:
        return error_response(str(err))


@food.route('/delete', methods=['DELETE'])
def delete():
    db = g.restaurant_name
    food_id = request.args.get('id')
    if not food_id:
        return error_response('id is required')
    try:
        status, data = delete_food(food_id, db)
        if not status:
            return error_response(str(data))
        return response(True, 'Food deleted successfully', None)
    except Exception as err:
        return error_response(str(err))
