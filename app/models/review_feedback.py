from flask import current_app as app

class Review_Feedback:
    def __init__(self, id, feedbacker_id, liked, disliked):
        self.id = id
        self.feedbacker_id = feedbacker_id
        self.liked = liked
        self.disliked = disliked

    #get all feedback for feedbacker
    @staticmethod
    def get_all_feedback(feedbacker_id):
        rows = app.db.execute (
            '''
            SELECT *
            FROM Review_Feedback
            WHERE feedbacker_id=:feedbacker_id
            ''',
            feedbacker_id=feedbacker_id
        )
        return [Review_Feedback(*row) for row in rows]
    
    #Check if a user has already given feedback on a review
    @staticmethod
    def check_feedback_by_rid_uid(id, feedbacker_id):
        rows = app.db.execute (
            '''
            SELECT *
            FROM Review_Feedback
            WHERE id = :id
            AND feedbacker_id = :feedbacker_id
            ''',
            id=id,
            feedbacker_id=feedbacker_id
        )
        #Check if the array of rows is greater than 0. If so, then it exists in Reviews already
        row_list = [Review_Feedback(*row) for row in rows]
        if len(row_list) > 0:
            return True
        return False
    
    @staticmethod
    def update_feedback_for_review(id, feedbacker_id, userFeedback):
        liked = None
        disliked = None
        if userFeedback == 0:
            liked = False
            disliked = True
        elif userFeedback == 1:
            liked = True
            disliked = False
        elif userFeedback == 2:
            liked = False
            disliked = False
        else: raise ValueError("Invalid user feedback = -1")

        app.db.execute(
            '''
            UPDATE Review_Feedback
            SET liked = :liked, disliked = :disliked
            WHERE id = :id
            AND feedbacker_id = :feedbacker_id
            ''',
            id=id,
            feedbacker_id=feedbacker_id,
            liked=liked,
            disliked=disliked
        )

    #Only difference b/w this and update is that we only insert when
    #the feedbacker has never given feedback on this review,
    #in which there is nothing to update, which is why we insert
    @staticmethod
    def insert_feedback_for_review(id, feedbacker_id, userFeedback):
        liked = None
        disliked = None
        if userFeedback == 0:
            liked = False
            disliked = True
        elif userFeedback == 1:
            liked = True
            disliked = False
        elif userFeedback == 2:
            liked = False
            disliked = False
        else: raise ValueError("Invalid user feedback = -1")

        app.db.execute(
            '''
            INSERT INTO Review_Feedback (id, feedbacker_id, liked, disliked)
            VALUES (:id, :feedbacker_id, :liked, :disliked)
            ''',
            id=id,
            feedbacker_id=feedbacker_id,
            liked=liked,
            disliked=disliked
        )

    @staticmethod
    def delete_all_feedback_by_rid(id):
        app.db.execute(
            '''
            DELETE FROM Review_Feedback
            WHERE id=:id
            ''',
            id=id
        )

        
