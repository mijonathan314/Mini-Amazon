from flask import render_template
from flask_login import current_user
import datetime
from flask import jsonify

from .models.product import Product

from flask import Blueprint
bp = Blueprint('product', __name__)


@bp.route('/product/<int:k>', methods=['GET'])
def get_top_products(k):
    # find the top k most expensive products
    if current_user.is_authenticated:
        product = Product.get_top_expensive_products(k)
    else:
        product = None
    return render_template('products.html', top_product = product)