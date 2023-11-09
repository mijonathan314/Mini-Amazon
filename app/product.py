from flask import render_template
from flask_login import current_user
import datetime
from flask import jsonify, request

from .models.product import Product

from flask import Blueprint
bp = Blueprint('product', __name__)


@bp.route('/product', methods=['POST'])
def get_top_products():
    if request.method == 'POST':
        k = int(request.form.get('k-value', 1))  # Get the value of k from the form
    else:
        k = 0  # Default value if no input provided

    if current_user.is_authenticated:
        products = Product.get_top_expensive_products(k)
    else:
        products = None

    return render_template('products.html', top_product=products)

@bp.route('/get_by_category', methods=['POST'])
def get_by_category():
    category = request.form['category'].strip()  # Get the category from the form input
    if current_user.is_authenticated and category:
        # Call a method to get products by category, you need to implement it in the Product model
        filtered_products = Product.get_by_category(category)
    else:
        filtered_products = []

    # Render the same products page or a specific category page with the filtered products
    return render_template('products.html', top_product=filtered_products)




