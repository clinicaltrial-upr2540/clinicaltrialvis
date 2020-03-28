#!/usr/bin/env python3

# Note: This script will NOT be used, in favor of using R with a predefined schema.

import os
import xmltodict
import json
import sqlalchemy

from sqlalchemy.orm import scoped_session, sessionmaker
from psycopg2.errors import SyntaxError as PostgresSyntaxError

# DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"
DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@localhost:54320/postgres"
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

    db.execute("CREATE TABLE IF NOT EXISTS drug_packagers (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    name VARCHAR, \
                                    url VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_manufacturers (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    generic VARCHAR, \
                                    url VARCHAR, \
                                    manufacturer_text VARCHAR);")

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
                                    name VARCHAR, \
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

    db.execute("CREATE TABLE IF NOT EXISTS drug_dosages (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    form VARCHAR, \
                                    route VARCHAR, \
                                    strength VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_sequences (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    format VARCHAR, \
                                    sequence_text VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_experimental_properties (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    kind VARCHAR, \
                                    value VARCHAR, \
                                    source VARCHAR);")

    db.execute("CREATE TABLE IF NOT EXISTS drug_external_identifiers (id SERIAL PRIMARY KEY, \
                                    drugbank_id VARCHAR NOT NULL, \
                                    resource VARCHAR, \
                                    identifier VARCHAR);")

    db.commit()


def get_key(json_object, key):
    if key in json_object and json_object[key] is not None:
        if isinstance(json_object[key], str):
            return(json_object[key].replace('\'', '\'\'').replace(r'(', r'\(').replace(r')', r'\)'))
            # return(f"$STR${json_object[key]}$STR$")
        else:
            return(json_object[key])
    else:
        return('')


