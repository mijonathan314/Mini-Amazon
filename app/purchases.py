from flask import render_template
from flask_login import current_user
import datetime

from .models.purchase import Purchase
from .models.order import Order

from flask import Blueprint
bp = Blueprint('purchases', __name__)


@bp.route('/orders/<int:uid>', methods=['GET'])
def get_orders_by_uid(uid):
    # find the orders the user has purchased given uid
    orders = None
    if current_user.is_authenticated:
        orders = Order.get_by_uid(uid)
    return render_template('orderHistory.html', order_history=orders)

@bp.route('/purchases/<int:uid>', methods=['GET'])
def get_purchases_by_uid(uid):
    # find the purchases the user has purchased given uid
    purchases = None
    category_counts = {}
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid(uid)
        for purchase in purchases: 
            if purchase.category not in category_counts: 
                category_counts[purchase.category] = 0
            category_counts[purchase.category] += 1
    return render_template('purchases.html', purchase_history=purchases, category_counts=category_counts)
