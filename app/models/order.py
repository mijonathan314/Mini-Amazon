from flask import current_app as app

class Order:
     def __init__(self, id, uid, total_price, total_items, timestamp):
        self.id = id
        self.user_id = uid
        self.total_price = total_price
        self.total_items = total_items
        self.timestamp = timestamp
    
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, user_id, total_price, total_items, time_stamp
FROM Orders
WHERE id =:id
''',
                              id=id)
        return [Order(*row) for row in rows]
    
    @staticmethod
    def add_order(user_id, total_price, total_items):
        rows = app.db.execute('''
INSERT INTO Orders(user_id, total_price, total_items)
VALUES (:user_id, :total_price, :total_items)
RETURNING id
''',
                                user_id = user_id,
                                total_price = total_price,
                                total_items = total_items)