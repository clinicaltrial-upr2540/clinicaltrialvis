#!/usr/bin/env python3

import os
import sqlalchemy
import glob
import shutil
import pandas as pd

from zipfile import ZipFile
from configparser import ConfigParser
from source_common import *


# Check if the DrugBank data file exists
# If it is zipped, unzip it
# Returns False or the path to the XML
def validate_downloaded_file(CURRENT_PATH):
    result = False
    FILENAME = "fda"
    PATH_LIST = [
        "/tmp/",
        "/Downloads/",
        "~/Downloads/",
        f"{CURRENT_PATH}/data/",
        f"{CURRENT_PATH}/../data/"
    ]

    # Loop through possible locations to unzip file if found
    for item in PATH_LIST:
        if os.path.exists(f"{item}{FILENAME}.zip"):
            # Unzip the thing
            with ZipFile(f"{item}{FILENAME}.zip", 'r') as zipObj:
                zipObj.extractall(f"{str(os.path.dirname(item))}/fda")
            break

    # Loop through dirs again to find the actual data file
    for item in PATH_LIST:
        if os.path.exists(f"{item}{FILENAME}"):
            result = f"{item}{FILENAME}"
            break

    return result


def validate_data(engine):
    print("Validating FDA data...")

    result = True

    table_list = [
        "applicationdocs",
        "applications",
        "applicationsdocstypelookup",
        "marketingstatus",
        "marketingstatuslookup",
        "products",
        "submissionclasslookup",
        "submissionpropertytype",
        "submissions"
    ]

    try:
        for table in table_list:
            if not validate_table(engine, "fda", table):
                result = False
    except Exception as e:
        print(e)
        result = False

    return result


# Download the FDA data files
def download(PATH):
    print("Downloading FDA data.")
    download_http("https://www.fda.gov/media/89850/download", "fda.zip", PATH)


# Function to import fda data
def import_to_db(config, engine, PATH, FORCE):
    uberprint("IMPORTING FDA")

    # get data file names
    filenames = glob.glob(PATH + "/data/fda" + "/*.txt")

    # Drop and recreate the schema
    with engine.connect() as conn:
        conn.execute(f"DROP SCHEMA IF EXISTS fda CASCADE;")
        conn.execute(f"CREATE SCHEMA fda;")

    for filename in filenames:
        if "Products.txt" in filename or "Products.txt" in filename:
            if "ActionTypes_Lookup.txt" in filename:
                data = pd.read_csv(filename, header=0, error_bad_lines=False, sep='\t')
                data["ActionTypes_LookupID"] = data.ActionTypes_LookupID.astype(int)
                data.to_sql('actiontypeslookup', con=engine, if_exists='replace', schema='fda')
                print('actiontypeslookup inserted')
            elif "Products.txt" in filename:
                data = pd.read_csv(filename, header=0, error_bad_lines=False, sep='\t')
                data["ApplNo"] = data.ApplNo.astype(int)
                data["ProductNo"] = pd.to_numeric(data["ProductNo"], downcast='integer')
                data.to_sql('products', con=engine, if_exists='replace', schema='fda')
                print('Products inserted')
        else:
            d = []
            try:
                with open(filename, 'r', encoding='windows-1252') as source:
                    for line in source:
                        fields = line.split('\t')
                        cleansed = [s.strip(';') for s in fields]
                        d.append(cleansed)
                    df = pd.DataFrame(d, columns=d[0])
                    df = df.iloc[1:]

                    df = df.replace('\n', '', regex=True)
                    df = df.replace(r'\\n', '', regex=True)
                    df = df.dropna()
                    if "ApplicationDocs.txt" in filename:
                        df.to_sql('applicationdocs', con=engine, if_exists='replace', schema='fda')
                        print('applicationdocs inserted')
                    elif "Applications.txt" in filename:
                        df.to_sql('applications', con=engine, if_exists='replace', schema='fda')
                        print('applications inserted')
                    elif "ApplicationsDocsType_Lookup.txt" in filename:
                        df.to_sql('applicationsdocstypelookup', con=engine, if_exists='replace', schema='fda')
                        print('applicationsdocstypelookup inserted')
                    elif "MarketingStatus.txt" in filename:
                        df.to_sql('marketingstatus', con=engine, if_exists='replace', schema='fda')
                        print('marketingstatus inserted')
                    elif "MarketingStatus_Lookup.txt" in filename:
                        df.to_sql('marketingstatuslookup', con=engine, if_exists='replace', schema='fda')
                        print('marketingstatuslookup inserted')
                    elif "SubmissionClass_Lookup.txt" in filename:
                        df.to_sql('submissionclasslookup', con=engine, if_exists='replace', schema='fda')
                        print('submissionclasslookup inserted')
                    elif "Submissions.txt" in filename:
                        df.to_sql('submissions', con=engine, if_exists='replace', schema='fda')
                        print('submissions inserted')
                    elif "SubmissionPropertyType.txt" in filename:
                        df.to_sql('submissionpropertytype', con=engine, if_exists='replace', schema='fda')
                        print('submissionpropertytype inserted')
                    elif "TE.txt" in filename:
                        df.to_sql('te', con=engine, if_exists='replace', schema='fda')
                        print('te inserted')
            except UnicodeDecodeError:
                print(f"ERROR: Could not decode: {filename}")
                raise

    uberprint("IMPORT OF FDA COMPLETE")


def cleanup(PATH):
    print("Cleaning up fda files.")
    try:
        shutil.rmtree(f"{PATH}/data/fda")
        os.remove(f"{PATH}/data/fda.zip")
    except Exception:
        pass


if __name__ == "__main__":
    # Get script directory
    CURRENT_PATH = str(os.path.dirname(os.path.realpath(__file__))) + "/.."

    # Import database configuration
    config = ConfigParser()
    config.read("../database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    download(CURRENT_PATH)
    validate_downloaded_file(CURRENT_PATH)
    import_to_db(config, engine, CURRENT_PATH, True)
    cleanup(CURRENT_PATH)
