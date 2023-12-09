from flask import render_template, request
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
        page = int(request.args.get('page', 1))
        items_per_page = 8
        start_idx = (page - 1) * items_per_page
        end_idx = page * items_per_page
        # get the items on the current page
        order_list = orders[start_idx:end_idx]
        total_pages = (len(orders) + items_per_page - 1) // items_per_page
    return render_template('orderHistory.html', order_history=order_list, orders=orders,
                           page=page, total_pages=total_pages)

@bp.route('/purchases/<int:uid>', methods=['GET'])
def get_purchases_by_uid(uid):
    # find the purchases the user has purchased given uid
    purchases = None
    category_counts = {}
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid(uid)
        page = int(request.args.get('page', 1))
        items_per_page = 8
        start_idx = (page - 1) * items_per_page
        end_idx = page * items_per_page
        # get the items on the current page
        purchase_list = purchases[start_idx:end_idx]
        total_pages = (len(purchases) + items_per_page - 1) // items_per_page

        for purchase in purchases: 
            if purchase.category not in category_counts: 
                category_counts[purchase.category] = 0
            category_counts[purchase.category] += 1
    return render_template('purchases.html', purchase_history=purchase_list, page=page, 
                           total_pages=total_pages, category_counts=category_counts)
