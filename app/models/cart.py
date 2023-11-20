from flask import current_app as app

class Cart:
    def __init__(self, id, uid, pid, quantity, fulfilled, order_placed):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.quantity = quantity
        self.fulfilled = fulfilled
        self.order_placed = order_placed

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, quantity, fulfilled, order_placed
FROM Carts
WHERE id =:id
''',
                              id=id)
        return [Cart(*row) for row in rows]
    
    @staticmethod
    def get_cart_items(uid):
        rows = app.db.execute('''
SELECT c.id, c.uid, c.pid, c.quantity, c.fulfilled, c.order_placed, p.name, p.price, p.available
FROM Carts c, Products p
WHERE c.uid =:uid
AND c.pid = p.id
AND c.order_placed = False
''',
                            uid=uid)
        return rows#[Cart(*row) for row in rows]

    @staticmethod
    def add_item_to_cart(uid, pid, quantity):
        try:
            rows = app.db.execute("""
INSERT INTO Carts(uid, pid, quantity, fulfilled, order_placed)
VALUES(:uid, :pid, :quantity, :fulfilled, :order_placed)
RETURNING id
""",
                                uid=uid,
                                pid=pid,
                                quantity=quantity, fulfilled=False, order_placed=False)
            id = rows[0][0]
            return Cart.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def update_cart_item(uid, pid, new_quantity):
        try:
            rows = app.db.execute("""
UPDATE Carts
SET quantity=:new_quantity
WHERE uid=:uid
AND pid=:pid
AND order_placed=False
""",
                                uid=uid,
                                pid=pid,
                                new_quantity=new_quantity)
            id = rows[0][0]
            return Cart.get(id)
        except Exception as e:
            print(str(e))
            return None   

    @staticmethod
    def delete_cart_item(uid, pid):
        try:
            rows = app.db.execute("""
DELETE FROM Carts
WHERE uid=:uid
AND pid=:pid
AND order_placed=False
""",
                                uid=uid,
                                pid=pid)
            return rows
        except Exception as e:
            print(str(e))
            return None     

    @staticmethod
    def submit_cart_item(uid, pid):
        try:
            rows = app.db.execute("""
UPDATE Carts
SET order_placed=True, order_time=CURRENT_TIMESTAMP
WHERE uid=:uid
AND pid=:pid
AND order_placed=False
""",
                                uid=uid,
                                pid=pid)
            id = rows[0][0]
            return Cart.get(id)
        except Exception as e:
            print(str(e))
            return None   

