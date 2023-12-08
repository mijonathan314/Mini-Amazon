from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_cart_items = 30
num_reviews = 1000

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
            seller = False
            balance = uid
            order_number = 0
            writer.writerow([uid, email, password, firstname, lastname, address, seller, balance, order_number])
        print(f'{num_users} generated')
    return



def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            quantity = fake.random_int(min=1, max=1000)
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            category = fake.sentence(nb_words=1)[:-1]
            writer.writerow([pid, uid, name, price, quantity, available, category])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_reviews(num_reviews):
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for rid in range(num_reviews):
            if rid % 100 == 0:
                print(f'{rid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            review = fake.sentence(nb_words=8)
            rating = fake.random_int(min=1, max=5)
            time_reviewed = fake.date_time()
            writer.writerow([rid, uid, pid, review, rating, time_reviewed])
        print(f'{num_reviews} generated')
    return


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids)
            quantity = fake.random_int(min=0, max=50)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            fulfillment_status = fake.random_element(elements=('ordered', 'shipped', 'delivered'))
            time_purchased = fake.date_time()
            order_id = fake.random_int(min=0, max=num_purchases)
            writer.writerow([id, uid, pid, quantity, price, fulfillment_status, time_purchased, order_id])
        print(f'{num_purchases} generated')
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
gen_purchases(num_purchases, available_pids)
gen_cart_items(num_cart_items, available_pids)
gen_reviews(num_reviews)
