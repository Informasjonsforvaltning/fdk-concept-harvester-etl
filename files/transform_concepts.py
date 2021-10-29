import json
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
new_base_uri = os.environ['NEW_URI']
old_base_uri = os.environ['OLD_URI']


def transform(inputfile, meta_type):

    meta = openfile(inputfile)
    transformed_meta = {}
    meta_to_delete = []

    for meta_key in meta:
        if is_old_uri(meta_key):
            transformed_meta[transform_uri(meta_key)] = transform_fields(meta[meta_key])
            meta_to_delete.append(meta_key)

    if meta_type == "concepts":
        output = args.outputdirectory + "conceptMeta_to_delete.json"
        with open(output, 'w', encoding="utf-8") as delete_file:
            json.dump(meta_to_delete, delete_file, ensure_ascii=False, indent=4)
    elif meta_type == "collections":
        output = args.outputdirectory + "collectionMeta_to_delete.json"
        with open(output, 'w', encoding="utf-8") as delete_file:
            json.dump(meta_to_delete, delete_file, ensure_ascii=False, indent=4)

    return transformed_meta


def transform_fields(meta):
    return {"fdkId": meta["fdkId"],
            "issued": meta["issued"],
            "modified": meta["modified"]}


def transform_uri(uri):
    return uri.replace(old_base_uri, f'{new_base_uri}/collections')


def is_old_uri(uri):
    if old_base_uri in uri:
        return True
    else:
        return False


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "mongo_conceptMeta.json"
outputfileName = args.outputdirectory + "conceptMeta_transformed.json"

with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName, "concepts"), outfile, ensure_ascii=False, indent=4)

inputfileName2 = args.outputdirectory + "mongo_collectionMeta.json"
outputfileName2 = args.outputdirectory + "collectionMeta_transformed.json"

with open(outputfileName2, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName2, "collections"), outfile, ensure_ascii=False, indent=4)


# 1: extract conceptMeta og collectionMeta
#TODO: 2: Kjøre løkke på begge, der vi får treff på _id som er concept-catalog
#TODO: 3: trekk ut guid fra _id-urien,
#TODO: 4: hent tilsvarende concept/collectionMeta som har "registrering-begrep"-uri med samme guid
#TODO: 5: Oppdater fdkId i "concept-catalog"-objektet med verdien fra "registrering-begrep" objektet
#TODO: 6: Load
#TODO: 7: Kjør høsting
#TODO: 8: Gjenta steg 2-4
#TODO: 9: Oppdater issued/modified i "concept-catalog"-objektet med verdiene fra "registrering-begrep"-objektet
#TODO: 10: Load
#TODO: 11: Update meta