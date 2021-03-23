import json
import re
import argparse
from datetime import datetime
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

inputfile = 'nav_concepts.json'
conceptsfileName = args.outputdirectory + "concepts.json"
outputfileName = args.outputdirectory + "unmatched_concepts.json"


exclude = {}
count = 0
with open(conceptsfileName) as concepts_file:
    data = json.load(concepts_file)
    array = data["hits"]["hits"]
    with open(inputfile) as nav_concepts_file:
        concepts = json.load(nav_concepts_file)
        for elastic_concept in array:
            if elastic_concept["_source"]["identifier"][:27] == 'https://data.nav.no/begrep/':
                nav_concept = elastic_concept["_source"]["identifier"]
                if nav_concept not in concepts:
                    count += 1
                    exclude[count] = nav_concept
                    print(str(exclude))
        with open(outputfileName, 'w', encoding="utf-8") as outfile:
            json.dump(exclude, outfile, ensure_ascii=False, indent=4)
