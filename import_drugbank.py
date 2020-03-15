#!/usr/bin/env python3

import os
import xmltodict
import json
import sqlalchemy

from sqlalchemy.orm import scoped_session, sessionmaker
from psycopg2.errors import SyntaxError as PostgresSyntaxError

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
                                    volume_of_distribution VARCHAR, \
                                    clearance VARCHAR, \
                                    fda_label VARCHAR, \
                                    msds VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_groups (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    drug_group VARCHAR NOT NULL);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_classification (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    description VARCHAR, \
                                    direct_parent VARCHAR, \
                                    kingdom VARCHAR, \
                                    superclass VARCHAR, \
                                    class VARCHAR, \
                                    subclass VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_categories (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    category VARCHAR, \
                                    mesh_id VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_synonyms (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    language VARCHAR, \
                                    coder VARCHAR, \
                                    name_text VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_products (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    labeller VARCHAR, \
                                    ndc_id VARCHAR, \
                                    ndc_product_code VARCHAR, \
                                    dpd_id VARCHAR, \
                                    ema_product_code VARCHAR, \
                                    started_marketing_on VARCHAR, \
                                    ended_marketing_on VARCHAR, \
                                    dosage_form VARCHAR, \
                                    strength VARCHAR, \
                                    route VARCHAR, \
                                    fda_application_number VARCHAR, \
                                    generic VARCHAR, \
                                    over_the_counter VARCHAR, \
                                    approved VARCHAR, \
                                    country VARCHAR, \
                                    source VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_mixtures (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    name VARCHAR, \
                                    ingredients VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_interactions (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    other_drugbank_id VARCHAR NOT NULL, \
                                    name VARCHAR, \
                                    description VARCHAR);")

    db.commit()


def get_key(json_object, key):
    if key in json_object and json_object[key] is not None:
        if isinstance(json_object[key], str):
            return(json_object[key].replace('\'', '\'\'').replace('(', r'$$($$').replace(')', r'$$)$$'))
            # return(f"$STR${json_object[key]}$STR$")
        else:
            return(json_object[key])
    else:
        return('')


# Function to insert a single drug into the main table
def insert_drug(drug):
    db.execute(f"set search_path to {SCHEMA_NAME};")
    try:
        # Insert the top level drug
        db.execute(f"INSERT INTO drugs (drugbank_id, name, description, cas_number, unii, \
                    state, indication, pharmacodynamics, \
                    mechanism_of_action, toxicity, \
                    metabolism, absorption, half_life, \
                    route_of_elimination, volume_of_distribution, clearance, fda_label, msds) \
                    VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug, 'name')}\', \
                    \'{get_key(drug, 'description')}\', \'{get_key(drug, 'cas-number')}\', \
                    \'{get_key(drug, 'unii')}\', \'{get_key(drug, 'state')}\', \'{get_key(drug, 'indication')}\', \
                    \'{get_key(drug, 'pharmacodynamics')}\', \'{get_key(drug, 'mechanism-of-action')}\', \
                    \'{get_key(drug, 'toxicity')}\', \'{get_key(drug, 'metabolism')}\', \
                    \'{get_key(drug, 'absorption')}\', \'{get_key(drug, 'half-life')}\', \
                    \'{get_key(drug, 'route-of-elimination')}\', \'{get_key(drug, 'volume-of-distribution')}\', \'{get_key(drug, 'clearance')}\', \'{get_key(drug, 'fda-label')}\', \
                    \'{get_key(drug, 'msds')}\');")

        # Insert the groups - TODO: fix some groups getting inserted letter by letter
        if drug['groups']['group'] is not None:
            for drug_group in drug['groups']['group']:
                db.execute(f"INSERT INTO drug_groups (drugbank_id, drug_group) \
                            VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{drug_group}\');")

        # Insert the classification(s)
        classification = drug["classification"]
        db.execute(f"INSERT INTO drug_classification (drugbank_id, description, \
                    direct_parent, kingdom, superclass, class, subclass) \
                    VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(classification, 'description')}\', \
                    \'{get_key(classification, 'direct_parent')}\', \'{get_key(classification, 'kingdom')}\', \
                    \'{get_key(classification, 'superclass')}\', \'{get_key(classification, 'class')}\', \
                    \'{get_key(classification, 'subclass')}\');")

        # Insert the categories
        for drug_category in drug['categories']['category']:
            db.execute(f"INSERT INTO drug_categories (drugbank_id, category, mesh_id) \
                        VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_category, 'category')}\', \'{get_key(drug_category, 'mesh-id')}\');")

        # Insert drug synonyms
        if drug['synonyms'] is not None and drug['synonyms']['synonym'] is not None:
            for drug_synonym in drug['synonyms']['synonym']:
                db.execute(f"INSERT INTO drug_synonyms (drugbank_id, language, coder, name_text) \
                            VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_category, '@language')}\', \
                            \'{get_key(drug_category, '@coder')}\', \'{get_key(drug_category, '#text')}\');")

        # Insert the products
        if drug['products'] is not None and drug['products']['product'] is not None:
            if isinstance(drug['products'], list):
                for drug_product in drug['products']['product']:
                    db.execute(f"INSERT INTO drug_products (drugbank_id, labeller, ndc_id, ndc_product_code, dpd_id, \
                                ema_product_code, started_marketing_on, ended_marketing_on, dosage_form, strength, \
                                route, fda_application_number, generic, over_the_counter, approved, country, source) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_product, 'labeller')}\', \
                                \'{get_key(drug_product, 'ndc-id')}\', \'{get_key(drug_product, 'ndc-product-code')}\', \
                                \'{get_key(drug_product, 'dpd-id')}\', \'{get_key(drug_product, 'ema-product-code')}\', \
                                \'{get_key(drug_product, 'started-marketing-on')}\', \'{get_key(drug_product, 'ended-marketing-on')}\', \
                                \'{get_key(drug_product, 'dosage-form')}\', \'{get_key(drug_product, 'strength')}\', \
                                \'{get_key(drug_product, 'route')}\', \'{get_key(drug_product, 'fda-application-number')}\', \
                                \'{get_key(drug_product, 'generic')}\', \'{get_key(drug_product, 'over-the-counter')}\', \
                                \'{get_key(drug_product, 'approved')}\', \'{get_key(drug_product, 'country')}\', \
                                \'{get_key(drug_product, 'source')}\');")
            else:
                drug_product = drug['products']['product']
                db.execute(f"INSERT INTO drug_products (drugbank_id, labeller, ndc_id, ndc_product_code, dpd_id, \
                                ema_product_code, started_marketing_on, ended_marketing_on, dosage_form, strength, \
                                route, fda_application_number, generic, over_the_counter, approved, country, source) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_product, 'labeller')}\', \
                                \'{get_key(drug_product, 'ndc-id')}\', \'{get_key(drug_product, 'ndc-product-code')}\', \
                                \'{get_key(drug_product, 'dpd-id')}\', \'{get_key(drug_product, 'ema-product-code')}\', \
                                \'{get_key(drug_product, 'started-marketing-on')}\', \'{get_key(drug_product, 'ended-marketing-on')}\', \
                                \'{get_key(drug_product, 'dosage-form')}\', \'{get_key(drug_product, 'strength')}\', \
                                \'{get_key(drug_product, 'route')}\', \'{get_key(drug_product, 'fda-application-number')}\', \
                                \'{get_key(drug_product, 'generic')}\', \'{get_key(drug_product, 'over-the-counter')}\', \
                                \'{get_key(drug_product, 'approved')}\', \'{get_key(drug_product, 'country')}\', \
                                \'{get_key(drug_product, 'source')}\');")

        # Insert the mixtures
        if drug['mixtures'] is not None and drug['mixtures']['mixture'] is not None:
            if isinstance(drug['mixtures'], list):
                for drug_mixture in drug['mixtures']['mixture']:
                    db.execute(f"INSERT INTO drug_mixtures (drugbank_id, name, ingredients) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_mixture, 'name')}\', \
                                \'{get_key(drug_mixture, 'ingredients')}\');")
            else:
                drug_mixture = drug['mixtures']['mixture']
                db.execute(f"INSERT INTO drug_mixtures (drugbank_id, name, ingredients) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_mixture, 'name')}\', \
                                \'{get_key(drug_mixture, 'ingredients')}\');")


        # Insert the interactions
        if drug['drug-interactions'] is not None and drug['drug-interactions']['drug-interaction'] is not None:
            for drug_interaction in drug['drug-interactions']['drug-interaction']:
                db.execute(f"INSERT INTO drug_interactions (drugbank_id, other_drugbank_id, name, description) \
                            VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_interaction, 'drugbank-id')}\', \
                            \'{get_key(drug_interaction, 'name')}\', \'{get_key(drug_interaction, 'description')}\');")

        db.commit()
    except ZeroDivisionError:
        pass
    # except KeyError:
    #     pass
    # except PostgresSyntaxError:
    #     pass
    # except sqlalchemy.exc.InvalidRequestError:
    #     pass


# Set up database
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# # Does the schema exist? If not, create
db.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
db.commit()

# Build the tables
build_main_table(db)

# Ugh, load in the whole thing, gross
with open('drugbank_full_database.xml') as inFh:
    data = xmltodict.parse(inFh.read())

# print(json.dumps(data["drugbank"]["drug"][0]))

for drug_to_insert in data["drugbank"]["drug"]:
    # Insert into the main table
    insert_drug(drug_to_insert)
