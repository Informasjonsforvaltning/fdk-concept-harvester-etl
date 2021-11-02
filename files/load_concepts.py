import json
import os
import sys

from pymongo import MongoClient
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/conceptHarvester?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection.conceptHarvester
concept_load_file = args.outputdirectory + "conceptMeta_transformed.json"
collection_load_file = args.outputdirectory + "collectionMeta_transformed.json"
concept_delete_file = args.outputdirectory + "conceptMeta_to_delete.json"
collection_delete_file = args.outputdirectory + "collectionMeta_to_delete.json"


def load(load_file, meta_type):
    transformed_json = json.load(load_file)
    total_updated = 0
    total_failed = 0
    fail_log = {}

    if meta_type == "concept":
        print("---- Loading concepts ----")
        meta = db.conceptMeta
    elif meta_type == "collection":
        print("---- Loading collections ----")
        meta = db.collectionMeta
    else:
        sys.exit("Illegal meta_type for load function")

    for mongo_id in transformed_json:
        to_be_updated = transformed_json[mongo_id]
        update_result = meta.find_one_and_update({'_id': mongo_id}, {'$set': to_be_updated})
        if update_result:
            total_updated += 1
        else:
            total_failed += 1
            print("Update failed: " + mongo_id)
            fail_log[mongo_id] = mongo_id

    print("Total number of " + meta_type + " updated: " + str(total_updated))
    print("Total number of " + meta_type + " updates failed: " + str(total_failed))
    with open(args.outputdirectory + meta_type + "_load_errors.json", 'w', encoding="utf-8") as err_file:
        json.dump(fail_log, err_file, ensure_ascii=False, indent=4)


def delete(del_file, meta_type):
    delete_json = json.load(del_file)
    total_deleted = 0
    total_failed = 0
    fail_log = {}

    if meta_type == "concept":
        print("---- Deleting concepts ----")
        meta = db.conceptMeta
    elif meta_type == "collection":
        print("---- Deleting collections ----")
        meta = db.collectionMeta
    else:
        sys.exit("Illegal meta_type for delete function")

    for mongo_id in delete_json:
        print("Deleting ID: " + mongo_id)
        delete_result = meta.delete_one({"_id": mongo_id})
        if delete_result.deleted_count > 0:
            print("Successfully deleted: " + mongo_id)
            total_deleted += 1
        else:
            print("Delete failed: " + mongo_id)
            total_failed += 1
            fail_log[mongo_id] = mongo_id
    print("Total number of " + meta_type + " deleted: " + str(total_deleted))
    print("Total number of " + meta_type + " deletion failed: " + str(total_failed))
    with open(args.outputdirectory + meta_type + "_delete_errors.json", 'w', encoding="utf-8") as err_file:
        json.dump(fail_log, err_file, ensure_ascii=False, indent=4)


# LOAD
with open(concept_load_file) as meta_file:
    load(meta_file, "concept")
with open(collection_load_file) as meta_file:
    load(meta_file, "collection")

# DELETE
with open(concept_delete_file) as delete_file:
    delete(delete_file, "concept")
with open(collection_delete_file) as delete_file:
    delete(delete_file, "collection")






