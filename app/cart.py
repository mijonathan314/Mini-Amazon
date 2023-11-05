from flask import render_template
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

    else:
        cart_items = None
        page = None
        total_pages = None

    return render_template('cart.html',
                           cart_items=cart_items, page=page, total_pages=total_pages)

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

