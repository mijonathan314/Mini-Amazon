from flask import current_app as app
from flask import render_template, redirect, url_for, flash, request


class Inventory:
    def __init__(self, user_id, product_id, name, price, quantity):
        self.product_id = product_id #from product
        self.user_id = user_id #from user
        self.name = name
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get_all_inventories_by_user(user_id):
        #the colon in below area means that it is what is passed in
        rows = app.db.execute('''
SELECT Users.id, Products.id, Products.name, Products.price, Products.quantity
FROM Users, Products
WHERE Products.user_id = :user_id AND Users.id = :user_id
''',
                              user_id=user_id)
        return [Inventory(*row) for row in rows]
