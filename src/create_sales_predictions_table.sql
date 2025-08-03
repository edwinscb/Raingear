CREATE TABLE sales_predictions (
  id SERIAL PRIMARY KEY,
  date DATE,
  product_id INT,
  sales INT,
  price FLOAT,
  category VARCHAR(50),
  temperature FLOAT,
  sales_prediction FLOAT
);