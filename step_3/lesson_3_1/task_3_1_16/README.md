# TASK DESCRIPTION

Your task is to create a **FastAPI** application that handles product-related requests. The application must have two endpoints:

1. Endpoint for getting product information:

    - Route: `/product/{product_id}`

    - Method: **GET**

    - Path parameter:

        - `product_id`: product ID (*integer*)

    - Response:

        - Returns a **JSON** object containing product information based on the provided `product_id`.

2. Endpoint for searching products:

    - Route: `/products/search`

    - Method: **GET**

    - Request parameters:

        - `keyword` (*string*, *required*): keyword to search for products.

        - `category` (*string*, *optional*): category to filter products.

        - `limit` (*integer*, *optional*): maximum number of products to return (defaults to 10 unless otherwise specified).

    - Answer:

        - Returns a **JSON** array containing product information that matches the search criteria.

3. For example, you can use the following data to send a response later:

```json
    sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
    }

    sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
    }

    sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
    }

    sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
    }

    sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
    }
```

```python
sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]
```

## Example

A **GET** request to `/product/123` should return:

```json
    {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
    }
```

A **GET** request to `/products/search?keyword=phone&category=Electronics&limit=5` should return:

```json
    [
    {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
    },
    {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
    },
    ...
    ]
```

Please note that if the routes are the same (for example, **`/products/{product_id}`** and **`/products/search`**), then our second route will not work, because the word search **FastAPI** will try to cast to int, that is, process the first route, and will return an error. Routes are processed in the order of handler declaration.
