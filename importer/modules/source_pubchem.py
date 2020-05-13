#!/usr/bin/env python3 -u

import os
import sqlalchemy
import json
import time
import requests

from configparser import ConfigParser
from source_common import *


# Pubchem doesn't download a data file
def validate_downloaded_file():
    print("Skipping validation step for PubChem data.")


# Validate whether PubChem already has data in the database
def validate_data(engine):
    print("Validating PubChem data...")

    result = True

    table_list = [
        "compounds"
    ]

    try:
        for table in table_list:
            if not validate_table(engine, "pubchem", table):
                result = False
    except Exception as e:
        print(e)
        result = False

    return result


# DrugBank data isn't public and can't actually be downloaded
def download():
    print("Skipping data download for PubChem data.")


# Function to get a value from a json object (really a dict) and suppress failures
def get_key(json_object, key):
    try:
        if isinstance(json_object[key], str):
            result = json_object[key].replace('\'', '\'\'').replace(r'(', r'\(').replace(r')', r'\)').replace(';', r'\;')
        else:
            result = json_object[key]
    except Exception:
        result = "null"

    return(result)


# Function to dynamically throttle requests based on PubChem API status
def api_delay(headers):
    if "X-Throttling-Control" in dict(headers):
        throttling_header = dict(headers)["X-Throttling-Control"]

        if "Black" in throttling_header:
            print("API status is BLACK, waiting 5 minutes...")
            time.sleep(300)
        elif "Red" in throttling_header:
            print("API status is RED, waiting 30 seconds...")
            time.sleep(30)
        elif "Yellow" in throttling_header:
            print("API status is YELLOW, waiting 10 seconds...")
            time.sleep(10)
    else:
        print("Bad API response, retrying...")
        time.sleep(1)


