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
    def add_order(id, user_id, total_price, total_items, timestamp):
        rows = app.db.execute('''
INSERT INTO Orders(id, user_id, total_price, total_items, time_stamp)
VALUES (:id, :user_id, :total_price, :total_items, :timestamp)
RETURNING id
''',
                                id = id,
                                user_id = user_id,
                                total_price = total_price,
                                total_items = total_items,
                                timestamp=timestamp)
    
    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT *
FROM Orders
WHERE user_id =:uid
ORDER BY time_stamp DESC
''',
                                uid=uid)
        return rows
