CREATE_USERS_TABLE = '''
CREATE TABLE users(
    id serial primary key,
    name varchar(200) not null,
    username varchar(200) not null unique,
    password varchar(200) not null
);
'''

CREATE_FOODS_TABLE = '''
CREATE TABLE foods(
    id serial primary key,
    name varchar(200) not null,
    picture_url varchar(200),
    available boolean default true,
    price float not null
);
'''

INSERT_FOOD_SQL = '''
INSERT INTO foods(name, picture_url, price)
VALUES (%(name)s, %(picture_url)s, %(price)s)
'''

SEARCH_FOOD_SQL = '''
SELECT * FROM foods
{search_exp}
'''

UPDATE_FOOD_SQL = '''
UPDATE foods
SET {update_exp}
WHERE id = %(id)s
'''

DELETE_FOOD_SQL = '''
DELETE FROM foods
WHERE id = %(id)s
'''

CREATE_ORDERS_TABLE = '''
CREATE TABLE orders(
    id serial primary key,
    phone varchar(20) not null,
    food_id serial references foods(id),
    delivered boolean default false
)
'''

CREATE_ORDER_SQL = '''
INSERT INTO orders(phone, food_id)
VALUES (%(phone)s, %(food_id)s)
'''

ALL_ORDERS_SQL = '''
SELECT DISTINCT phone
FROM orders
WHERE delivered = false
'''

INDIVIDUAL_ORDER_SQL = '''
SELECT foods.id, name, picture_url, price
FROM orders
LEFT JOIN foods ON foods.id = orders.food_id
WHERE phone = %(phone)s and delivered = false
'''

UPDATE_DELIVERED_ORDERS_SQL = '''
UPDATE orders
SET delivered = true
WHERE phone = %(phone)s and delivered = false
'''

CANCEL_ORDERS_SQL = '''
DELETE FROM orders
WHERE phone = %(phone)s and delivered = false
'''

INSERT_RESTAURANT_SQL = '''
INSERT INTO restaurants(name)
VALUES (%(name)s)
'''

INSERT_STAFF_SQL = '''
INSERT INTO users(name, username, password)
VALUES (%(name)s, %(username)s, %(password)s)
'''

GET_STAFF_BY_USERNAME_SQL = '''
SELECT * FROM users
WHERE username = %(username)s
'''