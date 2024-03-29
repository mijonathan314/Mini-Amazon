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
    
    @staticmethod
    def remove_product(user_id, product_id):
        rows = app.db.execute('''
DELETE FROM Products
WHERE user_id = :user_id AND product_id = :id
''',
                              user_id =user_id, product_id = product_id)
        return redirect(url_for('inventory.seller'))
class Sales:
    def __init__(self, count):
        self.count = count   

    @staticmethod
    def get_total_sales(user_id):
        rows = app.db.execute('''
SELECT COUNT(DISTINCT Orders.id) AS num_orders
FROM Orders, Products, Purchases, Users
WHERE (
    Products.user_id = :user_id AND
    Products.id = Purchases.pid AND
    Purchases.uid = Users.id AND
    Orders.id = Purchases.order_id                    
)
                              ''',
                              user_id = user_id)
        return [Sales(*row) for row in rows] 
class Popular:
    def __init__(self, name):
        self.name = name  

    @staticmethod
    def get_most_popular_by_user(user_id):
        rows = app.db.execute('''
SELECT  Products.name
FROM Orders, Products, Purchases, Users
WHERE (
    Products.user_id = :user_id AND
    Products.id = Purchases.pid AND
    Purchases.uid = Users.id AND
    Orders.id = Purchases.order_id                  
)
GROUP BY  Products.name
ORDER BY COUNT(*) DESC
LIMIT 1
                              ''',
                              user_id = user_id)
        return [Popular(*row) for row in rows] 
class Fulfillment:
    def __init__(self, user_id, order_id, address,name, fulfillment_status, time_stamp, total_items, product_id):
        self.user_id = user_id #from orders, this is the BUYER
        self.order_id = order_id #from orders and purchases
        self.address = address #from users
        self.name = name
        self.fulfillment_status = fulfillment_status #from purchases
        self.time_stamp = time_stamp #from orders
        self.total_items = total_items #from orders 
        self.product_id = product_id


    @staticmethod
    def get_all_fulfillment_by_user(user_id):
        rows = app.db.execute('''
SELECT Purchases.uid, Orders.id, Users.address, Products.name, Purchases.fulfillment_status, Orders.time_stamp, Orders.total_items, Products.id
FROM Orders, Products, Purchases, Users
WHERE (
    Products.user_id = :user_id AND
    Products.id = Purchases.pid AND
    Purchases.uid = Users.id AND
    Orders.id = Purchases.order_id

)
ORDER BY Orders.time_stamp DESC
''',
                              user_id=user_id)
        return [Fulfillment(*row) for row in rows]
    
    @staticmethod
    def mark_fulfilled(order_id, product_id, fulfillment_status):
        rows = app.db.execute('''
UPDATE Purchases
SET fulfillment_status = :fulfillment_status
WHERE order_id = :order_id AND product_id = :product_id
''',
                              order_id = order_id, fulfillment_status = fulfillment_status)
        return [Fulfillment(*row) for row in rows]

class moreProduct:
    def __init__(self, user_id, name, price, quantity, category):
        self.user_id = user_id #from orders, this is the BUYER
        self.name = name #from orders and purchases
        self.price = price #from purchases
        self.quantity = quantity #from orders 
        self.categpry = category

    @staticmethod
    def add_product(user_id, name,  price, quantity, category):
        try:
            quantity = int(quantity)
        except Exception as e:
            raise BadUpdateException("Quantity must be a number")

        if quantity <= 0:
            raise BadUpdateException("Quantity must be greater than 0")

        try:
            price = float(price)
        except Exception as e:
            raise BadUpdateException("Price must be a Float")

        try:
            app.db.execute("""
UPDATE Users
SET seller = True
WHERE Users.id = :uid 
""",
                                uid=user_id)

            app.db.execute("""
INSERT INTO Products(user_id, name, price, quantity, available, category)
VALUES(:uid, :name,  :price, :quantity, True, :category)
RETURNING id
""",
                                uid=user_id,  name=name,  price=price,
                                 quantity=quantity, category=category)

            

            return redirect(url_for('inventory.seller'))
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None