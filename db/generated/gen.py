import random
from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 1250
num_purchases = 1250
num_cart_items = 30
num_reviews = 3000
num_seller_reviews = 1000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['address']
            seller = False if uid % 2 == 0 else True
            balance = uid
            order_number = 0
            writer.writerow([uid, email, password, firstname, lastname, address, seller, balance, order_number])
        print(f'{num_users} generated')
    return

product_dict = {} #maps product id to seller id (user)

def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            product_dict[pid] = uid
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=1, max=1000)
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            category = fake.sentence(nb_words=1)[:-1]
            description = fake.sentence(nb_words=30)[:-1]
            writer.writerow([pid, uid, name, price, quantity, available, category, description])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

#available_to_review starts as purchase_dict, but then pids are removed as 
#users make reviews such that when prevent the user from making another review for a product
#they have already reviewed
def gen_reviews(num_reviews, available_to_review, feedback_dict):
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for rid in range(num_reviews):
            if rid % 100 == 0:
                print(f'{rid}', end=' ', flush=True)
            if len(available_to_review.keys()) == 0:
                continue
            uid = random.choice(list(available_to_review.keys()))
            pid = random.choice(list(available_to_review[uid])) #choose random element from available_to_review[uid]
            available_to_review[uid].remove(pid)
            #print(uid, pid)
            if len(available_to_review[uid]) == 0:
                available_to_review.pop(uid)
            #remove the pid from the set purchase_dict[uid] so that the next time around, the user can't make
            #a review for a product they have already reviewed
            review = fake.sentence(nb_words=8)
            rating = fake.random_int(min=1, max=5)
            time_reviewed = fake.date_time()
            thumbs_up = feedback_dict[rid][0]
            thumbs_down = feedback_dict[rid][1]
            img = None
            writer.writerow([rid, uid, pid, time_reviewed, rating, thumbs_up, thumbs_down, img, review])
        print(f'{num_reviews} generated')
    return

#Have it such that the number of likes and dislikes in reviews table is dependent on feedback_review generation
def gen_review_feedback():
    with open('Review_feedback.csv', 'w') as f:
        #This dictionary maps the review id to an array with two ints,
        #The first int is the number of likes, and second int is the number of dislikes
        feedback_dict = {}
        writer = get_csv_writer(f)
        print('Review_Feedback...', end=' ', flush=True)
        for rid in range(2467):
            for uid in range(num_users):
                mapper = random.randint(0, 19)
                liked = False
                disliked = False
                if mapper == 0: liked = True
                elif mapper == 1: disliked = True
                else:
                    continue

                if rid not in feedback_dict:
                    toAdd = [0, 0]
                    if liked == True: toAdd = [1, 0]
                    if disliked == True: toAdd = [0, 1]
                    feedback_dict[rid] = toAdd
                else:
                    if liked == True: 
                        feedback_dict[rid][0] = feedback_dict[rid][0] + 1
                    if disliked == True: 
                        feedback_dict[rid][1] = feedback_dict[rid][1] + 1

                writer.writerow([rid, uid, liked, disliked])
        print(feedback_dict)
        print('feedback_review generated')
        return feedback_dict
    

    
def gen_seller_reviews(num_seller_reviews):
    repeats = {} #maps buyer:seller
    with open('Seller_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller_Reviews...', end=' ', flush=True)
        for rid in range(num_seller_reviews):
            print("rid", rid)
            helper(writer, rid, repeats)
            

def helper(writer, rid, repeats):
    for pid, buyers in buyer_dict.items():
        for buyer in buyers:
            seller = product_dict[pid]
            if f"{buyer}:{seller}" in repeats:
                continue
            chance = random.randint(0, 10)
            if chance == 1:
                time_reviewed = fake.date_time()
                review = fake.sentence(nb_words=8)
                rating = fake.random_int(min=1, max=5)
                writer.writerow([rid, buyer, seller, time_reviewed, rating, review])
                repeats[f"{buyer}:{seller}"] = 1
                return
                
                        
            

def gen_orders(num_purchases):
    with open('Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('orders...', end=' ', flush=True)
        for id in range(num_purchases):
            user_id = fake.random_int(min=0, max=num_users-1)
            time_stamp = fake.date_time()
            total_items = fake.random_int(min=1, max=50)
            total_price = fake.random_int(min=0, max=10000)

            writer.writerow([id, user_id, total_price, total_items, time_stamp])
        print('generated orders')
    return

buyer_dict = {} #product mapped to set of buyers who bought it

def gen_purchases(num_purchases, available_pids):
    purchase_dict = {} #dictionary mapping uid to array of pids that the user has purchased
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases, num_purchases*2):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            if uid not in purchase_dict:
                toAdd = {pid}
                purchase_dict[uid] = toAdd
            else:
                purchase_dict[uid].add(pid)
            if pid not in buyer_dict:
                buyer_dict[pid] = {uid}
            else:
                buyer_dict[pid].add(uid)
            quantity = fake.random_int(min=0, max=50)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            fulfillment_status = fake.random_element(elements=('ordered', 'shipped', 'delivered'))
            time_purchased = fake.date_time()
            time_fulfillment_updated = fake.date_time()
            order_id = id
            writer.writerow([id, uid, pid, quantity, price, fulfillment_status, time_purchased, time_fulfillment_updated, order_id])
        print(f'{num_purchases} generated')
    return purchase_dict





def gen_cart_items(num_items, available_pids):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart Items...', end=' ', flush=True)
        for id in range(num_items):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            #uid = fake.random_int(min=0, max=num_users-1)
            uid = 0
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=1, max=20)
            order_time = fake.date_time()
            writer.writerow([id, uid, pid, quantity, False, False, order_time])
        print(f'{num_items} generated')
    return num_items

gen_users(num_users)
available_pids = gen_products(num_products)
gen_orders(num_purchases)

purchase_dict = gen_purchases(num_purchases, available_pids)
#print(purchase_dict)

gen_cart_items(num_cart_items, available_pids)
#assign purchases/products to data structure and then use those to 
#make sure your reviews are fulfilling constraints
feedback_dict = gen_review_feedback()
gen_seller_reviews(num_seller_reviews)
gen_reviews(num_reviews, purchase_dict, feedback_dict) #don't add stuff after this function


