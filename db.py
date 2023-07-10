from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb://localhost:27017"


ca = certifi.where()


def dbConnection():
    try:
        client = MongoClient(MONGO_URI)
        db = client["main"]

    except ConnectionError:
        print('Error de conexion con la bdd')
    return db
