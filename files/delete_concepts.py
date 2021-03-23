import json
import requests
import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

host = 'http://elasticsearch5:9200/'
url = host + os.environ["ELASTIC_CCAT_INDEX"] + "/concept/"
headers = {'Content-Type': 'application/json'}

with open(args.outputdirectory + 'unmatched_concepts.json') as transformed_file:
    transformed_json = json.load(transformed_file)
    totalDeleted = 0
    print("Deleting the following data from Begrep index: " + transformed_json)
    for concept in transformed_json:
        elastic_id = concept["id"]
        delete_url = url + elastic_id
        print("Deleting from the following url: ", delete_url)
        r = requests.delete(delete_url, headers=headers)
        print("Deleted " + elastic_id + ": " + str(r.status_code))
        if str(r.status_code) == "200":
            totalDeleted += 1
    print("Total deleted: ", str(totalDeleted))

