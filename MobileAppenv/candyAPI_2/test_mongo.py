from candyAPI.mongoManager import MongoDBInterface, mongoConnect
import json
from rich import print
import sys
import re


# db = MongoDBInterface('candy_store_2','candies')
# db = MongoDBInterface(username='',password='',db='candy_store',collection='canndies')


info = {
    'username' : "mongomin",
    'password' : "horsedonkeyblanketbattery",
    'host' : "localhost",
    'port' : "27017",
    'db_name' : "candy_store",
    'collection_name' : "candies"
}

db = mongoConnect(**info)

# result = db.get(select={},filter={'_id': 0, 'category': 1})

# categories = {}
# for category in result:
#     if not category['category'] in categories:
#         categories[category['category']] = 0
#     categories[category['category']] += 1 
# print(list(categories.keys()))

# result = db.get(select={"category": "gummy-candy"},filter={'_id':0})
# print(result)

result = db.get(query={"category": "gummy-candy","name": {"$regex": re.compile("Sour", re.IGNORECASE)},})
print(result)