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
import source_pubchem
import source_fda
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
    if source_fda.validate_data(engine):
        data_sources["fda"]["imported"] = True

    # DrugBank IMPORT PROCESS
    if not data_sources["drug_bank"]["imported"] or FORCE:
        drugbank_data = source_drugbank.validate_downloaded_file(CURRENT_PATH)

        if drugbank_data:
            source_drugbank.import_to_db(config, engine, drugbank_data, FORCE)
        else:
            print("Unable to find DrugBank data file.")
            uberprint("SKIPPING IMPORT OF DrugBank")
    else:
        uberprint("SKIPPING IMPORT OF DrugBank")

    # FDA IMPORT PROCESS
    if source_fda.validate_data(engine):
        data_sources["fda"]["imported"] = True
    if not data_sources["fda"]["imported"] or FORCE:
        # Download FDA data
        source_fda.download(CURRENT_PATH)

        fda_data = source_fda.validate_downloaded_file(CURRENT_PATH)

        # Import FDA data
        if fda_data:
            source_fda.import_to_db(config, engine, CURRENT_PATH, FORCE)
        else:
            print("Unable to find FDA data file.")
            uberprint("SKIPPING IMPORT OF FDA")

        source_fda.cleanup(CURRENT_PATH)
    else:
        uberprint("SKIPPING IMPORT OF FDA")

    # PubChem import process
    if source_pubchem.validate_data(engine):
        data_sources["pubchem"]["imported"] = True
    if not data_sources["pubchem"]["imported"] or FORCE:
        source_pubchem.import_to_db(config, engine, CURRENT_PATH)
    else:
        uberprint("SKIPPING IMPORT OF PUBCHEM")


if __name__ == "__main__":
    # Get script directory
    CURRENT_PATH = str(os.path.dirname(os.path.realpath(__file__)))

    # Import database configuration
    config = ConfigParser()
    config.read("./database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    main(config, engine, CURRENT_PATH, False)
