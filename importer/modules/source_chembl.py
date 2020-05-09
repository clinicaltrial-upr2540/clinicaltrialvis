#!/usr/bin/env python3 -u

import os
import shutil
import tarfile
import sqlalchemy

from subprocess import Popen
from configparser import ConfigParser
from sqlalchemy.exc import ProgrammingError
from source_common import *


# Check if the ChemBL data file exists
# If it is tarred, untar it
# Returns False or the path to the untarred directory
def validate_downloaded_file(CURRENT_PATH):
    result = False
    FILENAME = "chembl_26_postgresql"
    PATH_LIST = [
        "/tmp/",
        "/Downloads/",
        "~/Downloads/",
        f"{CURRENT_PATH}/data/",
        f"{CURRENT_PATH}/../data/"
    ]

    # Loop through possible locations to untar file if found
    for item in PATH_LIST:
        if os.path.exists(f"{item}{FILENAME}.tar.gz"):
            # Untar the thing
            chembl_tarfile = tarfile.open(f"{item}{FILENAME}.tar.gz")
            chembl_tarfile.extractall(f"{CURRENT_PATH}/data")  # specify which folder to extract to
            chembl_tarfile.close()

            break

    # Loop through dirs again to find the actual data file
    for item in PATH_LIST:
        if os.path.exists(f"{item}chembl_26"):
            result = f"{item}chembl_26"
            break

    return result


# Validate any ChemBL data present in the database
def validate_data(engine):
    print("Validating ChemBL data...")

    result = True

    table_list = [
        "action_type",
        "activities",
        "activity_properties",
        "activity_smid",
        "activity_stds_lookup",
        "activity_supp",
        "activity_supp_map",
        "assay_class_map",
        "assay_classification",
        "assay_parameters",
        "assay_type",
        "assays",
        "atc_classification",
        "binding_sites",
        "bio_component_sequences",
        "bioassay_ontology",
        "biotherapeutic_components",
        "biotherapeutics",
        "cell_dictionary",
        "chembl_id_lookup",
        "component_class",
        "component_domains",
        "component_go",
        "component_sequences",
        "component_synonyms",
        "compound_properties",
        "compound_records",
        "compound_structural_alerts",
        "compound_structures",
        "confidence_score_lookup",
        "curation_lookup",
        "data_validity_lookup",
        "defined_daily_dose",
        "docs",
        "domains",
        "drug_indication",
        "drug_mechanism",
        "formulations",
        "frac_classification",
        "go_classification",
        "hrac_classification",
        "indication_refs",
        "irac_classification",
        "ligand_eff",
        "mechanism_refs",
        "metabolism",
        "metabolism_refs",
        "molecule_atc_classification",
        "molecule_dictionary",
        "molecule_frac_classification",
        "molecule_hierarchy",
        "molecule_hrac_classification",
        "molecule_irac_classification",
        "molecule_synonyms",
        "organism_class",
        "patent_use_codes",
        "predicted_binding_domains",
        "product_patents",
        "products",
        "protein_class_synonyms",
        "protein_classification",
        "protein_family_classification",
        "relationship_type",
        "research_companies",
        "research_stem",
        "site_components",
        "source",
        "structural_alert_sets",
        "structural_alerts",
        "target_components",
        "target_dictionary",
        "target_relations",
        "target_type",
        "tissue_dictionary",
        "usan_stems",
        "variant_sequences",
        "version"
    ]

    try:
        for table in table_list:
            if not validate_table(engine, "chembl_26", table):
                result = False
    except Exception as e:
        print(e)
        result = False

    return result


# Download the ChemBL data files
def download(PATH):
    print("Downloading ChemBL data.")
    download_ftp("ftp.ebi.ac.uk", "pub/databases/chembl/ChEMBLdb/latest", "chembl_26_postgresql.tar.gz", PATH)


# Function to import ChemBL data
def import_to_db(config, engine, PATH):
    uberprint("IMPORTING ChemBL")

    # Do some database setup
    with engine.connect() as conn:
        try:
            conn.execute("CREATE ROLE \"user\" superuser;")
        except ProgrammingError:
            pass
        conn.execute("DROP SCHEMA IF EXISTS chembl_26 CASCADE;")

    # Build command to import chmbl data
    command = f"/usr/local/bin/pg_restore " \
        f"-h {config['drugdata']['host']} " \
        f"-d {config['drugdata']['database']} " \
        f"-p {config['drugdata']['port']} " \
        f"-U {config['drugdata']['user']} " \
        f"-w -j 2 {PATH}/data/chembl_26/chembl_26_postgresql/chembl_26_postgresql.dmp"

    # Run the import
    p = Popen(command, shell=True, env={
        'PGPASSWORD': config['drugdata']['password']
    })
    p.wait()

    # Rename the public schema and make a new one
    with engine.connect() as conn:
        conn.execute("ALTER SCHEMA public RENAME TO chembl_26;")
        conn.execute("CREATE SCHEMA public;")

    uberprint("IMPORT OF ChemBL COMPLETE")


# Remove downloaded ChemBL files
def cleanup(PATH):
    print("Cleaning up ChemBL files.")
    try:
        shutil.rmtree(f"{PATH}/data/chembl_26")
        os.remove(f"{PATH}/data/chembl_26_postgresql.tar.gz")
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
