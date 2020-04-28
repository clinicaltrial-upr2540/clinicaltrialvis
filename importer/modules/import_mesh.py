#!/usr/bin/env python3

# The provided script inventories all available mesh IDs in ChemBL database and once all mesh IDs are found,
# the script finds the corresponding disease classification in the downloaded MeshData file and persists disease
# classification back to database

import re
import pandas
import sqlalchemy
from configparser import ConfigParser


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


def import_mesh(config, engine, FORCE):
    if not check_for_schema(engine, "drug_bank"):
        uberprint("Unable to import MeSH without DrugBank data")
    elif FORCE or not check_for_schema(engine, "mesh"):
        uberprint("IMPORTING MeSH")

        # (Re)create the schema
        with engine.connect() as conn:
            conn.execute(f"DROP SCHEMA IF EXISTS mesh CASCADE;")
            conn.execute(f"CREATE SCHEMA mesh;")

            # Create the table
            conn.execute("CREATE TABLE mesh.mesh_term (id SERIAL PRIMARY KEY, \
                                            \"mesh_id\" VARCHAR NULL, \
                                            compound_name VARCHAR NULL, \
                                            disease VARCHAR NULL);")

        terms, ui_terms, ui_numbers, number_uis = {}, {}, {}, {}
        numbers = []

        # retrieving the mesh term ids
        print("Reading MeSh data file...")
        with open("data/d2020.bin", mode='rb') as file:
            mesh = file.readlines()

        # Read through the data
        for line in mesh:
            meshTerm = re.search(b'MH = (.+)$', line)
            if meshTerm:
                term = meshTerm.group(1).decode('utf-8')

            meshNumber = re.search(b'MN = (.+)$', line)
            if meshNumber:
                numbers.append(meshNumber.group(1).decode('utf-8'))

            meshUI = re.search(b'UI = (.+)$', line)
            if meshUI:
                ui = meshUI.group(1).decode('utf-8')
                ui_terms[ui] = term
                ui_numbers[ui] = numbers

                if term in terms:
                    terms[term] = terms[term] + ' ' + ui
                else:
                    terms[term] = ui
                for numb in numbers:
                    if numb in number_uis:
                        number_uis[numb] = number_uis[numb] + ' ' + ui
                    else:
                        number_uis[numb] = ui
                numbers = []

        # gets the list of all disease class based on found ui_numbers and ui_terms
        get_disease = lambda x: ui_numbers[x][0][:3] + ' ' + ui_terms[number_uis[ui_numbers[x][0][:3]]]

        # Inventory all available mesh IDs in ChemBL database
        print("Getting available MeSH IDs from DrugBank...")
        with engine.connect() as conn:
            result = conn.execute("select DISTINCT drug_indication.mesh_id, compound_records.compound_name from drugdata.chembl_26.drug_indication inner join drugdata.chembl_26.compound_records compound_records on compound_records.record_id = drug_indication.record_id")
        result = [dict(row) for row in result]
        df = pandas.DataFrame(result)

        #  Once all mesh IDs are found, following line joins the mesh_ids with the corresponding disease classification
        df['disease'] = df['mesh_id'].apply(get_disease)

        # Cleansing the data sets by removing extra parentheses and single quotes
        df['mesh_id'] = df['mesh_id'].str.replace("(", "")
        df['mesh_id'] = df['mesh_id'].str.replace(")", "")
        df['mesh_id'] = df['mesh_id'].str.replace("'", "")

        df['compound_name'] = df['compound_name'].str.replace("(", "")
        df['compound_name'] = df['compound_name'].str.replace(")", "")
        df['compound_name'] = df['compound_name'].str.replace("'", "")

        df['disease'] = df['disease'].str.replace("(", "")
        df['disease'] = df['disease'].str.replace(")", "")
        df['disease'] = df['disease'].str.replace("'", "")

        # the following for loop, iterates through data frame and inserts each row into database
        print("Inserting MeSH records into database...")
        with engine.connect() as conn:
            for i in range(0, len(df.index)):
                conn.execute(f"INSERT INTO mesh.mesh_term (mesh_id, compound_name, disease) VALUES ( \
                    \'{df.loc[i, ['mesh_id']]['mesh_id']}\', \
                    \'{df.loc[i, ['compound_name']]['compound_name']}\', \
                    \'{df.loc[i, ['disease']]['disease']}\')")

        print('Finished inserting mesh records into database!')
        uberprint("IMPORT OF MeSh COMPLETE")
    else:
        uberprint("SKIPPING IMPORT OF MeSH")


if __name__ == "__main__":
    # Import database configuration
    config = ConfigParser()
    config.read("../../app/database.conf")

    # Connect to database
    DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
    engine = sqlalchemy.create_engine(DATABASE_URL)

    import_mesh(config, engine, True)
