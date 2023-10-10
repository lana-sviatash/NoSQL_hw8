from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# import configparser


uri = "mongodb+srv://goitlearn:EonuZ7uxhFxUO8MQ@cluster0.mcqnxq7.mongodb.net/?retryWrites=true&w=majority"
# config = configparser.ConfigParser()
# config.read('config.ini')

# mongo_user = config.get('DB', 'user')
# mongodb_pass = config.get('DB', 'pass')
# domain = config.get('DB', 'domain')

# uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

db = client.hw_8_1

if __name__ == "__main__":
    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")

        results = db.author.find()
        for r in results:
            print(r)
    except Exception as e:
        print(e)
