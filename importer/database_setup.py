#!/usr/bin/env python3

import os
import sys
import sqlalchemy

from configparser import ConfigParser

# Set up path for local imports
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}")
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/modules")

import source_common
import source_drugbank
from source_common import *

data_sources = {
    "central_drug": {
        "downloaded": False,
        "imported": False
    },
    "chembl_26": {
        "downloaded": False,
        "imported": False
    },
    "drug_bank": {
        "downloaded": False,
        "imported": False
    },
    "fda": {
        "downloaded": False,
        "imported": False
    },
    "kegg": {
        "downloaded": False,
        "imported": False
    },
    "mesh": {
        "downloaded": False,
        "imported": False
    },
    "pubchem": {
        "downloaded": False,
        "imported": False
    },
    "top200": {
        "downloaded": False,
        "imported": False
    }
}


def main(config, engine, CURRENT_PATH, FORCE):
    # Check if data sources have already been imported
    if source_drugbank.validate_data(engine):
        data_sources["drug_bank"]["imported"] = True

    # Import DrugBank data
    if not data_sources["drug_bank"]["imported"] or FORCE:
        drugbank_data = source_drugbank.validate_downloaded_file(CURRENT_PATH)

        if drugbank_data:
            source_drugbank.import_to_db(config, engine, drugbank_data, FORCE)
        else:
            print("Unable to find DrugBank data file.")
            uberprint("SKIPPING IMPORT OF DrugBank")
    else:
        uberprint("SKIPPING IMPORT OF DrugBank")


if __name__ == "__main__":
    # Get script directory
    CURRENT_PATH = str(os.path.dirname(os.path.realpath(__file__)))

    # Import database configuration
    config = ConfigParser()
    config.read("./database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    main(config, engine, CURRENT_PATH, True)
