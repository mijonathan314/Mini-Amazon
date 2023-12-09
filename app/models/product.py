from flask import current_app as app


class Product:
    def __init__(self, id, name, price, quantity, available, category = None, description = None):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.available = available
        self.category = category
        self.description = description

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, quantity, available, category, description
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, quantity, available, category, description
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
  
    @staticmethod
    def get_top_expensive_products(k):
        rows = app.db.execute('''
    SELECT id, name, price, available, quantity, category, description
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
    SELECT id, name, price, available, quantity, category, description
    FROM Products
    WHERE category = :category AND available = :available
    ''',
                            category=category, available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_name_keyword(keyword, available=True):
        # New method to filter products by a keyword in the product name
        keyword_pattern = f'%{keyword}%'  # Prepares the keyword for pattern matching
        rows = app.db.execute('''
    SELECT id, name, price, available, quantity, category, description
    FROM Products
    WHERE name LIKE :keyword AND available = :available
    ''',
                          keyword=keyword_pattern, available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_product_sellers(product_id):
        rows = app.db.execute('''
    SELECT Users.id, Users.firstname, Products.quantity
    FROM Users
    JOIN Products ON Users.id = Products.user_id
    WHERE Products.id = :product_id
    ''',
                            product_id=product_id)
        return rows
