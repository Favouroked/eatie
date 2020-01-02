from flask import Flask, request, g

from controllers.admin.food import food as admin_food
from controllers.admin.orders import orders as admin_orders
from controllers.restaurants import restaurants
from controllers.staff import staff
from controllers.foods import foods

app = Flask(__name__)
app.config['SERVER_DOMAIN'] = 'eatie.com'


@app.before_request
def parse_subdomain():
    server_domain = app.config['SERVER_DOMAIN']
    host = request.host
    subdomain = host.split(server_domain)[0].rstrip('.')
    if len(subdomain) == 0 or subdomain == 'www':
        g.restaurant_name = None
    else:
        g.restaurant_name = subdomain


@app.route('/')
def hello_world():
    sub = g.restaurant_name
    return sub


app.register_blueprint(restaurants, url_prefix='/restaurants')
app.register_blueprint(staff, url_prefix='/staff')
app.register_blueprint(admin_food, url_prefix='/admin/foods')
app.register_blueprint(admin_orders, url_prefix='/admin/orders')
app.register_blueprint(foods, url_prefix='/foods')

if __name__ == '__main__':
    app.run()
