import binascii
from flask import current_app as app
import codecs

class Review:
    def __init__(self, id, uid, pid, review_time, review_rating, thumbs_up, thumbs_down, imagepath = "", review = ""):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.review_time = review_time
        self.review = review
        self.thumbs_up = thumbs_up
        self.thumbs_down = thumbs_down
        self.imagepath = imagepath
        self.review_rating = review_rating
        #self.review_image = review_image

    @staticmethod
    # Function to get all product reviews mapped to a user id given a user id
    def get_review_by_id(id):
        rows = app.db.execute (
            '''
            SELECT *
            FROM Reviews
            WHERE id=:id
            ''',
            id=id
        )
        return rows
    
    @staticmethod
    # Function to get all product reviews mapped to a user id given a user id
    def get_review_by_uid_pid(uid, pid):
        rows = app.db.execute (
            '''
            SELECT *
            FROM Reviews
            WHERE uid=:uid
            AND pid=:pid
            ''',
            uid=uid,
            pid=pid
        )
        return [Review(*row) for row in rows][0]

    @staticmethod
    # Function to get all product reviews mapped to a user id given a user id
    def get_all_by_uid(uid):
        rows = app.db.execute (
            '''
            SELECT *
            FROM Reviews
            WHERE buyer_id = :uid
            ORDER BY review_time DESC
            ''',
            uid=uid
        )
        return [Review(*row) for row in rows]
    
    @staticmethod
    def get_all_by_seller_id_with_product_info(uid):
        rows = app.db.execute (
            '''
            SELECT Reviews.review_time, Reviews.rating, Reviews.review, Products.name
            FROM Reviews, Products
            WHERE Reviews.product_id = Products.id
            AND Products.user_id = :uid
            ORDER BY review_time DESC
            ''',
            uid=uid
        )
        return rows
    
    @staticmethod
    def get_all_by_pid(pid):
        rows = app.db.execute (
            '''
            SELECT *
            FROM Reviews
            WHERE product_id = :pid
            ORDER BY review_time DESC
            ''',
            pid = pid
        )
        return [Review(*row) for row in rows]
    
    @staticmethod
    def get_all_by_pid_order_by_likes(pid):
        rows = app.db.execute (
            '''
            SELECT *
            FROM Reviews
            WHERE product_id = :pid
            ORDER BY thumbs_up DESC
            ''',
            pid = pid
        )
        return [Review(*row) for row in rows]
    
    def get_review(uid, pid):
        # TODO
        pass
    
    @staticmethod
    def add_review(uid, pid, time, rating, thumbs_up, thumbs_down, imagepath, review):
        # Convert image data to hexadecimal string
        #img_hex = binascii.hexlify(img).decode('utf-8') if img else None

        app.db.execute(
            '''INSERT INTO Reviews (buyer_id, product_id, review_time, rating, thumbs_up, thumbs_down, imagepath, review) 
            VALUES (:uid, :pid, :time, :rating, :thumbs_up, :thumbs_down, :imagepath, :review)''',
            uid=uid,
            pid=pid,
            time=time,
            rating=rating,
            thumbs_up=thumbs_up,
            thumbs_down=thumbs_down,
            imagepath=imagepath,  # Use the hexadecimal string
            review=review
        )

    #returns a boolean that is true if user already reviewed this product, and false otherwise
    def check_review(uid, pid):
        #fetches the tuples in Reviews where uid=uid and pid=pid
        rows = app.db.execute (
            '''
            SELECT *
            FROM Reviews
            WHERE buyer_id = :uid
            AND product_id = :pid
            ''',
            uid=uid,
            pid=pid
        )
        #Check if the array of rows is greater than 0. If so, then it exists in Reviews already
        row_list = [Review(*row) for row in rows]
        if len(row_list) > 0:
            return True
        return False

    def update_review(uid, pid, review, rating, time):
        #change your review
        pass

    def delete_review(uid, pid):
        #TODO delete existing review
        rows = app.db.execute (
            '''DELETE FROM Reviews 
            WHERE buyer_id = :uid
            AND product_id = :pid''',
            uid=uid,
            pid=pid
        )

    def update_feedback(id, thumbs_up, thumbs_down):
        app.db.execute (
            '''
            UPDATE Reviews
            SET thumbs_up = :thumbs_up, thumbs_down = :thumbs_down
            WHERE id=:id
            ''',
            id=id,
            thumbs_up=thumbs_up,
            thumbs_down=thumbs_down
        )

    def remove_image_from_product_review(uid, pid):
        '''
        Disassociate an image from a product review
        '''
        rows = app.db.execute(
            """
            UPDATE Reviews
            SET imagepath = :imagepath
            WHERE uid=:uid
            AND pid=:pid
            """,
            uid=uid,
            pid=pid, 
            imagepath = ""
        )
 
    def replace_image(uid, pid, imagepath):
        '''
        Replace an image with a different image
        '''
        app.db.execute(
            """
            UPDATE Reviews
            SET imagepath = :imagepath
            WHERE uid = :uid
            AND pid=:pid
            """,
            uid=uid,
            pid=pid,
            imagepath = imagepath
        )
 

"""
CREATE TABLE Reviews(
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    buyer_id INT NOT NULL REFERENCES Users (id),
    product_id INT NOT NULL REFERENCES Products(id), --do I need REFERENCES?,
    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    thumbs_up INT NOT NULL,
    thumbs_down INT NOT NULL,
    img BYTEA NOT NULL,
    review VARCHAR(255) 
);
"""
    
   