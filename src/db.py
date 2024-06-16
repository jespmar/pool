from pymongo import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv


uri = os.getenv('MONGO_URI')

class Connection:
    def __new__(cls, database):

        uri = "mongodb+srv://pool:eIqbTV9s47gwohZE@cluster0.c259gkh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(uri, server_api=ServerApi(
        version="1", strict=True, deprecation_errors=True))

        return client[database]