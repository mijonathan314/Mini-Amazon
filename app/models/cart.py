from flask import current_app as app

class Cart:
    def __init__(self, id, uid, pid, quantity, fulfilled):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.fulfilled = fulfilled

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT id, uid, pid, quantity, fulfilled
FROM Carts
WHERE uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]
    
    @staticmethod
    def get_cart_items(uid):
        rows = app.db.execute('''
SELECT c.id, c.uid, c.pid, c.quantity, c.fulfilled, p.name, p.price, p.available
FROM Carts c, Products p
WHERE c.uid = :uid
AND c.pid = p.id
''',
                            uid=uid)
        return rows#[Cart(*row) for row in rows]

#     @staticmethod
#     def get_all(available=True):
#         rows = app.db.execute('''
# SELECT id, name, price, available
# FROM Products
# WHERE available = :available
# ''',
#                               available=available)
#         return [Product(*row) for row in rows]
