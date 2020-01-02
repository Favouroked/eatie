from flask import Blueprint, request, g

from common.utils import response, error_response
from services.restaurants import create_restaurant_domain

restaurants = Blueprint('restaurants', __name__)


@restaurants.route('/create', methods=['POST'])
def create_restaurant():
    if g.restaurant_name:
        return error_response('Invalid route', 'error', 'RO', 404)
    body = request.get_json()
    if 'name' not in body:
        return error_response("Field 'name' is required")
    try:
        create_restaurant_domain(body['name'])
    except Exception as err:
        return error_response(str(err))
    domain = f'{body["name"]}.eatie.com'
    return response(True, f'{domain} created successfully', None)
