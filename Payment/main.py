from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

""" Inoder to privent application running on different port  """
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

""" Connted the connetion with the database  """
redis = get_redis_connection(
    host="redis-17648.c239.us-east-1-2.ec2.cloud.redislabs.com",
    port=17648,
    password="rH5oGfUSx65mnTZBRGrQ99pl6YHOcAYH",
    decode_responses=True
)

""" Here are creating funtion or class that will convert the data into table form """
class Product(HashModel):
    name: str
    price:float
    quantity:int

    """ to connect with the redis database """
    class Meta:
        database = redis

""" So with the help of the FastAPI we don't have to create api we can just use it with @app.methods what we want """
@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()] 

""" This function will return the data that is stored into the data base """
def format(pk:str):
    product = Product.get(pk)
    return{
        'id':product.pk,
        'name':product.name,
        'price':product.price,
        'quantity':product.quantity
    }

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk:str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk:str):
    return Product.delete(pk)