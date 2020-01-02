from flask import Blueprint, g, request

from common.utils import error_response, response, validate_body
from services.food import search_food
from services.orders import create_order, view_individual_order

foods = Blueprint('foods', __name__)


@foods.before_request
def validate_request():
    restaurant_name = g.restaurant_name
    if not restaurant_name:
        return error_response('Invalid route', 'error', 'RO', 404)


@foods.route('/view', methods=['GET'])
def search():
    db = g.restaurant_name
    try:
        status, data = search_food(request.args, db)
        if not status:
            return error_response(str(data))
        return response(True, 'Foods search successful', data)
    except Exception as err:
        return error_response(str(err))


@foods.route('/order', methods=['POST'])
def order():
    db = g.restaurant_name
    body = request.get_json()
    status, missing_field = validate_body(body, ['phone', 'food_id'])
    if not status:
        return error_response(f'{missing_field} is required')
    try:
        status, res = create_order(body, db)
        if not status:
            return error_response(str(res))
        return response(True, 'Order created successfully', None)
    except Exception as err:
        return error_response(str(err))


@foods.route('/order', methods=['GET'])
def view_orders():
    db = g.restaurant_name
    status, missing_field = validate_body(request.args, ['phone'])
    if not status:
        return error_response(f'{missing_field} is missing from query params')
    try:
        status, res = view_individual_order(request.args, db)
        if not status:
            return error_response(str(res))
        return response(True, 'Your Orders', res)
    except Exception as err:
        return error_response(str(err))
