import json
import os
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/conceptHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")

db = connection.conceptHarvester
concept_list = list(db.conceptMeta.find())
conceptMetas = {}
for id_dict in concept_list:
    _id = id_dict["_id"]
    conceptMetas[_id] = {}
    conceptMetas[_id]["fdkId"] = id_dict.get("fdkId")
    conceptMetas[_id]["issued"] = id_dict.get("issued")
    conceptMetas[_id]["modified"] = id_dict.get("modified")
print("Total number of extracted conceptMetas: " + str(len(conceptMetas)))

with open(args.outputdirectory + 'mongo_conceptMeta.json', 'w', encoding="utf-8") as outfile:
    json.dump(conceptMetas, outfile, ensure_ascii=False, indent=4)

collection_list = list(db.collectionMeta.find())
collectionMetas = {}
for id_dict in collection_list:
    _id = id_dict["_id"]
    collectionMetas[_id] = {}
    collectionMetas[_id]["fdkId"] = id_dict.get("fdkId")
    collectionMetas[_id]["issued"] = id_dict.get("issued")
    collectionMetas[_id]["modified"] = id_dict.get("modified")
print("Total number of extracted collectionMetas: " + str(len(collectionMetas)))

with open(args.outputdirectory + 'mongo_collectionMeta.json', 'w', encoding="utf-8") as outfile:
    json.dump(collectionMetas, outfile, ensure_ascii=False, indent=4)
