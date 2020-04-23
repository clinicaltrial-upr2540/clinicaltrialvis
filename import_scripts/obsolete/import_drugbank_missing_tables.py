#!/usr/bin/env python3

# This script is used to fix empty tables in the R import of DrugBank

import json
import xmltodict
import sqlalchemy

from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"
# DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@localhost:54320/postgres"
SCHEMA_NAME = "drug_bank"


def get_key(json_object, key):
    # if key in json_object and json_object[key] is not None:
    try:
        if isinstance(json_object[key], str):
            result = json_object[key].replace('\'', '\'\'').replace(r'(', r'\(').replace(r')', r'\)').replace(';', r'\;')
            # return(f"$STR${json_object[key]}$STR$")
        else:
            result = json_object[key]
    except Exception:
        result = ""

    return(result)


# Function to insert a single drug into the main table
def insert_drug(drug, counter):
    db.execute(f"set search_path to {SCHEMA_NAME};")
    try:
        # Get drugbank id
        if "#text" in drug['drugbank-id']:
            drugbank_id = drug['drugbank-id']['#text']
        else:
            drugbank_id = drug['drugbank-id'][0]['#text']

        # Insert external identifiers
        if "external-identifiers" in drug:
            if drug['external-identifiers'] is None or drug['external-identifiers']['external-identifier'] is None:
                pass
            elif "identifier" not in drug['external-identifiers']['external-identifier']:
                for drug_identifier in drug['external-identifiers']['external-identifier']:
                    counter["external_identifiers"] = counter["external_identifiers"] + 1
                    db.execute(f"INSERT INTO drug_external_identifiers (\"row.names\", resource, identifier, parent_key) VALUES ( \
                                \'{counter['external_identifiers']}\', \
                                \'{get_key(drug_identifier, 'resource')}\', \
                                \'{get_key(drug_identifier, 'identifier')}\', \
                                \'{drugbank_id}\');")
            else:
                drug_identifier = drug['external-identifiers']['external-identifier']
                counter["external_identifiers"] = counter["external_identifiers"] + 1
                db.execute(f"INSERT INTO drug_external_identifiers (\"row.names\", resource, identifier, parent_key) VALUES ( \
                                \'{counter['external_identifiers']}\', \
                                \'{get_key(drug_identifier, 'resource')}\', \
                                \'{get_key(drug_identifier, 'identifier')}\', \
                                \'{drugbank_id}\');")

        # Insert the dosages
        if "dosages" in drug:
            if drug['dosages'] is None or drug['dosages']['dosage'] is None:
                pass
            elif "form" not in drug['dosages']['dosage']:
                for drug_dosage in drug['dosages']['dosage']:
                    counter["dosages"] = counter["dosages"] + 1
                    db.execute(f"INSERT INTO drug_dosages (\"row.names\", form, route, strength, parent_key) VALUES ( \
                                \'{counter['dosages']}\', \
                                \'{get_key(drug_dosage, 'form')}\', \
                                \'{get_key(drug_dosage, 'route')}\', \
                                \'{get_key(drug_dosage, 'strength')}\', \
                                \'{drugbank_id}\');")
            else:
                drug_dosage = drug['dosages']['dosage']
                counter["dosages"] = counter["dosages"] + 1
                db.execute(f"INSERT INTO drug_dosages (\"row.names\", form, route, strength, parent_key) VALUES ( \
                                \'{counter['dosages']}\', \
                                \'{get_key(drug_dosage, 'form')}\', \
                                \'{get_key(drug_dosage, 'route')}\', \
                                \'{get_key(drug_dosage, 'strength')}\', \
                                \'{drugbank_id}\');")

        # Insert patents
        if "patents" in drug:
            if drug['patents'] is None or drug['patents']['patent'] is None:
                pass
            elif "number" not in drug['patents']['patent']:
                for patent in drug['patents']['patent']:
                    counter["patents"] = counter["patents"] + 1
                    db.execute(f"INSERT INTO drug_patents (\"row.names\", number, country, approved, expires,\"pediatric-extension\", parent_key) VALUES ( \
                                \'{counter['patents']}\', \
                                \'{get_key(patent, 'number')}\', \
                                \'{get_key(patent, 'country')}\', \
                                \'{get_key(patent, 'approved')}\', \
                                \'{get_key(patent, 'expires')}\', \
                                \'{get_key(patent, 'pediatric-extension')}\', \
                                \'{drugbank_id}\');")
            else:
                patent = drug['patents']['patent']
                counter["patents"] = counter["patents"] + 1
                db.execute(f"INSERT INTO drug_patents (\"row.names\", number, country, approved, expires, \"pediatric-extension\", parent_key) VALUES ( \
                                \'{counter['patents']}\', \
                                \'{get_key(patent, 'number')}\', \
                                \'{get_key(patent, 'country')}\', \
                                \'{get_key(patent, 'approved')}\', \
                                \'{get_key(patent, 'expires')}\', \
                                \'{get_key(patent, 'pediatric-extension')}\', \
                                \'{drugbank_id}\');")

        # Insert products
        if "products" in drug:
            if drug['products'] is None or drug['products']['product'] is None:
                pass
            elif "number" not in drug['products']['product']:
                for product in drug['products']['product']:
                    counter["products"] = counter["products"] + 1
                    db.execute(f"INSERT INTO drug_products (\"row.names\", name, labeller, \"ndc-id\", \"ndc-product-code\", \"dpd-id\", \"ema-product-code\", \
                                                            \"ema-ma-number\", \"started-marketing-on\", \"ended-marketing-on\", \"dosage-form\", strength, route, \
                                                            \"fda-application-number\", generic, \"over-the-counter\", approved, country, source, parent_key) VALUES ( \
                                \'{counter['products']}\', \
                                \'{get_key(product, 'name')}\', \
                                \'{get_key(product, 'labeller')}\', \
                                \'{get_key(product, 'ndc-id')}\', \
                                \'{get_key(product, 'ndc-product-code')}\', \
                                \'{get_key(product, 'dpd-id')}\', \
                                \'{get_key(product, 'ema-product-code')}\', \
                                \'{get_key(product, 'ema-ma-number')}\', \
                                \'{get_key(product, 'started-marketing-on')}\', \
                                \'{get_key(product, 'ended-marketing-on')}\', \
                                \'{get_key(product, 'dosage-form')}\', \
                                \'{get_key(product, 'strength')}\', \
                                \'{get_key(product, 'route')}\', \
                                \'{get_key(product, 'fda-application-number')}\', \
                                \'{get_key(product, 'generic')}\', \
                                \'{get_key(product, 'over-the-counter')}\', \
                                \'{get_key(product, 'approved')}\', \
                                \'{get_key(product, 'country')}\', \
                                \'{get_key(product, 'source')}\', \
                                \'{drugbank_id}\');")
            else:
                product = drug['products']['product']
                counter["products"] = counter["products"] + 1
                db.execute(f"INSERT INTO drug_products (\"row.names\", name, labeller, \"ndc-id\", \"ndc-product-code\", \"dpd-id\", \"ema-product-code\", \
                                                            \"ema-ma-number\", \"started-marketing-on\", \"ended-marketing-on\", \"dosage-form\", strength, route, \
                                                            \"fda-application-number\", generic, \"over-the-counter\", approved, country, source, parent_key) VALUES ( \
                                \'{counter['products']}\', \
                                \'{get_key(product, 'name')}\', \
                                \'{get_key(product, 'labeller')}\', \
                                \'{get_key(product, 'ndc-id')}\', \
                                \'{get_key(product, 'ndc-product-code')}\', \
                                \'{get_key(product, 'dpd-id')}\', \
                                \'{get_key(product, 'ema-product-code')}\', \
                                \'{get_key(product, 'ema-ma-number')}\', \
                                \'{get_key(product, 'started-marketing-on')}\', \
                                \'{get_key(product, 'ended-marketing-on')}\', \
                                \'{get_key(product, 'dosage-form')}\', \
                                \'{get_key(product, 'strength')}\', \
                                \'{get_key(product, 'route')}\', \
                                \'{get_key(product, 'fda-application-number')}\', \
                                \'{get_key(product, 'generic')}\', \
                                \'{get_key(product, 'over-the-counter')}\', \
                                \'{get_key(product, 'approved')}\', \
                                \'{get_key(product, 'country')}\', \
                                \'{get_key(product, 'source')}\', \
                                \'{drugbank_id}\');")

        db.commit()
    except Exception as e:
        error_file = open('errors.json', 'w')
        error_file.write(json.dumps(drug, indent=4, separators=(',', ': ')))
        error_file.close()

        raise(e)

        # counter["failed"] = counter["failed"] + 1
        # print(f"TOTAL FAILED: {counter['failed']}")

    if counter["overall"] % 100 == 0:
        print(f"Inserted {counter['overall']} drugs")

    return(counter)


######################################
# Begin main function
######################################

# Set up database
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# # Does the schema exist? If not, create
db.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
db.commit()

# Truncate the tables we want
db.execute(f"truncate table drug_bank.drug_external_identifiers;")
db.execute(f"truncate table drug_bank.drug_dosages;")
db.execute(f"truncate table drug_bank.drug_patents;")
db.execute(f"truncate table drug_bank.drug_products;")
db.commit()

# Ugh, load in the whole thing, gross
with open('../data/drugbank/drugbank_full_database.xml') as inFh:
    data = xmltodict.parse(inFh.read())

counter = {
    "overall": 0,
    "failed": 0,
    "external_identifiers": 0,
    "dosages": 0,
    "patents": 0,
    "products": 0
}

for drug_to_insert in data["drugbank"]["drug"]:
    counter["overall"] = counter["overall"] + 1

    # Insert into the main table
    counter = insert_drug(drug_to_insert, counter)
