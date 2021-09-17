import json
import os
from pymongo import MongoClient
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/datasetHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.datasetHarvester

with open(args.outputdirectory + 'datasets_transformed.json') as datasets_file:
    transformed_json = json.load(datasets_file)

    total_updated = 0
    total_skipped = 0
    for mongo_id in transformed_json:
        to_be_updated = transformed_json[mongo_id]
        if mongo_id == to_be_updated.get("_id"):
            print("Not updating identical ids: " + mongo_id)
            total_skipped += 1
        else:
            print("Inserting ID: " + to_be_updated.get("_id"))
            insert_result = db.datasetMeta.insert_one(to_be_updated)
            print("Result ID: " + insert_result.inserted_id)
            print("Deleting ID: " + mongo_id)
            delete_result = db.datasetMeta.delete_one({"_id": mongo_id})
            print("Documents deleted: " + str(delete_result.deleted_count))
            total_updated += 1
    print("Total number of datasets updated: " + str(total_updated))
    print("Total number of datasets skipped: " + str(total_skipped))
