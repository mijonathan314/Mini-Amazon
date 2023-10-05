from flask import render_template
from flask import current_app as app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from .models.seller import Inventory

from flask import Blueprint
bp = Blueprint('inventory', __name__)


@bp.route('/seller', methods=['GET'])

def seller():
    # get all available products for sale:
    if current_user.is_authenticated:
        inventory = Inventory.get_all_inventories_by_user(current_user.id)
    else:
        inventory = None
    # render the page by adding information to the index.html file
    return render_template('inventory.html',
                           all_products = inventory)
