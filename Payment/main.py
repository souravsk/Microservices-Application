from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests,time

app = FastAPI()

""" Inoder to privent application running on different port  """
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

""" This database should we a new database because in microservices every services have differnt database """

""" Connted the connetion with the database  """
redis = get_redis_connection(
    host="redis-17648.c239.us-east-1-2.ec2.cloud.redislabs.com",
    port=17648,
    password="rH5oGfUSx65mnTZBRGrQ99pl6YHOcAYH",
    decode_responses=True
)

class Order(HashModel):
    product_id: str
    price:float
    fee:float
    total:float
    quantity:int
    status:str #pending, completed, refunded

    class Meta:
        database = redis

@app.get('/orders/{pk}')
def get(pk:str):
    return Order.get(pk)


@app.post('/orders')
async def create(request: Request, backGround_task: BackgroundTasks): #here we will just sent ID and Quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    backGround_task.add_task(order_completed, order)

    return order

    return order

def order_completed(order: Order):
    time.sleep(15)
    order.status = 'completed'
    order.save()
