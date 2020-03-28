#!/usr/bin/env python3

# Script for importing data from pubchem data files.
# Currently only does download step—can't import to db because these things are HUGE.

import os
import gzip
import json
import xmltodict

from ftplib import FTP

data_categories = [
    {
        "name": "Compound",
        "path": "pubchem/Compound/CURRENT-Full/XML",
        "com_ext": ".xml.gz",
        "raw_ext": ".xml"
    },
    {
        "name": "Bioassay",
        "path": "pubchem/Bioassay/JSON",
        "com_ext": ".zip",
        "raw_ext": ""
    },
    {
        "name": "Substance",
        "path": "pubchem/Substance/CURRENT-Full/XML",
        "com_ext": ".xml.gz",
        "raw_ext": ".xml"
    },
    {
        "name": "Target",
        "path": "pubchem/Target",
        "com_ext": ".gz",
        "raw_ext": ""
    }
]

# Loop through data categories
for category in data_categories:
    # Set up FTP connection
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()
    ftp.cwd(category["path"])

    # Get list of filenames
    filenames = ftp.nlst()

    # Download all files
    for filename in filenames:
        if filename.endswith(category["com_ext"]):
            # Check if each file exists
            if os.path.exists(f"./data/pubchem/{category['name']}/{filename}") or os.path.exists(f"./data/pubchem/{category['name']}/{filename.replace(category['com_ext'], category['raw_ext'])}"):
                # If the gzip exists, check the md5 to make sure it's not a partial download

                print(f"{filename} already exists. Skipping!")
            else:
                local_filename = os.path.join(f"./data/pubchem/{category['name']}", filename)
                file = open(local_filename, 'wb')

                print(f"Downloading {filename}...")
                ftp.retrbinary('RETR ' + filename, file.write)

                file.close()

    # Close the ftp connection
    ftp.quit()

# Unzip all the files
# for filename in filenames:
#     if os.path.exists(f"./data/pubchem/{filename.replace('.xml.gz', '.xml')}"):
#         print(f"{filename} has already been decompressed. Skipping!")
#     else:

# with gzip.open("./data/pubchem/Compound_000000001_000500000.xml.gz", mode='rb') as inFh:
#     data = xmltodict.parse(inFh.read())
#     with open('./data/pubchem/Compound_000000001_000500000.json', 'w') as out_file:
#         json.dump(xmltodict.parse(data), out_file)