# Function to insert a single drug into the main table
def insert_drug(drug, FAILED_COUNT):
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

        # Insert the groups
        if drug['groups']['group'] is not None:
            if isinstance(drug['groups']['group'], str):
                db.execute(f"INSERT INTO drug_groups (drugbank_id, drug_group) \
                            VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{drug['groups']['group']}\');")
            else:
                for drug_group in drug['groups']['group']:
                    db.execute(f"INSERT INTO drug_groups (drugbank_id, drug_group) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{drug_group}\');")

        # Insert the packagers
        if drug['packagers'] is not None and drug['packagers']['packager'] is not None:
            if "name" not in drug['packagers']['packager']:
                for drug_packager in drug['packagers']['packager']:
                    db.execute(f"INSERT INTO drug_packagers (drugbank_id, name, url) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_packager, 'name')}\', \
                                \'{get_key(drug_packager, 'url')}\');")
            else:
                drug_packager = drug['packagers']['packager']
                db.execute(f"INSERT INTO drug_packagers (drugbank_id, name, url) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_packager, 'name')}\', \
                                \'{get_key(drug_packager, 'url')}\');")

        # Insert the manufacturers
        if drug['manufacturers'] is not None and drug['manufacturers']['manufacturer'] is not None:
            if "#text" not in drug['manufacturers']['manufacturer']:
                for drug_manufacturer in drug['manufacturers']['manufacturer']:
                    db.execute(f"INSERT INTO drug_manufacturers (drugbank_id, generic, url, manufacturer_text) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_manufacturer, '@generic')}\', \
                                \'{get_key(drug_manufacturer, '@url')}\', \'{get_key(drug_manufacturer, '#text')}\');")
            else:
                drug_manufacturer = drug['manufacturers']['manufacturer']
                db.execute(f"INSERT INTO drug_manufacturers (drugbank_id, generic, url, manufacturer_text) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_manufacturer, '@generic')}\', \
                                \'{get_key(drug_manufacturer, '@url')}\', \'{get_key(drug_manufacturer, '#text')}\');")

        # Insert the classification(s)
        if "classification" in drug:
            classification = drug["classification"]
            db.execute(f"INSERT INTO drug_classification (drugbank_id, description, \
                        direct_parent, kingdom, superclass, class, subclass) \
                        VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(classification, 'description')}\', \
                        \'{get_key(classification, 'direct_parent')}\', \'{get_key(classification, 'kingdom')}\', \
                        \'{get_key(classification, 'superclass')}\', \'{get_key(classification, 'class')}\', \
                        \'{get_key(classification, 'subclass')}\');")

        # Insert the categories
        if "categories" in drug:
            if drug['categories'] is not None and drug['categories']['category'] is not None:
                if "mesh-id" not in drug['categories']['category']:
                    for drug_category in drug['categories']['category']:
                        db.execute(f"INSERT INTO drug_categories (drugbank_id, category, mesh_id) \
                                    VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_category, 'category')}\', \'{get_key(drug_category, 'mesh-id')}\');")
                else:
                    drug_category = drug['categories']['category']
                    db.execute(f"INSERT INTO drug_categories (drugbank_id, category, mesh_id) \
                                    VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_category, 'category')}\', \'{get_key(drug_category, 'mesh-id')}\');")

        # Insert drug synonyms
        if drug['synonyms'] is not None and drug['synonyms']['synonym'] is not None:
            if "#text" not in drug['synonyms']['synonym']:
                for drug_synonym in drug['synonyms']['synonym']:
                    db.execute(f"INSERT INTO drug_synonyms (drugbank_id, language, coder, name_text) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_synonym, '@language')}\', \
                                \'{get_key(drug_synonym, '@coder')}\', \'{get_key(drug_synonym, '#text')}\');")
            else:
                drug_synonym = drug['synonyms']['synonym']
                db.execute(f"INSERT INTO drug_synonyms (drugbank_id, language, coder, name_text) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_synonym, '@language')}\', \
                                \'{get_key(drug_synonym, '@coder')}\', \'{get_key(drug_synonym, '#text')}\');")

        # Insert the products
        if drug['products'] is not None and drug['products']['product'] is not None:
            if "name" not in drug['products']['product']:
                for drug_product in drug['products']['product']:
                    db.execute(f"INSERT INTO drug_products (drugbank_id, name, labeller, ndc_id, ndc_product_code, dpd_id, \
                                ema_product_code, started_marketing_on, ended_marketing_on, dosage_form, strength, \
                                route, fda_application_number, generic, over_the_counter, approved, country, source) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_product, 'name')}\', \'{get_key(drug_product, 'labeller')}\', \
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
                db.execute(f"INSERT INTO drug_products (drugbank_id, name, labeller, ndc_id, ndc_product_code, dpd_id, \
                                ema_product_code, started_marketing_on, ended_marketing_on, dosage_form, strength, \
                                route, fda_application_number, generic, over_the_counter, approved, country, source) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_product, 'name')}\', \'{get_key(drug_product, 'labeller')}\', \
                                \'{get_key(drug_product, 'ndc-id')}\', \'{get_key(drug_product, 'ndc-product-code')}\', \
                                \'{get_key(drug_product, 'dpd-id')}\', \'{get_key(drug_product, 'ema-product-code')}\', \
                                \'{get_key(drug_product, 'started-marketing-on')}\', \'{get_key(drug_product, 'ended-marketing-on')}\', \
                                \'{get_key(drug_product, 'dosage-form')}\', \'{get_key(drug_product, 'strength')}\', \
                                \'{get_key(drug_product, 'route')}\', \'{get_key(drug_product, 'fda-application-number')}\', \
                                \'{get_key(drug_product, 'generic')}\', \'{get_key(drug_product, 'over-the-counter')}\', \
                                \'{get_key(drug_product, 'approved')}\', \'{get_key(drug_product, 'country')}\', \
                                \'{get_key(drug_product, 'source')}\');")

        # Insert the mixtures
        if "mixtures" in drug:
            if drug['mixtures'] is not None and drug['mixtures']['mixture'] is not None:
                if "name" not in drug['mixtures']['mixture']:
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
        if "drug-interactions" in drug:
            if drug['drug-interactions'] is not None and drug['drug-interactions']['drug-interaction'] is not None:
                if "drugbank-id" not in drug['drug-interactions']['drug-interaction']:
                    for drug_interaction in drug['drug-interactions']['drug-interaction']:
                        db.execute(f"INSERT INTO drug_interactions (drugbank_id, other_drugbank_id, name, description) \
                                    VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_interaction, 'drugbank-id')}\', \
                                    \'{get_key(drug_interaction, 'name')}\', \'{get_key(drug_interaction, 'description')}\');")
                else:
                    drug_interaction = drug['drug-interactions']['drug-interaction']
                    db.execute(f"INSERT INTO drug_interactions (drugbank_id, other_drugbank_id, name, description) \
                                    VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_interaction, 'drugbank-id')}\', \
                                    \'{get_key(drug_interaction, 'name')}\', \'{get_key(drug_interaction, 'description')}\');")

        # Insert the dosages
        if "dosages" in drug:
            if drug['dosages'] is None or drug['dosages']['dosage'] is None:
                pass
            elif "form" not in drug['dosages']['dosage']:
                for drug_dosage in drug['dosages']['dosage']:
                    db.execute(f"INSERT INTO drug_dosages (drugbank_id, form, route, strength) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_dosage, 'form')}\', \
                                \'{get_key(drug_dosage, 'route')}\', \'{get_key(drug_dosage, 'strength')}\');")
            else:
                drug_dosage = drug['dosages']['dosage']
                db.execute(f"INSERT INTO drug_dosages (drugbank_id, form, route, strength) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_dosage, 'form')}\', \
                                \'{get_key(drug_dosage, 'route')}\', \'{get_key(drug_dosage, 'strength')}\');")

        # Insert the sequences
        if "sequences" in drug:
            if drug['sequences'] is None or drug['sequences']['sequence'] is None:
                pass
            elif "#text" not in drug['sequences']['sequence']:
                for drug_sequence in drug['sequences']['sequence']:
                    db.execute(f"INSERT INTO drug_sequences (drugbank_id, format, sequence_text) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_sequence, '@format')}\', \
                                \'{get_key(drug_sequence, '#text')}\');")
            else:
                drug_sequence = drug['sequences']['sequence']
                db.execute(f"INSERT INTO drug_sequences (drugbank_id, format, sequence_text) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_sequence, '@format')}\', \
                                \'{get_key(drug_sequence, '#text')}\');")

        # Insert the experimental properties
        if "experimental-properties" in drug:
            if drug['experimental-properties'] is None or drug['experimental-properties']['property'] is None:
                pass
            elif "kind" not in drug['experimental-properties']['property']:
                for drug_property in drug['experimental-properties']['property']:
                    db.execute(f"INSERT INTO drug_experimental_properties (drugbank_id, kind, value, source) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_property, 'kind')}\', \
                                \'{get_key(drug_property, 'value')}\', \'{get_key(drug_property, 'source')}\');")
            else:
                drug_property = drug['experimental-properties']['property']
                db.execute(f"INSERT INTO drug_experimental_properties (drugbank_id, kind, value, source) \
                                VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_property, 'kind')}\', \
                                \'{get_key(drug_property, 'value')}\', \'{get_key(drug_property, 'source')}\');")

        # Insert external identifiers
        if drug['external-identifiers'] is None or drug['external-identifiers']['external-identifier'] is None:
            pass
        elif "identifier" not in drug['external-identifiers']['external-identifier']:
            for drug_identifier in drug['external-identifiers']['external-identifier']:
                db.execute(f"INSERT INTO drug_external_identifiers (drugbank_id, resource, identifier) \
                            VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_identifier, 'resource')}\', \
                            \'{get_key(drug_identifier, 'identifier')}\');")
        else:
            drug_identifier = drug['external-identifiers']['external-identifier']
            db.execute(f"INSERT INTO drug_external_identifiers (drugbank_id, resource, identifier) \
                            VALUES (\'{drug['drugbank-id'][0]['#text']}\', \'{get_key(drug_identifier, 'resource')}\', \
                            \'{get_key(drug_identifier, 'identifier')}\');")

        db.commit()
    # except ZeroDivisionError:
    #     pass
    # except KeyError:
    #     # print(json.dumps(drug))
    #     exit(1)
    # except PostgresSyntaxError:
    #     pass
    except sqlalchemy.exc.StatementError:
        FAILED_COUNT = FAILED_COUNT + 1
        print(f"FAILED: {FAILED_COUNT}")


######################################
# Begin main function
######################################

FAILED_COUNT = 0

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
    insert_drug(drug_to_insert, FAILED_COUNT)
