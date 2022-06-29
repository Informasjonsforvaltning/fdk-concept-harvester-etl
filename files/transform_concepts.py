import json
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
new_base_uri = os.environ['NEW_URI']


def transform(inputfile):

    meta = openfile(inputfile)
    transformed_meta = {}
    meta_to_delete = []
    new_meta = {}
    old_meta = {}

    for meta_key in meta:
        if is_reg_uri(meta_key):
            concept_id = meta_key.split("/")[-1]
            if "/concepts/" in meta_key:
                new_meta[concept_id] = meta[meta_key].get("_id")
            else:
                old_meta[concept_id] = meta[meta_key]

    for concept_key in new_meta:
        transformed_meta[new_meta[concept_key]] = {"fdkId": old_meta[concept_key]["fdkId"],
                                                   "issued": old_meta[concept_key]["issued"],
                                                   "modified": old_meta[concept_key]["modified"]}
        meta_to_delete.append(old_meta[concept_key]["_id"])

    output = args.outputdirectory + "conceptMeta_to_delete.json"
    with open(output, 'w', encoding="utf-8") as delete_file:
        json.dump(meta_to_delete, delete_file, ensure_ascii=False, indent=4)

    return transformed_meta


def transform_fields(meta):
    return {"fdkId": meta["fdkId"],
            "issued": meta["issued"],
            "modified": meta["modified"]}


def is_reg_uri(uri):
    if new_base_uri in uri:
        return True
    else:
        return False


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "mongo_conceptMeta.json"
outputfileName = args.outputdirectory + "conceptMeta_transformed.json"

with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName), outfile, ensure_ascii=False, indent=4)


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