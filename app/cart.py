from flask import render_template
from flask_login import current_user
import datetime
from flask import jsonify

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)

@bp.route('/cart')
def cart():
    # get all items in user's cart
    if current_user.is_authenticated:
        test = Cart.get_cart_items(current_user.id)
        items = Cart.get(current_user.id)
    else:
        items = None

    #return jsonify([item.__dict__ for item in items])
    return render_template('cart.html',
                           cart_items=test)
