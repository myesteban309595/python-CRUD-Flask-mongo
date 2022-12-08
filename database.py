
from pymongo import MongoClient
import certifi

# mongodb+srv://admin:admin1234@cluster0.groubjk.mongodb.net/?retryWrites=true&w=majority

MONGO_URI = 'mongodb+srv://admin:admin1234@cluster0.groubjk.mongodb.net/?retryWrites=true&w=majority'

ca = certifi.where()   # instancia de certifi

def dbConnection():
    try:
        client = MongoClient.connect(MONGO_URI, tlsCAFile = ca)
        # en caso que no exista la base de datos crearla
        db = client['dbb_products_app']
    except ConnectionError:
        print('Error de conexion con la bdd')
    return db