from flask import Blueprint, g, request

from common.utils import error_response, response, validate_body
from services.orders import view_individual_order, all_orders, deliver_orders, cancel_orders
from services.staff import decode_jwt

orders = Blueprint('orders', __name__)


@orders.before_request
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


@orders.route('/view', methods=['GET'])
def view():
    args = request.args
    db = g.restaurant_name
    try:
        if not args:
            status, data = all_orders(db)
        elif 'phone' in args:
            status, data = view_individual_order(args, db)
        else:
            return error_response('phone should be present in the query params')
        if not status:
            return error_response(str(data))
        return response(True, 'Success', data)
    except Exception as err:
        return error_response(str(err))


@orders.route('/delivered', methods=['PUT'])
def deliver():
    body = request.get_json()
    db = g.restaurant_name
    status, missing_field = validate_body(body, ['phone'])
    if not status:
        return error_response(f'{missing_field} is required')
    try:
        status, res = deliver_orders(body, db)
        if not status:
            return error_response(str(res))
        return response(True, 'Orders status updated', None)
    except Exception as err:
        return error_response(str(err))


@orders.route('/cancel', methods=['PUT'])
def cancel():
    body = request.get_json()
    db = g.restaurant_name
    status, missing_field = validate_body(body, ['phone'])
    if not status:
        return error_response(f'{missing_field} is required')
    try:
        status, res = cancel_orders(body, db)
        if not status:
            return error_response(str(res))
        return response(True, 'Orders canceled successfully', None)
    except Exception as err:
        return error_response(str(err))
