from fastapi import FastAPI,HTTPException
from product import product_router

app = FastAPI()
app.include_router(product_router)
