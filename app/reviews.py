from flask import render_template
from flask_login import current_user
import datetime

from .models.reviews import Review

from flask import Blueprint

bp = Blueprint('reviews', __name__)

@bp.route('/reviews/<int:uid>', methods=['GET'])
def get_review_by_uid(uid):
    if current_user.is_authenticated:
        reviews = Review.get_all_by_uid(uid)
    else:
        reviews = None
    return render_template('review.html', review_history=reviews)