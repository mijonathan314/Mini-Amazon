from flask import render_template, flash
from flask_login import current_user
import datetime
from flask import jsonify

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.order import Order

from flask import Blueprint, request, redirect, url_for
bp = Blueprint('cart', __name__)

# @bp.route('/add-order', methods=['GET', 'POST'])
# def add_order():
