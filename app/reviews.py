from flask import render_template
from flask_login import current_user
from flask import request, redirect, url_for
import time
import datetime

from .models.reviews import Review

from flask import Blueprint

bp = Blueprint('reviews', __name__)

#Opens up the review html page for user to submit review and rating
@bp.route('/leaveReview/<int:uid>/<int:pid>', methods=['GET'])
def leave_review_by_uid_pid(uid, pid):
    if current_user.is_authenticated:
        return render_template('leaveReview.html', uid=uid, pid=pid)
    
#Opens up the review html page for user to edit review and rating
@bp.route('/editReview/<int:uid>/<int:pid>', methods=['GET'])
def init_edit_review_by_uid_pid(uid, pid):
    if current_user.is_authenticated:
        return render_template('editReview.html', uid=uid, pid=pid)
    
#Deletes review
@bp.route('/deleteReview/<int:uid>/<int:pid>', methods=['GET'])
def delete_review_by_uid_pid(uid, pid):
    if current_user.is_authenticated:
        Review.delete_review(uid, pid)
    return redirect('/')

#Send review and rating to the backend
@bp.route('/submitReview/<int:uid>/<int:pid>', methods=['POST']) #submitReview never used?
def send_review_by_uid_pid(uid, pid):
    #grab information from html form
    #what the user inputs has a unique id
    if current_user.is_authenticated:
        review = request.form["review"]
        rating = request.form["rating"]
        #time = datetime.datetime.now()
        #time_formatted = f"{time.year}-{str(time.month).zfill(2)}-{str(time.day).zfill(2)} {str(time.hour).zfill(2)}:{str(time.minute).zfill(2)}:{str(time.second).zfill(2)}" 
        #print(time_formatted)
        time_formatted = time.strftime('%Y-%m-%d %H:%M:%S')
        #see zfill for formatting information
        # submit to the database
        Review.add_review(uid, pid, review, rating, time_formatted)
        #Review.get_review(uid, pid)
        return redirect('/')
    
#Edit review by deleting the existing review and adding a new review
@bp.route('/submitEditedReview/<int:uid>/<int:pid>', methods=['POST']) #submitReview never used?
def edit_review_by_uid_pid(uid, pid):
    if current_user.is_authenticated:
        review = request.form["review"]
        rating = request.form["rating"]
        time_formatted = time.strftime('%Y-%m-%d %H:%M:%S')
        Review.delete_review(uid, pid)
        Review.add_review(uid, pid, review, rating, time_formatted)
        return redirect('/')
    
@bp.route('/myReviews/<int:uid>', methods=['GET'])
def see_my_reviews(uid):
    '''if current_user.is_authenticated:
        return render_template('myReviews.html', uid=uid)'''
    if current_user.is_authenticated:
        reviews = Review.get_all_by_uid(uid)
    else:
        reviews = None
    return render_template('myReviews.html', review_history=reviews) #huh?
    
    
