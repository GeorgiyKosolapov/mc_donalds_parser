import json
from fastapi import FastAPI


app = FastAPI()

with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

@app.get("/products/")
def get_products():
    return products

@app.get('/products/{product_name}')
def get_product_by_name(product_name: str):
    product = products.get(product_name)
    if product:
        return product
    return {"error": "Product not found"}

@app.get('/products/{product_name}/{product_field}')
def get_product_field(product_name:str, product_field:str):
    product = products.get(product_name)
    if product:
        field_value = product.get(product_field)
        if field_value:
            return {product_field: field_value}
        return {"error": "Field not found"}
    return {"error": "Product not found"}

