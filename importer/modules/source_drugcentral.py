#!/usr/bin/env python3 -u

import os
import gzip
import sqlalchemy

from subprocess import Popen
from configparser import ConfigParser
from source_common import *


# Check if the DrugCentral data file exists
# If it is gzipped, decompress it
# Returns False or the path to the unzipped directory
def validate_downloaded_file(CURRENT_PATH):
    result = False
    FILENAME = "drugcentral.sql"
    PATH_LIST = [
        "/tmp/",
        "/Downloads/",
        "~/Downloads/",
        f"{CURRENT_PATH}/data/",
        f"{CURRENT_PATH}/../data/"
    ]

    # Loop through possible locations to untar file if found
    for item in PATH_LIST:
        if os.path.exists(f"{item}{FILENAME}.gz"):
            # Decompress the gzip
            with gzip.open(f"{item}{FILENAME}.gz", 'rb') as infile:
                with open(f"{CURRENT_PATH}/data/drugcentral.sql", 'wb') as outfile:
                    drugcentral_data = infile.read()
                    outfile.write(drugcentral_data)

            break

    # Loop through dirs again to find the actual data file
    for item in PATH_LIST:
        if os.path.exists(f"{item}{FILENAME}"):
            result = f"{item}{FILENAME}"
            break

    return result


# Validate any DrugCentral data present in the database
def validate_data(engine):
    print("Validating DrugCentral data...")

    result = True

    table_list = [
        "act_table_full",
        "action_type",
        "active_ingredient",
        "approval",
        "approval_type",
        "atc",
        "atc_ddd",
        "attr_type",
        "data_source",
        "dbversion",
        "ddi",
        "ddi_risk",
        "doid",
        "doid_xref",
        "drug_class",
        "faers",
        "id_type",
        "identifier",
        "inn_stem",
        "label",
        "lincs_signature",
        "ob_exclusivity",
        "ob_exclusivity_code",
        "ob_patent",
        "ob_patent_use_code",
        "ob_product",
        "omop_relationship",
        "parentmol",
        "pdb",
        "pharma_class",
        "pka",
        "prd2label",
        "product",
        "protein_type",
        "ref_type",
        "reference",
        "section",
        "struct2atc",
        "struct2drgclass",
        "struct2obprod",
        "struct2parent",
        "struct_type_def",
        "structure_type",
        "structures",
        "synonyms",
        "target_class",
        "target_component",
        "target_dictionary",
        "target_go",
        "target_keyword",
        "td2tc",
        "tdgo2tc",
        "tdkey2tc"
    ]

    try:
        for table in table_list:
            if not validate_table(engine, "central_drug", table):
                result = False
    except Exception as e:
        print(e)
        result = False

    return result


# Download the DrugCentral data files
def download(PATH):
    print("Downloading DrugCentral data.")
    download_http("http://unmtid-shinyapps.net/download/drugcentral.dump.08262018.sql.gz", "drugcentral.sql.gz", PATH)


# Function to import DrugCentral data
def import_to_db(config, engine, PATH):
    uberprint("IMPORTING DrugCental")

    # Drop existing data
    with engine.connect() as conn:
        conn.execute("DROP SCHEMA IF EXISTS central_drug CASCADE;")

    # Build command to import DrugCentral data
    command = f"/usr/local/bin/psql -h {config['drugdata']['host']} " \
        f"-d {config['drugdata']['database']} " \
        f"-p {config['drugdata']['port']} " \
        f"-U {config['drugdata']['user']} " \
        f"-f {PATH}/data/drugcentral.sql"

    # Run the command
    p = Popen(command, shell=True, env={
        'PGPASSWORD': config['drugdata']['password']
    })
    p.wait()

    # Rename the public schema and make a new one
    with engine.connect() as conn:
        conn.execute("ALTER SCHEMA public RENAME TO central_drug;")
        conn.execute("CREATE SCHEMA public;")

    uberprint("IMPORT OF DrugCental COMPLETE")


# Remove downloaded DrugCentral files
def cleanup(PATH):
    print("Cleaning up DrugCentral files.")
    try:
        os.remove(f"{PATH}/data/drugcentral.sql")
        os.remove(f"{PATH}/data/drugcentral.sql.gz")
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    # Get script directory
    CURRENT_PATH = str(os.path.dirname(os.path.realpath(__file__))) + "/.."

    # Import database configuration
    config = ConfigParser()
    config.read(f"{CURRENT_PATH}/database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    download(CURRENT_PATH)
    validate_downloaded_file(CURRENT_PATH)
    import_to_db(config, engine, CURRENT_PATH)
    cleanup(CURRENT_PATH)
