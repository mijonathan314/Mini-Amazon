from flask import render_template
from flask_login import current_user
import datetime

from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchases', __name__)


@bp.route('/purchases/<int:uid>', methods=['GET'])
def get_purchases_by_uid(uid):
    # find the products the user has purchased given uid
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid(uid)
    else:
        purchases = None
    return render_template('purchases.html', purchase_history=purchases)
