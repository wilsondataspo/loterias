import logging
from pymongo import ASCENDING
from pymongo import MongoClient


logger = logging.getLogger(__name__)

MONGODB_CLIENT = MongoClient("mongodb://127.0.0.1:27017/")


def install(app):
    """returns a collection, with result by lotofacil contest"""
    try:
        db = MONGODB_CLIENT.get_database("Resultados")
        app.db = db.get_collection("Lotofacil")
        db.addresses.create_index([("CONC", ASCENDING)], unique=True)
        MONGODB_CLIENT.server_info()
    except Exception as e:
        logger.error(f"Error connect database: {e}")
        exit()