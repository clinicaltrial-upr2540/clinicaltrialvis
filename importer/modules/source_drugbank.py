#!/usr/bin/env python3

from zipfile import ZipFile
from subprocess import Popen
from os import path
from source_common import *


# Check if the DrugBank data file exists
# If it is zipped, unzip it
# Returns False or the path to the XML
def validate_downloaded_file(CURRENT_PATH):
    result = False
    FILENAME = "drugbank_all_full_database.xml"
    PATH_LIST = [
        "/tmp/",
        "/Downloads/",
        "~/Downloads/",
        f"{CURRENT_PATH}/data/",
        f"{CURRENT_PATH}/../data/"
    ]

    # Loop through possible locations to unzip file if found
    for item in PATH_LIST:
        if path.exists(f"{item}{FILENAME}.zip"):
            # Unzip the thing
            with ZipFile(f"{item}{FILENAME}.zip", 'r') as zipObj:
                zipObj.extractall(str(path.dirname(item)))
            break

    # Loop through dirs again to find the actual XML
    for item in PATH_LIST:
        if path.exists(f"{item}{FILENAME}"):
            result = f"{item}{FILENAME}"
            break

    return result


def validate_data(engine):
    print("Validating DrugBank data...")

    result = True

    table_list = [
        "drug_targ_polys_go",
        "drug_targ_polys_pfams",
        "drug_trans_actions",
        "drug_trans_articles",
        "drug_enzymes_links",
        "carr_poly_pfams",
        "drug",
        "drug_affected_organisms",
        "drug_ahfs_codes",
        "drug_articles",
        "drug_atc_codes",
        "drug_books",
        "drug_calculated_properties",
        "drug_carriers",
        "drug_carriers_actions",
        "drug_carriers_articles",
        "drug_carriers_links",
        "drug_carriers_polypeptides",
        "drug_carriers_polypeptides_syn",
        "drug_carriers_textbooks",
        "drug_categories",
        "drug_classifications",
        "drug_drug_interactions",
        "drug_enzymes",
        "drug_enzymes_actions",
        "drug_enzymes_articles",
        "drug_enzymes_polypeptides",
        "drug_enzymes_polypeptides_external_identifiers",
        "drug_enzymes_polypeptides_pfams",
        "drug_trans_links",
        "drug_trans_polys",
        "drug_trans_polys_external_identifiers",
        "drug_trans_polys_go",
        "drug_trans_polys_pfams",
        "drug_trans_polys_syn",
        "snp_adverse_reactions",
        "drug_pdb_entries",
        "drug_prices",
        "drug_products",
        "drug_reactions",
        "drug_reactions_enzymes",
        "drug_sequences",
        "drug_snp_effects",
        "drug_syn",
        "drug_targ",
        "drug_targ_actions",
        "drug_targ_articles",
        "drug_targ_links",
        "drug_targ_polys",
        "drug_experimental_properties",
        "drug_targ_polys_external_identifiers",
        "drug_targ_polys_syn",
        "drug_targ_textbooks",
        "carr_poly_go",
        "drug_carriers_polypeptides_external_identifiers",
        "drug_dosages",
        "drug_enzy_poly_go",
        "drug_trans_textbooks",
        "drug_transporters",
        "international_brands",
        "salts",
        "drug_enzymes_polypeptides_syn",
        "drug_enzymes_textbooks",
        "drug_external_identifiers",
        "drug_external_links",
        "drug_food_interactions",
        "drug_groups",
        "drug_links",
        "drug_manufacturers",
        "drug_mixtures",
        "drug_packagers",
        "drug_patents",
        "drug_pathway",
        "drug_pathway_drugs",
        "drug_pathway_enzyme"
    ]

    try:
        for table in table_list:
            if not validate_table(engine, "drug_bank", table):
                result = False
    except Exception:
        result = False

    return result


# DrugBank data isn't public and can't actually be downloaded
def download():
    print("DrugBank data is not available for download. Please download manually to your Downloads folder.")


# Function to import drugbank data
def import_to_db(config, engine, PATH, FORCE):
    # If the schema doesn't exist of FORCE is specified, run the import
    if FORCE or not check_for_schema(engine, "drug_bank"):
        uberprint("IMPORTING DrugBank")

        # Drop any old versions of the schema
        with engine.connect() as conn:
            conn.execute("drop schema if exists drug_bank cascade;")

        # Build command to import drugbank data
        command = f"./modules/import_drugbank.R " \
            f"{config['drugdata']['host']} " \
            f"{config['drugdata']['port']} " \
            f"{config['drugdata']['database']} " \
            f"{config['drugdata']['user']} " \
            f"{config['drugdata']['password']} " \
            f"{PATH}"

        # Run the import
        p = Popen(command, shell=True)
        p.wait()

        # Rename the public schema and make a new one
        with engine.connect() as conn:
            conn.execute("alter schema public rename to drug_bank;")
            conn.execute("create schema public;")

        uberprint("IMPORT OF DrugBank COMPLETE")
    else:
        uberprint("SKIPPING IMPORT OF DrugBank")


def cleanup():
    print("Skipping cleanup step for DrugBank.")


if __name__ == "__main__":
    import_to_db(False)
