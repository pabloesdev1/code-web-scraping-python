from pymongo import MongoClient
from bson import ObjectId

class ProductRepository:

    def __init__(self):
        self.client = MongoClient(
            host="", # add your url
            port=27017
        )
        self.db = self.client["web-scraping"]
        self.collection = self.db.products

    def save_product(self, name: str, amazon_url: str, meli_url: str, amazon_price: float, meli_price: float):
        product = {
            "name": name,
            "amazon_url": amazon_url,
            "meli_url": meli_url,
            "amazon_price": amazon_price,
            "meli_price": meli_price
        }
        self.collection.insert_one(product)

    def list_products(self):
        result = self.collection.find({})
        return result

    def update_product(self, id: str, data: dict):
        self.collection.find_one_and_update(
            { "_id": ObjectId(id) },
            { "$set": data },
            upsert=False
        )