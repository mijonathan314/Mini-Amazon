from flask import render_template, redirect, url_for, flash, request
from flask import current_app as app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.product import Product
from .models.seller import Inventory, Fulfillment, moreProduct, Popular, Sales

from flask import Blueprint
bp = Blueprint('inventory', __name__)


@bp.route('/seller', methods=['GET'])
@bp.route('/seller/<action>/<user_id>/<product_id>', methods=['GET', 'POST'])
@bp.route('/seller/<action>/<user_id>/<product_id>/<order_id>/<buyer_id>', methods=['GET', 'POST'])
def seller(action = None, user_id = None, product_id = None, order_id = None, buyer_id = None, quantity = 1, price = None):
    # get all available products for sale:
    if current_user.is_authenticated:
        inventory = Inventory.get_all_inventories_by_user(current_user.id)
        fulfillment = Fulfillment.get_all_fulfillment_by_user(current_user.id)
        popular = Popular.get_most_popular_by_user(current_user.id)
        sales = Sales.get_total_sales(current_user.id)
    else:
        inventory = None
        fulfillment = None
        popular = None
        sales = None
    if request.method == "POST":
        if action == 'delete':
            app.db.execute(''' 
            UPDATE Products
            SET quantity = 0, available = false
            WHERE user_id = :user_id AND id = :product_id
            ''', user_id = user_id, product_id = product_id)
            return redirect(url_for('inventory.seller'))
        if action == 'update':
            quantity = request.form['quant']
            if quantity == '':
                quantity = 1
            app.db.execute('''
            UPDATE Products
            SET quantity = :quantity, available = true
            WHERE user_id = :user_id AND id = :product_id
            ''', user_id = user_id, product_id = product_id, quantity= quantity)
            return redirect(url_for('inventory.seller'))
        if action == 'price':
            price = request.form['quant']
            if price == '':
                price = 1
            app.db.execute('''
            UPDATE Products
            SET price = :price
            WHERE user_id = :user_id AND id = :product_id
            ''', user_id = user_id, product_id = product_id, price= price)
            return redirect(url_for('inventory.seller'))
        if action == 'edit':
            print("CHECKME", buyer_id, order_id)
            app.db.execute('''
            UPDATE Purchases
            SET fulfillment_status = :fulfillment_status
            WHERE pid = :product_id
            AND uid =:buyer_id
            ''', fulfillment_status = request.form['quant'], order_id = order_id, product_id = product_id, buyer_id=buyer_id)
            return redirect(url_for('inventory.seller'))


    # render the page by adding information to the index.html file
    print("newThing")
    return render_template('inventory.html',
                           purchase_history=fulfillment,
                           all_products = inventory,
                           popular = popular,
                           sales = sales)

class AddInventoryForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Register Item')

@bp.route('/addinventory', methods=['GET', 'POST'])
def addinventory():
    user = User.get(current_user.id)   
    form = AddInventoryForm()
    if form.validate_on_submit():
        try:
            ret = moreProduct.add_product(user.id,
                        form.name.data.strip(), 
                        form.price.data.strip(),
                        form.quantity.data.strip(),
                        form.category.data.strip()
                        )
            if ret is not None:
                flash('Inventory Information Updated')
            return redirect(url_for('inventory.seller'))
        except BadUpdateException as e:
            flash(e.toString())
    return render_template('addinventory.html', form=form)