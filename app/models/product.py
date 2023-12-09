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
    def get_top_products_by_quantity(k):
        rows = app.db.execute('''
    SELECT id, name, price, quantity, available, category, description
    FROM Products
    WHERE available = True
    ORDER BY quantity DESC
    LIMIT :k
    ''',
                        k=k)
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

    @staticmethod
    def add_new_product(name, price, quantity, category, description, user_id):
        try:
            rows = app.db.execute("""
    INSERT INTO Products(name, price, quantity, category, description, user_id)
    VALUES(:name, :price, :quantity, :category, :description, :user_id)
    RETURNING id
    """,
                                    name=name,
                                    price=price,
                                    quantity=quantity,
                                    category=category,
                                    description=description,
                                    user_id=user_id)
            return rows[0][0]  # Returns the new product ID
        except Exception as e:
            print(str(e))
            return None
