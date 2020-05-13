#!/usr/bin/env python3 -u

# Description: this The top 200 records are the result of the analysis performed by Jon Tryggiv from department of
# Chemistry and Biochemistry at University of Arizona.

import os
import numpy as np
import pandas as pd
import sqlalchemy

from configparser import ConfigParser
from source_common import *


# Check if the Top200 data file exists
# Returns False or the path to the data file
def validate_downloaded_file(CURRENT_PATH):
    result = False
    FILENAME = "top_pharmaceuticals_poster_data.xlsx"
    PATH_LIST = [
        "/tmp/",
        "/Downloads/",
        "~/Downloads/",
        f"{CURRENT_PATH}/static_data/",
        f"{CURRENT_PATH}/../static_data/",
        f"{CURRENT_PATH}/data/",
        f"{CURRENT_PATH}/../data/"
    ]

    # Loop through dirs again to find the actual data file
    for item in PATH_LIST:
        if os.path.exists(f"{item}{FILENAME}"):
            result = f"{item}{FILENAME}"
            break

    return result


# Validate any top200 data present in the database
def validate_data(engine):
    print("Validating Top200 data...")

    result = True

    table_list = [
        "t200_pharm_prd_by_pres_2016",
        "t200_pharm_prd_by_rtl_sls_2018",
        "t200_sm_mol_pharm_rtl_sls_2018"
    ]

    try:
        for table in table_list:
            if not validate_table(engine, "top200", table):
                result = False
    except Exception as e:
        print(e)
        result = False

    return result


# Download the top200 data files
def download(PATH):
    print("Top200 data is not available for download. Skipping!")


# this function reads and parse the data frame produced from pdf/excel file
def pdf_table_parser(df):
    drug_name = pd.DataFrame()
    drug_brand_name = pd.DataFrame()
    scripts_number = pd.DataFrame()
    target_d = pd.DataFrame()
    for i in range(0, len(df.index), 4):
        drug_name = pd.concat([drug_name, df.iloc[i]], sort=False)
        drug_brand_name = pd.concat([drug_brand_name, df.iloc[i + 1]], sort=False)
        scripts_number = pd.concat([scripts_number, df.iloc[i + 2]], sort=False)
        target_d = pd.concat([target_d, df.iloc[i + 3]], sort=False)

        drug_name.reset_index(drop=True, inplace=True)
        drug_brand_name.reset_index(drop=True, inplace=True)
        scripts_number.reset_index(drop=True, inplace=True)
        target_d.reset_index(drop=True, inplace=True)

    drug_name.dropna(inplace=True)
    drug_name.reset_index(drop=True, inplace=True)
    drug_brand_name.dropna(inplace=True)
    drug_brand_name.reset_index(drop=True, inplace=True)
    scripts_number.dropna(inplace=True)
    scripts_number.reset_index(drop=True, inplace=True)
    target_d.dropna(inplace=True)
    target_d.reset_index(drop=True, inplace=True)
    drug_name = drug_name[~drug_name.applymap(np.isreal).all(1)]
    drug_name.reset_index(drop=True, inplace=True)
    final_df = pd.concat([drug_name, drug_brand_name, scripts_number, target_d], axis=1)
    final_df.columns = ["drug_name", "drug_brand_name", "scripts_number", "target_d"]

    final_df['drug_brand_name'] = final_df['drug_brand_name'].str.replace("(", "")
    final_df['drug_brand_name'] = final_df['drug_brand_name'].str.replace(")", "")

    return final_df


# Function to import top200 data
def import_to_db(config, engine, PATH):
    uberprint("IMPORTING Top200")

    # Drop existing data
    with engine.connect() as conn:
        conn.execute("DROP SCHEMA IF EXISTS top200 CASCADE;")
        conn.execute("CREATE SCHEMA top200;")

    # the following lines read excel information from excel sheet and converts them into readable dataframes.
    t200_sm_mol_pharm_rtl_sls_2018 = pd.read_excel(f"{PATH}/static_data/top_pharmaceuticals_poster_data.xlsx",
                                                   sheet_name='t200_sm_mol_pharm_rtl_sls_2018', header=None)
    t200_pharm_prd_by_pres_2016 = pd.read_excel(f"{PATH}/static_data/top_pharmaceuticals_poster_data.xlsx",
                                                sheet_name='t200_pharm_prd_by_pres_2016', header=None)
    t_200_pharm_prd_by_rtl_sls_2018 = pd.read_excel(f"{PATH}/static_data/top_pharmaceuticals_poster_data.xlsx",
                                                    sheet_name='t_200_pharm_prd_by_rtl_sls_2018', header=None)

    # Parse and converts excel sheets to data frames
    t200_sm_mol_pharm_rtl_sls_2018_df = pdf_table_parser(t200_sm_mol_pharm_rtl_sls_2018)
    t200_pharm_prd_by_pres_2016_df = pdf_table_parser(t200_pharm_prd_by_pres_2016)
    t_200_pharm_prd_by_rtl_sls_2018_df = pdf_table_parser(t_200_pharm_prd_by_rtl_sls_2018)

    # Writes the dataframes to PostgreSQL DB
    t200_sm_mol_pharm_rtl_sls_2018_df.to_sql('t200_sm_mol_pharm_rtl_sls_2018', con=engine, if_exists='replace',
                                             schema='top200')
    t200_pharm_prd_by_pres_2016_df.to_sql('t200_pharm_prd_by_pres_2016', con=engine, if_exists='replace', schema='top200')
    t_200_pharm_prd_by_rtl_sls_2018_df.to_sql('t200_pharm_prd_by_rtl_sls_2018', con=engine, if_exists='replace',
                                              schema='top200')

    print('top 200 records are successfully inserted')

    uberprint("IMPORT OF Top200 COMPLETE")


# Remove downloaded top200 files
def cleanup(PATH):
    print("Skipping cleanup of top200 files.")


if __name__ == "__main__":
    # Get script directory
    CURRENT_PATH = str(os.path.dirname(os.path.realpath(__file__))) + "/.."

    # Import database configuration
    config = ConfigParser()
    config.read(f"{CURRENT_PATH}/database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    validate_downloaded_file(CURRENT_PATH)
    import_to_db(config, engine, CURRENT_PATH)
