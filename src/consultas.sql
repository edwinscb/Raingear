SELECT category, AVG(ABS(sales - sales_prediction)) AS average_error
FROM sales_predictions
GROUP BY
    category;