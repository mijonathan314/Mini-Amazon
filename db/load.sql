\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_id_seq',
                         (SELECT MAX(id)+1 FROM Orders),
                         false);

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV


\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.carts_id_seq',
                         (SELECT MAX(id)+1 FROM Carts),
                         false);

\COPY Reviews FROM 'Reviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.reviews_id_seq',
                         (SELECT MAX(id)+1 FROM Reviews),
                         false);

\COPY Review_Feedback FROM 'Review_Feedback.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Seller_Reviews FROM 'Seller_Reviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.seller_reviews_id_seq',
                         (SELECT MAX(id)+1 FROM Seller_Reviews),
                         false);