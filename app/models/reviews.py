from flask import current_app as app

class Review:
    def __init__(self, id, uid, pid, review_time, review_rating, review_content = ""):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.review_time = review_time
        self.review_content = review_content
        self.review_rating = review_rating
        #self.review_image = review_image

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