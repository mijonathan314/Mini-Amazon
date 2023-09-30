from flask import render_template
from flask_login import current_user
import datetime
from flask import jsonify

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)

@bp.route('/cart', methods=['GET'])
def cart():
    # get all items in user's cart
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_items(current_user.id)
    else:
        cart_items = None

    return render_template('cart.html',
                           cart_items=cart_items)
