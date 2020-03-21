#!/usr/bin/env python3

# Ad-hoc script for testing working with large pubchem data files.

import json
import xmltodict

with open("./data/pubchem/Compound_000000001_000500000.xml", mode='rb') as file:
    data = xmltodict.parse(file.read())

with open('./data/pubchem/Compound_000000001_000500000.json', 'w') as out_file:
    json.dump(data, out_file)
