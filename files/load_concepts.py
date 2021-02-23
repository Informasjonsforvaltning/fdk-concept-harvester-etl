import json
import os
from pymongo import MongoClient
import argparse
import bson


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/conceptHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.conceptHarvester
update_dates = os.environ["UPDATE_DATES"] == 'True'

with open(args.outputdirectory + 'concepts_transformed.json') as transformed_file:
    transformed_json = json.load(transformed_file)
    for mongo_id in transformed_json:
        print("Mongo_id: " + mongo_id)
        values = transformed_json[mongo_id]
        if update_dates is True:
            to_be_updated = {"issued": bson.Int64(int(values["issued"])),
                             "modified": bson.Int64(int(values["modified"]))}
        else:
            to_be_updated = {"fdkId": str(values["fdkId"])}

        print("To be updated: " + str(to_be_updated))
        print(db.conceptMeta.find_one_and_update({'_id': mongo_id},  {'$set': to_be_updated}))
