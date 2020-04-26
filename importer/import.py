#!/usr/bin/env python3

import requests
import sqlalchemy

from ftplib import FTP
from os import path
from configparser import ConfigParser

import data_processors

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
def main():
    FORCE = False

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
                    download_ftp(value["ftp_site"], value["ftp_path"], value["filename"])
                if value["type"] == "http":
                    download_http(value["url"], value["filename"])
            else:
                print(f"{value['filename']} has already been downloaded.")

    # Import ChemBL
    data_processors.import_chembl(config, engine, FORCE)
    data_processors.import_drugcentral(config, engine, FORCE)


if __name__ == "__main__":
    main()
