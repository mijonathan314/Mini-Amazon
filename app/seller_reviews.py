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
from .models.review_feedback import Review_Feedback

from flask import Blueprint

bp = Blueprint('seller_reviews', __name__)

#Opens up the review html page for user to submit review and rating
@bp.route('/leaveSellerReview/<int:uid>/<int:pid>', methods=['GET'])
def leave_review_by_uid_pid(uid, pid):
    if current_user.is_authenticated:
        print('hereawref')
        return render_template('leaveSellerReview.html', uid=uid, pid=pid)

#Opens up the review html page for user to edit review and rating
@bp.route('/editReview/<int:rid>/<int:uid>/<int:sid>', methods=['GET'])
def init_edit_review_by_uid_sid(rid, uid, sid):
    if current_user.is_authenticated:
        return render_template('editReview.html', rid=rid, uid=uid, sid=sid)
    
#Deletes review
@bp.route('/deleteReview/<int:rid>/<int:uid>/<int:sid>', methods=['GET'])
def delete_review_by_uid_pid(rid, uid, sid):
    if current_user.is_authenticated:
        Review_Seller_Feedback.delete_all_feedback_by_rid(rid)
        Seller_Review.delete_review(uid, sid)
    return redirect('/')

#Send review and rating to the backend
@bp.route('/submitSellerReview/<int:uid>/<int:pid>', methods=['POST']) #submitReview never used?
def send_seller_review_by_uid_pid(uid, pid):
    #grab information from html form
    #what the user inputs has a unique id
    print("send seller review")
    if current_user.is_authenticated:

        #check who sells this product
        seller = Seller_Review.find_seller_by_product(pid)
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
            Seller_Review.add_review(uid, pid, time_formatted, rating, 0, 0, review)
            #Review.get_review(uid, pid)
            return redirect('/')
'''    
#Edit review by deleting the existing review and adding a new review
@bp.route('/submitEditedReview/<int:rid>/<int:uid>/<int:pid>', methods=['POST']) #submitReview never used?
def edit_review_by_uid_sid(rid, uid, sid):
    if current_user.is_authenticated:
        review = request.form["review"]
        rating = request.form["rating"]
        time_formatted = time.strftime('%Y-%m-%d %H:%M:%S')
        Review_Seller_Feedback.delete_all_feedback_by_rid(rid)
        Seller_Review.delete_review(uid, sid)
        Seller_Review.add_review(uid, sid, time_formatted, rating, 0, 0, review)
        return redirect('/')
''' 


