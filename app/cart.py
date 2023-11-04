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
    # get all items in user's cart
    if current_user.is_authenticated:
        cart_items = Cart.get_cart_items(current_user.id)
    else:
        cart_items = None

    return render_template('cart.html',
                           cart_items=cart_items)

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

