"""A module that provides a server for efficient operation of applications."""

from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException

from models.models import Product
from database import sample_products

app = FastAPI()

# Preprocess sample_products into a list
# of Product objects and a dictionary for fast lookup
filtered_products = [Product(**item) for item in sample_products]
product_dict = {product.product_id: product for product in filtered_products}


@app.get("/products/search", response_model=List[Product])
def read_product_by_keyword(
    keyword: str,
    category: Optional[str] = None,
    limit: int = 10
) -> List[Product]:
    """
    Search for products by keyword and optional category.

    Parameters:
        keyword (str):
                The keyword to search for in product names.
        category (str, optional):
                The category to filter products by. Defaults to None.
        limit (int):
                The maximum number of products to return. Defaults to 10.

    Returns:
        List[Product]:
                A list of products matching the search criteria,
                limited by the specified limit.
    """

    keyword_lower = keyword.lower()
    if category:
        category_lower = category.lower()
        result = [product for product in filtered_products
                  if keyword_lower in product.name.lower() and
                  product.category.lower() == category_lower]
    else:
        result = [product for product in filtered_products
                  if keyword_lower in product.name.lower()]

    return result[:limit]


@app.get("/product/{product_id}", response_model=Product)
def read_product_by_id(product_id: int) -> Product:
    """
    Retrieve a product by its unique identifier.

    Parameters:
        product_id (int): The unique identifier of the product to retrieve.

    Returns:
        Product: The product object corresponding to the given product ID.

    Raises:
        HTTPException: 404 if the product with the specified ID does not exist.
    """

    if product_id not in product_dict:
        raise HTTPException(status_code=404, detail="Product not available")

    return product_dict[product_id]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
