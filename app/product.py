from flask import render_template, flash
from flask_login import current_user
import datetime
from flask import jsonify, request

from .models.product import Product
from .models.cart import Cart

from flask import Blueprint, redirect, url_for
bp = Blueprint('product', __name__)


@bp.route('/product', methods=['POST'])
def get_top_products():
    if request.method == 'POST':
        k = int(request.form.get('k-value', 1))  # Get the value of k from the form
    else:
        k = 0  # Default value if no input provided

    
    products = Product.get_top_expensive_products(k)
    

    return render_template('products.html', top_product=products)

@bp.route('/get_by_category', methods=['POST'])
def get_by_category():
    category = request.form['category'].strip()  # Get the category from the form input
    
    filtered_products = Product.get_by_category(category)

    # Render the same products page or a specific category page with the filtered products
    return render_template('products.html', top_product=filtered_products)

@bp.route('/get_by_keyword', methods=['POST'])
def get_by_keyword():
    keyword = request.form['keyword'].strip()  # Get the keyword from the form input
    
    filtered_products = Product.get_by_name_keyword(keyword)
    

    # Render the same products page with the filtered products
    return render_template('products.html', top_product=filtered_products)

@bp.route('/get_by_quantity', methods=['POST'])
def get_by_quantity():
    k = int(request.form.get('k-value', 0))  # Get the value of k from the form
    products = Product.get_top_products_by_quantity(k)
    return render_template('products.html', top_product=products)


@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.get(product_id)
    sellers = Product.get_product_sellers(product_id)
    return render_template('productDescription.html', product=product, sellers=sellers)

@bp.route('/add-to-cart/<int:product_id>/<int:seller_id>', methods=['POST'])
def add_to_cart(product_id, seller_id):
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not authenticated'}), 401

    try:
        quantity = int(request.form.get('quantity', 0))
        if quantity <= 0:
            return jsonify({'error': 'Invalid quantity'}), 400

        Cart.add_item_to_cart(current_user.id, product_id, quantity)
        product = Product.get(product_id)
        sellers = Product.get_product_sellers(product_id)

        flash('Item added to cart')
        return render_template('productDescription.html', product=product, sellers=sellers)


    except ValueError:
        return jsonify({'error': 'Quantity must be a number'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@bp.route('/create-product', methods=['POST'])
def create_product():
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not authenticated'}), 401

    try:
        name = request.form.get('name')
        price = float(request.form.get('price'))
        quantity = int(request.form.get('quantity'))
        category = request.form.get('category')
        description = request.form.get('description')

        new_product_id = Product.add_new_product(name, price, quantity, category, description, current_user.id)

        
        # Fetch updated list of products
        products = Product.get_all(available=True)
        return render_template('products.html', top_product=products)

    except Exception as e:
        products = Product.get_all(available=True)
        return render_template('products.html', top_product=products)




