import json
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
new_base_uri = os.environ['FDK_REGISTRATION_BASE_URI']


def transform(inputfile, inputfile2):

    datasets = openfile(inputfile)
    datasets_meta = openfile(inputfile2)
    transformed_datasets = {}
    print("Total number of extracted datasets: " + str(len(datasets)))
    for dataset_key in datasets:
        old_uri = datasets[dataset_key].get("uri")
        new_uri = create_uri(datasets[dataset_key])
        to_be_transformed = datasets_meta.get(old_uri)
        if to_be_transformed:
            transformed = transform_catalog(to_be_transformed, new_uri)
            transformed_datasets[old_uri] = transformed
    return transformed_datasets


def transform_catalog(to_be_transformed, new_id):
    transformed = to_be_transformed
    transformed["_id"] = new_id
    return transformed


def create_uri(dataset):
    return new_base_uri + '/catalogs/' + dataset["org_id"] + "/datasets/" + dataset["ds_id"]


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "mongo_conceptMeta.json"
inputfileName2 = args.outputdirectory + "mongo_collectionMeta.json"
outputfileName = args.outputdirectory + "conceptMeta_transformed.json"
outputfileName2 = args.outputdirectory + "collectionMeta_transformed.json"


with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName, inputfileName2), outfile, ensure_ascii=False, indent=4)


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