from flask import render_template, flash
from flask_login import current_user
import datetime
from flask import jsonify

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint, request, redirect, url_for
bp = Blueprint('cart', __name__)

@bp.route('/cart', methods=['GET'])
def cart():
    if current_user.is_authenticated:
        # get all items in the cart
        all_cart_items = Cart.get_cart_items(current_user.id)
        page = int(request.args.get('page', 1))
        items_per_page = 10
        start_idx = (page - 1) * items_per_page
        end_idx = page * items_per_page
        # get the items on the current page
        cart_items = all_cart_items[start_idx:end_idx]
        total_pages = (len(all_cart_items) + items_per_page - 1) // items_per_page
        total_price = 0
        for item in all_cart_items:
            total_price += item[3]*item[7]

    else:
        cart_items = None
        page = None
        total_pages = None

    return render_template('cart.html',
                           cart_items=cart_items, page=page, total_pages=total_pages, total_price=total_price)

@bp.route('/update-cart-item/<int:pid>', methods=['PATCH'])
def update_cart_item(pid):
    try:
        data = request.get_json()
        new_quantity = data.get('newQuantity')
        if current_user.is_authenticated:
            Cart.update_cart_item(current_user.id, pid, new_quantity)
            return jsonify({'message': 'Update successful'}), 200
        else:
            return jsonify({'error': 'User not authenticated'}), 401
    except Exception as e:
        return jsonify({'error': 'Unexpected error'}), 500

@bp.route('/delete-cart-item/<int:pid>', methods=['DELETE', 'GET'])
def delete_cart_item(pid):
    try:
        if current_user.is_authenticated:
            Cart.delete_cart_item(current_user.id, pid)
            return jsonify({'message': 'Update successful'}), 200
        else:
            return jsonify({'error': 'User not authenticated'}), 401
    except Exception as e:
        return jsonify({'error': 'Unexpected error'}), 500

@bp.route('/submit-order', methods=['GET', 'POST'])
def submit_order():
    try:
        if current_user.is_authenticated:
            avail_balance = current_user.balance
            all_cart_items = Cart.get_cart_items(current_user.id)
            total_price = 0
            items_not_enough = []
            items_unavailable = []
            if len(all_cart_items) == 0:
                flash('No items in cart')
                return redirect(url_for('cart.cart'))
            for item in all_cart_items:
                quantity_requested = item[3]
                unit_price = item[7]
                total_price += quantity_requested * unit_price
                prod_id = item[2]
                prod_name = item[6]
                prod_details = Product.get(prod_id) 
                if not prod_details.available:
                    items_unavailable.append(prod_name)
                    continue
                if prod_details.quantity < quantity_requested:
                    items_not_enough.append(prod_name)
            if len(items_unavailable) > 0:
                flash('The following item(s) are unavailable; please take them out of your cart:')
                for i in items_unavailable:
                    flash(i)
            if len(items_not_enough) > 0:
                flash('Not enough inventory for the following items; please adjust quantities in cart:')
                for i in items_not_enough:
                    flash(i)
                return redirect(url_for('cart.cart'))
            if total_price > avail_balance:
                flash('Insufficient funds; check your balance')
                return redirect(url_for('cart.cart'))
            now = datetime.datetime.now()
            order_items = all_cart_items
            for item in all_cart_items:
               Cart.submit_cart_item(current_user.id, item[2], now, item[3], item[7], current_user.order_number) 
        else:
            order_items = None
        # return redirect(url_for('cart.cart'))
        return render_template('orders.html',
                           order_items=order_items)
    except Exception as e:
        print(f"Error rendering template: {e}")
        return jsonify({'error': 'Unexpected error'}), 500

@bp.route('/order/<int:oid>', methods=['GET'])
def order_detail(oid):
    try:
        if current_user.is_authenticated:
            order_items = Purchase.get_all_by_oid(oid, current_user.id)
            print(order_items)
        else:
            order_items = None
        return render_template('orders.html',
        order_items=order_items)
    except Exception as e:
        print(f"Error rendering template: {e}")
        return jsonify({'error': 'Unexpected error'}), 500
