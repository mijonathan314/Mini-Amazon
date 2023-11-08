-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
     address VARCHAR NOT NULL,
    seller BOOLEAN DEFAULT FALSE,
    balance REAL DEFAULT 0 CHECK(balance >= 0) NOT NULL
);


CREATE TABLE if not exists Orders (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    total_price REAL NOT NULL CHECK(total_price >= 0),
    total_items INT NOT NULL CHECK(total_items > 0),
    time_stamp timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    quantity INT NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE if not exists Purchases (
    id INT NOT NULL REFERENCES Orders(id),
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL CHECK(quantity >= 0),
    fulfillment_status VARCHAR NOT NULL CHECK(fulfillment_status in ('ordered', 'shipped', 'delivered')) 
);

CREATE TABLE Carts (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL CHECK(quantity >= 0),
    fulfilled BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Reviews(
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    buyer_id INT NOT NULL REFERENCES Users (id),
    product_id INT NOT NULL REFERENCES Products (id),
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_time timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

