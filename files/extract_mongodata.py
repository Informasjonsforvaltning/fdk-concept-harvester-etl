import json
import os
import re
from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/conceptHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.conceptHarvester
dict_list = list(db.conceptMeta.find({}, {"_id": 1}))
ids = {}
for id_dict in dict_list:
    id_str = id_dict["_id"]

    ids[id_str] = id_str

with open(args.outputdirectory + 'mongo_concepts_id.json', 'w', encoding="utf-8") as outfile:
    json.dump(ids, outfile, ensure_ascii=False, indent=4)
