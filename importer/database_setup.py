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
import source_mesh
import source_chembl
from source_common import *

data_sources = {
    "central_drug": {
        "imported": False
    },
    "chembl_26": {
        "imported": False
    },
    "drug_bank": {
        "imported": False
    },
    "fda": {
        "imported": False
    },
    "mesh": {
        "imported": False
    },
    "pubchem": {
        "imported": False
    },
    "top200": {
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

    # MeSH IMPORT PROCESS
    if source_mesh.validate_data(engine):
        data_sources["mesh"]["imported"] = True
    if not data_sources["mesh"]["imported"] or FORCE:
        # Download MeSH data
        source_mesh.download(CURRENT_PATH)

        mesh_data = source_mesh.validate_downloaded_file(CURRENT_PATH)

        # Import MeSH data
        if mesh_data:
            source_mesh.import_to_db(config, engine, CURRENT_PATH)
        else:
            print("Unable to find MeSH data file.")
            uberprint("SKIPPING IMPORT OF MeSH")

        source_mesh.cleanup(CURRENT_PATH)
    else:
        uberprint("SKIPPING IMPORT OF MeSH")

    # ChemBL IMPORT PROCESS
    if source_chembl.validate_data(engine):
        data_sources["chembl_26"]["imported"] = True
    if not data_sources["chembl_26"]["imported"] or FORCE:
        # Download ChemBL data
        source_chembl.download(CURRENT_PATH)

        chembl_data = source_chembl.validate_downloaded_file(CURRENT_PATH)

        # Import ChemBL data
        if chembl_data:
            source_chembl.import_to_db(config, engine, CURRENT_PATH)
        else:
            print("Unable to find ChemBL data file.")
            uberprint("SKIPPING IMPORT OF ChemBL")

        source_chembl.cleanup(CURRENT_PATH)
    else:
        uberprint("SKIPPING IMPORT OF ChemBL")


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