# @bp.route('/myReviews/<int:uid>', methods=['GET'])
# def see_my_seller_reviews(uid):
#     '''if current_user.is_authenticated:
#         return render_template('myReviews.html', uid=uid)'''
#     if current_user.is_authenticated:
#         reviews = Seller_Review.get_all_by_uid(uid)
#     else:
#         reviews = None
#     return render_template('myReviews.html', review_history=reviews) #huh?
'''
@bp.route('/summaryRatingSeller/<int:sid>', methods=['GET'])
def see_seller_reviews(sid):
    if current_user.is_authenticated:
        reviews = Seller_Review.get_all_by_sid(sid)
        top_reviews = Review.get_all_by_pid_order_by_likes(pid)
        top_three_reviews = []
        top_three_review_ids = []
        other_reviews = []
        # avg_rating = Product.get_avg_rating_by_pid(pid)
        # num_reviews = Product.get_num_reviews_by_pid(pid)
        review_feedbacks = Review_Feedback.get_all_feedback(current_user.id)


        avg_rating = 0
        num_reviews = 0

        for i in range(len(top_reviews)):
            if i < 3:
                avg_rating = avg_rating + top_reviews[i].review_rating
                num_reviews = num_reviews + 1
                top_three_reviews.append(top_reviews[i])
                top_three_review_ids.append(top_reviews[i].id)
                top_reviews[i].liked = False
                top_reviews[i].disliked = False
                print("id of top review", top_reviews[i].id)
                print("thumps up", top_reviews[i].thumbs_up)
                for feedback in review_feedbacks:
                    if feedback.id == top_reviews[i].id:
                        top_reviews[i].liked = feedback.liked
                        top_reviews[i].disliked = feedback.disliked
                        print("likes", top_reviews[i].liked)
                        print("dislikes", top_reviews[i].disliked)
                        
                        break
            else: break

        for review in reviews:
            if review.id not in top_three_review_ids:
                avg_rating = avg_rating + review.review_rating
                num_reviews = num_reviews + 1
                other_reviews.append(review)
                review.liked = False
                review.disliked = False
                print("id of other review", top_reviews[i].id)
                print("review time", review.review_time)
                for feedback in review_feedbacks:
                    if feedback.id == review.id:
                        review.liked = feedback.liked
                        review.disliked = feedback.disliked
                        print("likes", review.liked)
                        print("dislikes", review.disliked)
                        break
        for review in top_three_reviews: print(review.id)
        for review in other_reviews: print(review.id)

        
        
        # currReview = 0
        # for i in range(len(reviews)):
        #     if currReview < 3: #Get the top three highest rated reviews by likes
        #         avg_rating = avg_rating + top_reviews[i].review_rating
        #         num_reviews = num_reviews + 1
        #         if top_reviews[i] in reviews:
        #             reviews.remove(top_reviews[i])
        #     else:
        #         avg_rating = avg_rating + reviews[i].review_rating
        #         num_reviews = num_reviews + 1

            # for review_feedback in review_feedbacks:
            #     if review.id == review_feedback.id:
            #         review.my_thumb_up = review_feedback.liked
            #         review.my_thumb_down = review_feedback.disliked

        if num_reviews == 0: avg_rating = 0
        else: avg_rating = avg_rating / num_reviews
        #print("average rating: ", avg_rating)
        #print("number of reviews: ", num_reviews)
        #print("pid: ", pid)
        #print("review_feedbacks: ", review_feedbacks)
    else:
        reviews = None
    return render_template('summaryRatingProd.html', top_three_reviews = top_three_reviews, prod_reviews = other_reviews, review_feedbacks = review_feedbacks, my_avg = avg_rating, my_num = num_reviews)

@bp.route('/summaryRatingProd/<int:id>/<int:numLikes>/<int:numDislikes>/<int:userFeedback>', methods=['PATCH'])
def update_review_feedback(id, numLikes, numDislikes, userFeedback):
    try:
        if current_user.is_authenticated:
            print("id", id)
            print("numLikes", numLikes)
            print("numDislikes", numDislikes)
            print("userFeedback", userFeedback)
            print("current_user.id", current_user.id)
            Review.update_feedback(id, numLikes, numDislikes)
            print("update_feedback Review Succeeded")
            if Review_Feedback.check_feedback_by_rid_uid(id, current_user.id):
                Review_Feedback.update_feedback_for_review(id, current_user.id, userFeedback)
            else:
                Review_Feedback.insert_feedback_for_review(id, current_user.id, userFeedback)
            print("update_feedback_for_review Review_Feedback succeeded\n")
            return jsonify({'message': 'Update successful'}), 200
        else:
            return jsonify({'error': 'User not authenticated'}), 401
    except Exception as e:
        print(e)
        return jsonify({'error': 'Unexpected error'}), 500
    

@bp.route('/upload_photo/<int:uid>/<int:pid>', methods=['GET', 'POST'])
def upload_photo(uid, pid):
    print("hi")
    review = Review.get_review_by_uid_pid(uid, pid)
    #upload a photo associated with the review with this product_review_id
   
    if request.method == 'POST':  
        f = request.files['file']
        filepath = os.path.join("app/static",f.filename)
        f.save(filepath)
        #Then add this filepath to the product table
        Review.replace_image(uid, pid, "/static/"+str(f.filename))
        
        #return redirect(url_for('reviews.look_at_product_review_and_edit_product_review', uid = review.uid, product_id = review.pid))
    #return redirect(url_for('reviews.look_at_product_review_and_edit_product_review', uid = review.uid, product_id = review.pid))
   
# @bp.route('/delete_photo/<int:product_review_id>', methods=['GET', 'POST'])
# def remove_image_from_prod_review(product_review_id):
#     review = Review_Of_Product.get_review(product_review_id)
#     Review_Of_Product.remove_image_from_product_review(product_review_id)
#     return redirect(url_for('reviews.look_at_product_review_and_edit_product_review', uid = review.uid, product_id = review.pid))
    


# def get_average_rating(pid):
#     if current_user.is_authenticated:
#         average_rating = Review.get_avg_rating_by_pid(pid)
#     else:
#         average_rating = None
#     return average_rating
    
    
'''