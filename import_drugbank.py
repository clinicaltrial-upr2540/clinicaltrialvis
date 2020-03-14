#!/usr/bin/env python3

import os
import xmltodict
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"
SCHEMA_NAME = "drugbank"


# Function to create the primary drugs table
def build_main_table(db):
    db.execute(f"set search_path to {SCHEMA_NAME};")
    db.execute("CREATE TABLE IF NOT EXISTS drugs (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    name VARCHAR NOT NULL, \
                                    description VARCHAR, \
                                    cas_number VARCHAR, \
                                    unii VARCHAR, \
                                    state VARCHAR, \
                                    indication VARCHAR, \
                                    pharmacodynamics VARCHAR, \
                                    mechanism_of_action VARCHAR, \
                                    toxicity VARCHAR, \
                                    metabolism VARCHAR, \
                                    absorption VARCHAR, \
                                    half_life VARCHAR, \
                                    route_of_elimination VARCHAR, \
                                    fda_label VARCHAR);")
    db.commit()


def get_key(json_object, key):
    try:
        return(json_object[key].replace('"', r'\"').replace('\'', r'\\\''))
    except KeyError:
        return('')


# Function to insert a single drug into the main table
def insert_drug(drug):
    db.execute(f"set search_path to {SCHEMA_NAME};")
    db.execute(f"INSERT INTO drugs (drugbank_id, name, description, cas_number, unii, \
                                    state, indication, pharmacodynamics, \
                                    mechanism_of_action, toxicity, \
                                    metabolism, absorption, half_life, \
                                    route_of_elimination, fda_label) \
                                    VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug, 'name')}\', \
                                    \'{get_key(drug, 'description')}\', \'{get_key(drug, 'cas-number')}\', \
                                    \'{get_key(drug, 'unii')}\', \'{get_key(drug, 'state')}\', \'{get_key(drug, 'indication')}\', \
                                    \'{get_key(drug, 'pharmacodynamics')}\', \'{get_key(drug, 'mechanism-of-action')}\', \
                                    \'{get_key(drug, 'toxicity')}\', \'{get_key(drug, 'metabolism')}\', \
                                    \'{get_key(drug, 'absorption')}\', \'{get_key(drug, 'half-life')}\', \
                                    \'{get_key(drug, 'route-of-elimination')}\', \'{get_key(drug, 'fda-label')}\');")
    db.commit()


# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# # Does the schema exist? If not, create
db.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
db.commit()

# Build the main table
build_main_table(db)

# Ugh, load in the whole thing, gross
with open('drugbank_full_database.xml') as inFh:
    data = xmltodict.parse(inFh.read())

for drug_to_insert in data["drugbank"]["drug"]:
    insert_drug(drug_to_insert)
