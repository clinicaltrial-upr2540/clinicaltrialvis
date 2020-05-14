#!/usr/bin/env python3 -u

import os
import sys
import sqlalchemy

from configparser import ConfigParser
from sqlalchemy.exc import ProgrammingError
from subprocess import Popen

# Set up path for local imports
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}")
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/modules")

import visualization_setup
import source_common
import source_drugbank
import source_pubchem
import source_fda
import source_mesh
import source_chembl
import source_drugcentral
import source_top200
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
    # Create the data directory if it doesn't already exist
    try:
        os.mkdir(f"{CURRENT_PATH}/data")
    except FileExistsError:
        pass

    # Import visualization data
    try:
        visualization_setup.import_visualization_demos(engine)
    except Exception:
        print("WARNING: Unable to refresh visualization data.")

    # DrugBank IMPORT PROCESS
    if not source_drugbank.validate_data(engine) or FORCE:
        drugbank_data = source_drugbank.validate_downloaded_file(CURRENT_PATH)

        if drugbank_data:
            source_drugbank.import_to_db(config, engine, CURRENT_PATH)
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
            source_fda.import_to_db(config, engine, CURRENT_PATH)
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

    # DrugCentral IMPORT PROCESS
    if source_drugcentral.validate_data(engine):
        data_sources["central_drug"]["imported"] = True
    if not data_sources["central_drug"]["imported"] or FORCE:
        # Download DrugCentral data
        source_drugcentral.download(CURRENT_PATH)

        drugcentral_data = source_drugcentral.validate_downloaded_file(CURRENT_PATH)

        # Import ChemBL data
        if drugcentral_data:
            source_drugcentral.import_to_db(config, engine, CURRENT_PATH)
        else:
            print("Unable to find DrugCentral data file.")
            uberprint("SKIPPING IMPORT OF DrugCentral")

        source_drugcentral.cleanup(CURRENT_PATH)
    else:
        uberprint("SKIPPING IMPORT OF DrugCentral")

    # Top200 IMPORT PROCESS
    if source_top200.validate_data(engine):
        data_sources["top200"]["imported"] = True
    if not data_sources["top200"]["imported"] or FORCE:
        top200_data = source_top200.validate_downloaded_file(CURRENT_PATH)

        # Import Top200 data
        if top200_data:
            source_top200.import_to_db(config, engine, CURRENT_PATH)
        else:
            print("Unable to find Top200 data file.")
            uberprint("SKIPPING IMPORT OF Top200")
    else:
        uberprint("SKIPPING IMPORT OF Top200")

    # Build the materialized views
    uberprint("BUILDING VIEWS")

    # Create schema if necessary
    with engine.connect() as conn:
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS curated;")

    directory = os.fsencode(f"{CURRENT_PATH}/ddl/")

    # Loop through sql files in ddl/ and execute each one
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".sql"):
            # Build command to import a single view
            command = f"{find_binary('psql')} -h {config['drugdata']['host']} " \
                f"-d {config['drugdata']['database']} " \
                f"-p {config['drugdata']['port']} " \
                f"-U {config['drugdata']['user']} " \
                f"-f {CURRENT_PATH}/ddl/{filename}"

            # Run the command
            p = Popen(command, shell=True, env={
                'PGPASSWORD': config['drugdata']['password']
            })
            p.wait()

    uberprint("BUILDING VIEWS COMPLETE")

    # Create application user
    APP_USER_PASSWORD = generatePassword(16)

    with engine.connect() as conn:
        try:
            conn.execute("CREATE USER app_user;")
            conn.execute(f"ALTER USER app_user WITH ENCRYPTED PASSWORD '{APP_USER_PASSWORD}';")
            conn.execute(f"GRANT ro_role TO app_user;")

            print("Created app_user account. Save the following username and password to configure the ChemDataExplorer application:")
            print("THESE CREDENTIALS ARE ONLY PROVIDED ONCE!")
            print("")
            print("    Username: app_user")
            print(f"    Password: {APP_USER_PASSWORD}")
            print("")
            print("Launch the application with the following command:")
            print(f"    docker run -e DB_USER=app_user -e DB_PASSWORD={APP_USER_PASSWORD} -e DB_HOST={config['drugdata']['host']} -e DB_PORT={config['drugdata']['port']} -e DB_NAME={config['drugdata']['database']} -p 5000:5000 chemdataexplorer/chemdataexplorer:latest")
        except Exception:
            print("app_user account already exists.")
            print("")
            print("Launch the application with the following command:")
            print(f"    docker run -e DB_USER=app_user -e DB_PASSWORD=<password> -e DB_HOST={config['drugdata']['host']} -e DB_PORT={config['drugdata']['port']} -e DB_NAME={config['drugdata']['database']} -p 5000:5000 chemdataexplorer/chemdataexplorer:latest")


# If called as a script, set up database connection and execute main()
if __name__ == "__main__":
    # Get script directory
    CURRENT_PATH = str(os.path.dirname(os.path.realpath(__file__)))

    # Import database configuration
    config = ConfigParser()
    config.read(f"{CURRENT_PATH}/database.conf")

    # If environment variables are present, override config file
    if "drugdata" not in config:
        config["drugdata"] = {}
    if "DB_USER" in os.environ:
        config["drugdata"]["user"] = os.environ.get("DB_USER")
    if "DB_PASSWORD" in os.environ:
        config["drugdata"]["password"] = os.environ.get("DB_PASSWORD")
    if "DB_HOST" in os.environ:
        config["drugdata"]["host"] = os.environ.get("DB_HOST")
    if "DB_PORT" in os.environ:
        config["drugdata"]["port"] = os.environ.get("DB_PORT")
    if "DB_NAME" in os.environ:
        config["drugdata"]["database"] = os.environ.get("DB_NAME")

    # Initial connection to create database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)
    try:
        conn = engine.connect()
        conn.connection.connection.set_isolation_level(0)
        conn.execute(f"CREATE DATABASE {config['drugdata']['database']};")
        conn.connection.connection.set_isolation_level(1)
        conn.close()
    except ProgrammingError:
        print("Database already exists.")
        conn.close()

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    main(config, engine, CURRENT_PATH, False)
