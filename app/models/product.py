from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available, category = None):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.category = category

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available, category
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available, category
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
  
    @staticmethod
    def get_top_expensive_products(k):
        rows = app.db.execute('''
    SELECT id, name, price, available, category
    FROM Products
    ORDER BY price DESC
    LIMIT :k
    ''',
                            k=k)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_category(category, available=True):
        # New method to filter products by category
        rows = app.db.execute('''
    SELECT id, name, price, available, category
    FROM Products
    WHERE category = :category AND available = :available
    ''',
                            category=category, available=available)
        return [Product(*row) for row in rows]
