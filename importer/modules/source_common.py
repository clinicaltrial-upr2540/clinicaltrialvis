#!/usr/bin/env python3 -u

# Module with various utility functions to support the process of downloading and
# importing data into the ChemDataExplorer database

import requests
import os

from ftplib import FTP


def uberprint(toprint):
    print("\n" + ("*" * len(toprint)) + "****")
    print(f"* {toprint} *")
    print("*" * len(toprint) + "****\n")


def check_for_schema(engine, schema):
    with engine.connect() as conn:
        result = conn.execute(f"SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = '{schema}');").fetchone()

    if list(result)[0] is True:
        return True
    else:
        return False


# Function to confirm there's data present in a table
# Returns True if data is present, False if not
def validate_table(engine, schema, table):
    with engine.connect() as conn:
        result = conn.execute(f"SELECT COUNT(*) FROM {schema}.{table};").fetchone()

    if int(list(result)[0]) > 0:
        return True
    else:
        return False


# Function to download a data file via HTTP
def download_http(url, filename, PATH):
    filedata = requests.get(url)

    with open(f"{PATH}/data/{filename}", 'wb') as f:
        f.write(filedata.content)


# Function to download a data file via FTP
def download_ftp(ftp_site, ftp_path, filename, PATH):
    # Set up FTP connection
    ftp = FTP(ftp_site)
    ftp.login()
    ftp.cwd(ftp_path)

    # Open file for writing and download file
    file = open(f"{PATH}/data/{filename}", 'wb')
    ftp.retrbinary('RETR ' + filename, file.write)

    # Close file and FTP connection
    file.close()
    ftp.quit()


# Function to find executables for Popen scripts
# (paths change depending on OS)
def find_binary(binary_name):
    result = f"/usr/local/bin/{binary_name}"
    PATHS = [
        "/usr/local/sbin",
        "/usr/local/bin",
        "/usr/sbin",
        "/usr/bin",
        "/sbin",
        "/bin",
        "/Library/Apple/usr/bin"
    ]

    for item in PATHS:
        if os.path.exists(f"{item}/{binary_name}"):
            result = f"{item}/{binary_name}"
            break

    return(result)
