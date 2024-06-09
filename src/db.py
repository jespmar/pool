from pymongo import MongoClient

import os
from dotenv import load_dotenv

HOST = os.getenv('MONGO_HOST')
PORT = int(os.getenv('MONGO_PORT'))
USERNAME = os.getenv('MONGO_USERNAME')
PASSWORD = os.getenv('MONGO_PASSWORD')


config={
    "host":"mongo-nodeport-svc",
    "port":27017,
    "username":"adminuser",
    "password":"password123"
}

class Connection:
    def __new__(cls, database):
        connection=MongoClient(**config)
        return connection[database]