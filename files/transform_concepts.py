import json
import re
import argparse
from datetime import datetime
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
update_dates = os.environ["TO_BE_UPDATED"] == 'dates'


def transform(inputfile, inputfile_mongo):

    concepts = openfile(inputfile)
    mongo_ids = openfile(inputfile_mongo)

    array = concepts["hits"]["hits"]

    print("Number of concepts:" + str(len(array)))
    transformed = {}
    failed = {}
    for concept in array:
        uri = concept["_source"].get("identifier")
        if mongo_ids.get(uri):
            transformed[uri] = fields_to_change(concept)
        else:
            failed[uri] = "Not found in mongo"

    failed_transform = args.outputdirectory + "failed_transform.json"
    with open(failed_transform, 'w', encoding="utf-8") as failed_file:
        json.dump(failed, failed_file, ensure_ascii=False, indent=4)
    return transformed


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def fields_to_change(elastic_concept):
    if update_dates is True:
        return {"issued": elastic_concept["_source"]["harvest"]["firstHarvested"],
                "modified": elastic_concept["_source"]["harvest"]["lastHarvested"]}
    else:
        return {"fdkId": elastic_concept["_id"]}


inputfileName = args.outputdirectory + "concepts.json"
inputfileNameMongo = args.outputdirectory + "mongo_concepts_id.json"
outputfileName = args.outputdirectory + "concepts_transformed.json"


with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName, inputfileNameMongo), outfile, ensure_ascii=False, indent=4)
