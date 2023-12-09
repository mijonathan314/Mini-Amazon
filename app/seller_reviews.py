import base64
from io import BytesIO
import os
from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
from flask import jsonify
from flask import send_file
import codecs
import time
import datetime

from .models.seller_reviews import Seller_Review

from flask import Blueprint

bp = Blueprint('seller_reviews', __name__)

#Opens up the review html page for user to submit review and rating
@bp.route('/leaveSellerReview/<int:uid>/<int:pid>', methods=['GET'])
def leave_review_by_uid_pid(uid, pid):
    if current_user.is_authenticated:
        print('hereawref')
        return render_template('leaveSellerReview.html', uid=uid, pid=pid)

#Opens up the review html page for user to edit review and rating
@bp.route('/editSellerReview/<int:rid>/<int:uid>/<int:sid>', methods=['GET'])
def init_edit_seller_review_by_uid_sid(rid, uid, sid):
    if current_user.is_authenticated:
        return render_template('editSellerReview.html', rid=rid, uid=uid, sid=sid)
    
#Deletes review
@bp.route('/deleteSellerReview/<int:rid>', methods=['GET'])
def delete_seller_review_by_uid_pid(rid):
    if current_user.is_authenticated:
        Seller_Review.delete_review(rid)
    return redirect('/')

#Send review and rating to the backend
@bp.route('/submitSellerReview/<int:uid>/<int:pid>', methods=['POST']) #submitReview never used?
def send_seller_review_by_uid_pid(uid, pid):
    #grab information from html form
    #what the user inputs has a unique id
    print("send seller review")
    if current_user.is_authenticated:

        #check who sells this product
        seller = Seller_Review.find_seller_by_product(pid)[0]
        print(seller)

        #check if user has already added review for this seller
        if Seller_Review.check_review(uid, seller) == True:
            #raise error
            return render_template('reviewError.html', uid=uid, sid=seller)
        else:
            review = request.form["review"]
            rating = request.form["rating"]
            time_formatted = time.strftime('%Y-%m-%d %H:%M:%S')
            # submit to the database
            Seller_Review.add_review(uid, seller, time_formatted, rating, review)
            #Review.get_review(uid, pid)
            return redirect('/')
  
#Edit review by deleting the existing review and adding a new review
@bp.route('/submitEditedSellerReview/<int:rid>/<int:uid>/<int:sid>', methods=['POST']) #submitReview never used?
def edit_seller_review_by_rid(rid, uid, sid):
    if current_user.is_authenticated:
        review = request.form["review"]
        rating = request.form["rating"]
        time_formatted = time.strftime('%Y-%m-%d %H:%M:%S')
        Seller_Review.delete_review(rid)
        Seller_Review.add_review(uid, sid, time_formatted, rating, review)
        return redirect('/')



@bp.route('/mySellerReviews/<int:uid>', methods=['GET'])
def see_my_seller_reviews(uid):
    '''if current_user.is_authenticated:
        return render_template('myReviews.html', uid=uid)'''
    if current_user.is_authenticated:
        reviews = Seller_Review.get_all_by_uid(uid)
    else:
        reviews = None
    return render_template('mySellerReviews.html', seller_review_history=reviews) #huh?

@bp.route('/summaryRatingSeller/<int:pid>', methods=['GET'])
def see_seller_reviews(pid):
    if current_user.is_authenticated:
        seller = Seller_Review.find_seller_by_product(pid)[0]
        reviews = Seller_Review.get_all_by_sid(seller)
        # avg_rating = Product.get_avg_rating_by_pid(pid)
        # num_reviews = Product.get_num_reviews_by_pid(pid)
        avg_rating = 0
        num_reviews = 0

        for review in reviews:
            avg_rating = avg_rating + review.review_rating
            num_reviews = num_reviews + 1

        if num_reviews == 0: avg_rating = 0
        else: avg_rating = avg_rating / num_reviews
    else:
        reviews = None
    return render_template('summaryRatingSeller.html', seller_reviews=reviews, my_avg = avg_rating, my_num = num_reviews)
