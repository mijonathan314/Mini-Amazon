from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, quantity, unit_price, fulfillment_status, time_purchased, time_fulfillment_updated, order_id):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.price = unit_price
        self.fulfillment_status = fulfillment_status
        self.time_purchased = time_purchased,
        self.time_fulfillment_updated = time_fulfillment_updated
        self.order_id = order_id

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, quantity, price, fulfillment_status, time_purchased, order_id
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_oid(oid, uid):
        rows = app.db.execute('''
SELECT uid, pid, Purchases.quantity, Purchases.price, Purchases.fulfillment_status, Purchases.time_purchased, Purchases.time_fulfillment_updated, Purchases.order_id, Products.name
FROM Purchases, Products
WHERE order_id = :oid
AND uid = :uid
AND Products.id = Purchases.pid
''',
                              oid=oid, uid=uid)
        return rows#[Purchase(*row) for row in rows]