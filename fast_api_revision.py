from fastapi import FastAPI, Request
from mockData import products
from dtos import ProductDTO

app= FastAPI()

@app.get("/")
def home():
    return {"message":"server is up and running"}

# Get all products
@app.get('/products')
def all_prods():
    return products
# Path Parameter 
@app.get('/product/{prod_id}')
def product(prod_id:int):
    for product in products:
        if product.get("id")==prod_id:
            return product
    return {"Message":"Item not found with id"}

# Query Param
@app.get("/greet")
def greet(request:Request):
    query_params=dict(request.query_params)
    print(query_params)
    return {
        "message":f'Hello {query_params.get("name")} welcome your age is {query_params.get("age")} '
    }


# HTTP METHODS GET PUT POST DELETE

# Create POST
@app.post('/create_product')
def create_product(product_data:ProductDTO):

    product=product_data.model_dump()
    products.append(product)
    return {
        "Message":"Successfully Created Product",
        "Products":products
    }

# UPDATE
@app.put("/update_data/{product_id}")
def update_product(product_id:int,product_data:ProductDTO):
    for index,product in enumerate(products):
        if product.get("id") == product_id:
            products[index]=product_data.model_dump()
            return{
                "Message":"Updated Sucessfully",
                "Data":products[index]
            }
    return {"Message":"Invalid ID's"}

# DELETE 
@app.delete('/delete/{product_id}')
def delete(product_id:int):
    for index,product in enumerate(products):
        if product.get("id") == product_id:
            deleted_product=products.pop(index)
            return {"message":"Deletion Successfull",
                    "Deleted":deleted_product}
    return {"Message":"Invalid ID provided"}