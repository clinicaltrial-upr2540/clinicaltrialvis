#!/usr/bin/env python3

# This script is used to import data for the unified visualizations

import json
import csv
import sqlalchemy

DATABASE_URL = "postgresql://postgres:L4LvB1QGv7wp@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"
# DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@localhost:54320/postgres"
SCHEMA_NAME = "application"

# Set up database
engine = sqlalchemy.create_engine(DATABASE_URL)

# Does the schema exist? If not, create
with engine.connect() as conn:
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")

# Create the tables
with engine.connect() as conn:
    conn.execute(f"set search_path to {SCHEMA_NAME};")
    conn.execute(f"DROP TABLE IF EXISTS cdc_descriptors;")
    conn.execute("CREATE TABLE cdc_descriptors (id SERIAL PRIMARY KEY, \
                                    company VARCHAR NOT NULL, \
                                    disease_class VARCHAR NOT NULL, \
                                    compound VARCHAR, \
                                    mw REAL, \
                                    clogp REAL, \
                                    arom BIGINT, \
                                    hba BIGINT, \
                                    hbd BIGINT, \
                                    rtb BIGINT, \
                                    psa REAL, \
                                    bpka REAL, \
                                    apka REAL);")

    conn.execute(f"DROP TABLE IF EXISTS cdc_data_all;")
    conn.execute("CREATE TABLE cdc_data_all (id SERIAL PRIMARY KEY, \
                                company VARCHAR NOT NULL, \
                                disease_class VARCHAR NOT NULL, \
                                counts BIGINT);")

# Open the first data file
with open('cdc_descriptors.csv') as in_file:
    data = csv.DictReader(in_file)

    # Insert cdc_descriptors data
    with engine.connect() as conn:
        for item in data:
            # Clean missing values
            for key in item.keys():
                if item[key] == "":
                    item[key] = "NULL"

            # Insert a record
            conn.execute(f"INSERT INTO {SCHEMA_NAME}.cdc_descriptors (company, disease_class, compound, mw, clogp, arom, hba, hbd, rtb, psa, bpka, apka) VALUES \
                        (\'{item.get('company')}\', \'{item.get('disease_class')}\', \'{item.get('compound')}\', {item.get('mw')}, {item.get('clogp')}, {item.get('arom')}, {item.get('hba')}, {item.get('hbd')}, {item.get('rtb')}, {item.get('psa')}, {item.get('bpka')}, {item.get('apka')})")

# Open the second data file
with open('cdc_data.json') as in_file:
    data = json.load(in_file)

    with engine.connect() as conn:
        for item in data["data"]:
            # Insert a record
            conn.execute(f"INSERT INTO {SCHEMA_NAME}.cdc_data_all (company, disease_class, counts) VALUES (\'{item['company']}\', \'{item['disease_class']}\', {item['counts']})")
