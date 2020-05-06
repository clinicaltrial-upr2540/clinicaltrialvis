#!/usr/bin/env python3

# Description: this script import and persists the data from FDA

import os
import glob
import pandas as pd
import sqlalchemy

from configparser import ConfigParser
from zipfile import ZipFile


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


def import_fda(config, engine, FORCE):
    if FORCE or not check_for_schema(engine, "fda"):
        uberprint("IMPORTING FDA")

        # Set current working path
        current_path = str(os.path.dirname(os.path.realpath(__file__)))

        # Unzip the fda data file
        with ZipFile(f"{current_path}/../data/fda.zip", 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(f"{current_path}/../data/fda")

        # get data file names
        path = f"{current_path}/../data/fda"
        filenames = glob.glob(path + "/*.txt")

        # Create the schema if necessary
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
    else:
        uberprint("SKIPPING IMPORT OF FDA")


if __name__ == "__main__":
    # Import database configuration
    config = ConfigParser()
    config.read("../../app/database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    import_fda(config, engine, False)