# Function to import pubchem data
def import_to_db(config, engine, PATH):
    uberprint("IMPORTING PubChem")

    # Create PubChem schema and table
    with engine.connect() as conn:
        conn.execute(f"DROP SCHEMA IF EXISTS pubchem CASCADE;")
        conn.execute(f"CREATE SCHEMA pubchem;")
        conn.execute(f"set search_path to pubchem;")
        conn.execute("CREATE TABLE IF NOT EXISTS compounds (id SERIAL PRIMARY KEY, \
                                            cid VARCHAR NOT NULL, \
                                            charge BIGINT, \
                                            \"Compound_Canonicalized\" BIGINT, \
                                            \"Compound Complexity\" REAL, \
                                            \"Count_Hydrogen Bond Acceptor\" BIGINT, \
                                            \"Count_Hydrogen Bond Donor\" BIGINT, \
                                            \"Count_Rotatable Bond\" BIGINT, \
                                            \"Fingerprint_SubStructure Keys\" VARCHAR, \
                                            \"IUPAC Name_Allowed\" VARCHAR, \
                                            \"IUPAC Name_CAS-like Style\" VARCHAR, \
                                            \"IUPAC Name_Markup\" VARCHAR, \
                                            \"IUPAC Name_Preferred\" VARCHAR, \
                                            \"IUPAC Name_Systematic\" VARCHAR, \
                                            \"IUPAC Name_Traditional\" VARCHAR, \
                                            \"InChI_Standard\" VARCHAR, \
                                            \"InChIKey_Standard\" VARCHAR, \
                                            \"Log P_XLogP3-AA\" REAL, \
                                            \"Mass_Exact\" REAL, \
                                            \"Molecular Formula\" VARCHAR, \
                                            \"Molecular Weight\" REAL, \
                                            \"SMILES_Canonical\" VARCHAR, \
                                            \"SMILES_Isomeric\" VARCHAR, \
                                            \"Topological_Polar Surface Area\" REAL, \
                                            \"Weight_MonoIsotopic\" REAL, \
                                            \"Log P_XLogP3\" REAL, \
                                            \"count_heavy_atom\" BIGINT, \
                                            \"count_atom_chiral\" BIGINT, \
                                            \"count_atom_chiral_def\" BIGINT, \
                                            \"count_atom_chiral_undef\" BIGINT, \
                                            \"count_bond_chiral\" BIGINT, \
                                            \"count_bond_chiral_def\" BIGINT, \
                                            \"count_bond_chiral_undef\" BIGINT, \
                                            \"count_isotope_atom\" BIGINT, \
                                            \"count_covalent_unit\" BIGINT, \
                                            \"count_tautomers\" BIGINT);")

    # Query the DrugBank list
    with engine.connect() as conn:
        drugbank_list = conn.execute("SELECT identifier FROM drug_bank.drug_external_identifiers WHERE resource = \'PubChem Compound\'").fetchall()
    drugbank_list = [dict(row) for row in drugbank_list]

    # Break the drugbank list into batches of 200 to avoid overstressing the API
    drugbank_chunks = [drugbank_list[x:x + 100] for x in range(0, len(drugbank_list), 100)]

    chunk_counter = 0

    # Loop through the chunks
    for chunk in drugbank_chunks:
        chunk_counter = chunk_counter + 1
        print(f"Loading chunk {chunk_counter} of {len(drugbank_chunks)}")

        cid_list = []
        for element in chunk:
            cid_list.append(element['identifier'])
        cid_list = ",".join(cid_list)

        if len(cid_list) > 0:
            successful = 0

            while successful == 0:
                chem_response = requests.post('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/record/JSON', data={'cid': f"{cid_list}"})

                if chem_response.status_code == 200:
                    successful = 1
                else:
                    print(f"REQUEST FAILURE: Retrying get CIDs on chunk {chunk_counter}")

                # Sleep to avoid stressing API
                api_delay(chem_response.headers)

            chem_response = json.loads(chem_response.text)

            # Loop through compounds in the response and insert into db
            with engine.connect() as conn:
                for compound in chem_response["PC_Compounds"]:
                    compound_dict = {}

                    # Get the CID
                    if "id" in compound:
                        if "id" in compound["id"]:
                            if "cid" in compound["id"]["id"]:
                                compound_dict["cid"] = compound["id"]["id"]["cid"]

                    # Add the charge to the dict
                    compound_dict["charge"] = get_key(compound, "charge")

                    # Loop through properties and add to dict
                    for prop in compound["props"]:
                        if "label" in prop['urn'] and "name" in prop['urn']:
                            prop_full_name = f"{prop['urn']['label']}_{prop['urn']['name']}"
                        elif "label" in prop['urn']:
                            prop_full_name = f"{prop['urn']['label']}"
                        elif "name" in prop['urn']:
                            prop_full_name = f"{prop['urn']['name']}"

                        if "ival" in prop['value']:
                            compound_dict[prop_full_name] = get_key(prop['value'], "ival")
                        elif "fval" in prop['value']:
                            compound_dict[prop_full_name] = get_key(prop['value'], "fval")
                        elif "binary" in prop['value']:
                            compound_dict[prop_full_name] = get_key(prop['value'], "binary")
                        elif "sval" in prop['value']:
                            compound_dict[prop_full_name] = get_key(prop['value'], "sval")

                    # Loop through counts in the compound and add to dict
                    for count in compound["count"].keys():
                        compound_dict[f"count_{count}"] = get_key(compound["count"], count)

                    # Insert into the table
                    conn.execute(f"INSERT INTO compounds (cid, charge, \"Compound_Canonicalized\", \"Compound Complexity\", \"Count_Hydrogen Bond Acceptor\", \
                                                \"Count_Hydrogen Bond Donor\", \"Count_Rotatable Bond\", \"Fingerprint_SubStructure Keys\", \"IUPAC Name_Allowed\", \
                                                \"IUPAC Name_CAS-like Style\", \"IUPAC Name_Markup\", \"IUPAC Name_Preferred\", \"IUPAC Name_Systematic\", \
                                                \"IUPAC Name_Traditional\", \"InChI_Standard\", \"InChIKey_Standard\", \"Log P_XLogP3-AA\", \"Mass_Exact\", \
                                                \"Molecular Formula\", \"Molecular Weight\", \"SMILES_Canonical\", \"SMILES_Isomeric\", \
                                                \"Topological_Polar Surface Area\", \"Weight_MonoIsotopic\", \"Log P_XLogP3\", \"count_heavy_atom\", \
                                                \"count_atom_chiral\", \"count_atom_chiral_def\", \"count_atom_chiral_undef\", \"count_bond_chiral\", \
                                                \"count_bond_chiral_def\", \"count_bond_chiral_undef\", \"count_isotope_atom\", \"count_covalent_unit\", \
                                                \"count_tautomers\") VALUES ( \
                                            \'{get_key(compound_dict, 'cid')}\', \
                                            \'{get_key(compound_dict, 'charge')}\', \
                                            \'{get_key(compound_dict, 'Compound_Canonicalized')}\', \
                                            \'{get_key(compound_dict, 'Compound Complexity')}\', \
                                            \'{get_key(compound_dict, 'Count_Hydrogen Bond Acceptor')}\', \
                                            \'{get_key(compound_dict, 'Count_Hydrogen Bond Donor')}\', \
                                            \'{get_key(compound_dict, 'Count_Rotatable Bond')}\', \
                                            \'{get_key(compound_dict, 'Fingerprint_SubStructure Keys')}\', \
                                            \'{get_key(compound_dict, 'IUPAC Name_Allowed')}\', \
                                            \'{get_key(compound_dict, 'IUPAC Name_CAS-like Style')}\', \
                                            \'{get_key(compound_dict, 'IUPAC Name_Markup')}\', \
                                            \'{get_key(compound_dict, 'IUPAC Name_Preferred')}\', \
                                            \'{get_key(compound_dict, 'IUPAC Name_Systematic')}\', \
                                            \'{get_key(compound_dict, 'IUPAC Name_Traditional')}\', \
                                            \'{get_key(compound_dict, 'InChI_Standard')}\', \
                                            \'{get_key(compound_dict, 'InChIKey_Standard')}\', \
                                            {get_key(compound_dict, 'Log P_XLogP3-AA')}, \
                                            \'{get_key(compound_dict, 'Mass_Exact')}\', \
                                            \'{get_key(compound_dict, 'Molecular Formula')}\', \
                                            \'{get_key(compound_dict, 'Molecular Weight')}\', \
                                            \'{get_key(compound_dict, 'SMILES_Canonical')}\', \
                                            \'{get_key(compound_dict, 'SMILES_Isomeric')}\', \
                                            \'{get_key(compound_dict, 'Topological_Polar Surface Area')}\', \
                                            \'{get_key(compound_dict, 'Weight_MonoIsotopic')}\', \
                                            {get_key(compound_dict, 'Log P_XLogP3')}, \
                                            \'{get_key(compound_dict, 'count_heavy_atom')}\', \
                                            \'{get_key(compound_dict, 'count_atom_chiral')}\', \
                                            \'{get_key(compound_dict, 'count_atom_chiral_def')}\', \
                                            \'{get_key(compound_dict, 'count_atom_chiral_undef')}\', \
                                            \'{get_key(compound_dict, 'count_bond_chiral')}\', \
                                            \'{get_key(compound_dict, 'count_bond_chiral_def')}\', \
                                            \'{get_key(compound_dict, 'count_bond_chiral_undef')}\', \
                                            \'{get_key(compound_dict, 'count_isotope_atom')}\', \
                                            \'{get_key(compound_dict, 'count_covalent_unit')}\', \
                                            \'{get_key(compound_dict, 'count_tautomers')}\');")

    uberprint("IMPORT OF PubChem COMPLETE")


# Since PubChem uses an API, this is a no-op
def cleanup(PATH):
    print("No PubChem files to clean up.")


if __name__ == "__main__":
    # Get script directory
    CURRENT_PATH = str(os.path.dirname(os.path.realpath(__file__))) + "/.."

    # Import database configuration
    config = ConfigParser()
    config.read(f"{CURRENT_PATH}/database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    if not validate_data(engine):
        import_to_db(config, engine, CURRENT_PATH)
