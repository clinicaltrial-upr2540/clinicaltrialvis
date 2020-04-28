#!/usr/bin/env python3

import requests
import sqlalchemy
import sys
import os

from ftplib import FTP
from os import path
from configparser import ConfigParser

# Set up path for local imports
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}")
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/modules")

# Custom imports
import data_processors
import import_fda
import import_pubchem
import import_mesh

data_sources = {
    "central_drug": {
        "mode": "open",
        "type": "http",
        "url": "http://unmtid-shinyapps.net/download/drugcentral.dump.08262018.sql.gz",
        "filename": "drugcentral.sql.gz"
    },
    "chembl_26": {
        "mode": "open",
        "type": "ftp",
        "ftp_site": "ftp.ebi.ac.uk",
        "ftp_path": "pub/databases/chembl/ChEMBLdb/latest",
        "filename": "chembl_26_postgresql.tar.gz"
    },
    "drug_bank": {
        "mode": "closed"
    },
    "fda": {
        "mode": "open",
        "type": "http",
        "url": "https://www.fda.gov/media/89850/download",
        "filename": "fda.zip"
    },
    "kegg": {
        "mode": "closed",
    },
    "mesh": {
        "mode": "open",
        "type": "ftp",
        "ftp_site": "nlmpubs.nlm.nih.gov",
        "ftp_path": "online/mesh/MESH_FILES/asciimesh",
        "filename": "d2020.bin"
    },
    "pubchem": {
        "mode": "open",
        "type": "api"
    },
    "top200": {
        "mode": "closed",

    }
}


# Function to download a data file via FTP
def download_ftp(ftp_site, ftp_path, filename):
    # Set up FTP connection
    ftp = FTP(ftp_site)
    ftp.login()
    ftp.cwd(ftp_path)

    # Open file for writing and download file
    file = open(f"data/{filename}", 'wb')
    ftp.retrbinary('RETR ' + filename, file.write)

    # Close file and FTP connection
    file.close()
    ftp.quit()


# Function to download a data via http
def download_http(url, filename):
    filedata = requests.get(url)

    with open(f"data/{filename}", 'wb') as f:
        f.write(filedata.content)


# Begin main function here
def main(FORCE):
    # Import database configuration
    config = ConfigParser()
    config.read("../app/database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    # Download all public data files
    for key, value in data_sources.items():
        if value["mode"] == "open" and (value["type"] == "ftp" or value["type"] == "http"):
            if not path.exists(f"data/{value['filename']}"):
                print(f"Downloading {key}...")

                # Perform the appropriate download type
                if value["type"] == "ftp":
                    try:
                        download_ftp(value["ftp_site"], value["ftp_path"], value["filename"])
                        value["downloaded"] = True
                    except:
                        print(f"Failed to download {value['filename']}")
                        value["downloaded"] = False
                if value["type"] == "http":
                    try:
                        download_http(value["url"], value["filename"])
                        value["downloaded"] = True
                    except:
                        print(f"Failed to download {value['filename']}")
                        value["downloaded"] = False
            else:
                print(f"{value['filename']} has already been downloaded.")
                value["downloaded"] = True

    # Clean the public schema
    # THIS DELETES EVERYTHING IN public
    with engine.connect() as conn:
        conn.execute("DROP SCHEMA public CASCADE;")
        conn.execute("CREATE SCHEMA public;")

    # Import ChemBL
    if(data_sources["chembl_26"]["downloaded"]):
        try:
            data_processors.import_chembl(config, engine, FORCE)
            data_sources["chembl_26"]["imported"] = True
        except Exception as e:
            print("ERROR: Unable to import ChemBL")
            print(e)
            data_sources["chembl_26"]["imported"] = False

    # Import DrugCentral
    if(data_sources["central_drug"]["downloaded"]):
        try:
            data_processors.import_drugcentral(config, engine, FORCE)
            data_sources["central_drug"]["imported"] = True
        except Exception as e:
            print("ERROR: Unable to import DrugCentral")
            print(e)
            data_sources["central_drug"]["imported"] = False

    # Import DrugBank
    try:
        data_processors.import_drugbank(config, engine, FORCE)
        data_sources["drug_bank"]["imported"] = True
    except Exception as e:
        print("ERROR: Unable to import DrugCentral")
        print(e)
        data_sources["drug_bank"]["imported"] = False

    if(data_sources["fda"]["downloaded"]):
        try:
            import_fda.import_fda(config, engine, FORCE)
            data_sources["fda"]["imported"] = True
        except Exception as e:
            print("ERROR: Unable to import fda")
            print(e)
            data_sources["fda"]["imported"] = False

    # Import pubchem
    if not data_sources["drug_bank"]["imported"]:
        print("ERROR: Unable to import PubChem without DrugBank data")
    else:
        try:
            import_pubchem.import_pubchem(config, engine, FORCE)
            data_sources["pubchem"]["imported"] = True
        except Exception as e:
            print("ERROR: Unable to import PubChem")
            print(e)
            data_sources["pubchem"]["imported"] = False

    # Import MeSH
    if not data_sources["drug_bank"]["imported"]:
        print("ERROR: Unable to import MeSH without DrugBank data")
    elif(data_sources["mesh"]["downloaded"]):
        try:
            import_mesh.import_mesh(config, engine, FORCE)
            data_sources["mesh"]["imported"] = True
        except Exception as e:
            print("ERROR: Unable to import MeSH")
            print(e)
            data_sources["mesh"]["imported"] = False


if __name__ == "__main__":
    main(False)
