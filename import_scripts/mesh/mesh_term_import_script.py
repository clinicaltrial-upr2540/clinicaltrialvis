# The provided script inventories all available mesh IDs in ChemBL database and once all mesh IDs are found,
# the script finds the corresponding disease classification in the downloaded MeshData file and persists disease
# classification back to database

import re
import pandas
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

terms, ui_terms, ui_numbers, number_uis = {}, {}, {}, {}
numbers = []

DATABASE_URL = "postgresql://YOUR_USERNAME:YOUR_PASSWORD@DB_URL:5432/drugdata"

# retrieving the mesh term ids
meshFile = 'd2020.bin'
with open(meshFile, mode='rb') as file:
    mesh = file.readlines()
# the following for loop read through
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

engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

#The following section,inventories all available mesh IDs in ChemBL database
connection = engine.connect()
sql_statement = 'select DISTINCT drug_indication.mesh_id, compound_records.compound_name	 from drugdata.chembl_26.drug_indication inner join drugdata.chembl_26.compound_records compound_records on compound_records.record_id = drug_indication.record_id'
result = connection.execute(sql_statement)
result = [dict(row) for row in result]
df = pandas.DataFrame(result)

#  Once all mesh IDs are found, following line joins the mesh_ids with the corresponding disease classification
df['disease'] = df['mesh_id'].apply(get_disease)

# Persisting the data into data base
SCHEMA_NAME = "mesh"

# Create the table if necessary
db.execute(f"set search_path to {SCHEMA_NAME};")
db.execute("CREATE TABLE IF NOT EXISTS mesh_term (id SERIAL PRIMARY KEY, \
                                \"mesh_id\" VARCHAR NULL, \
                                compound_name VARCHAR NULL, \
                                disease VARCHAR NULL);")
db.commit()

# Truncate the tables we want
db.execute(f"truncate table {SCHEMA_NAME}.mesh_term;")
db.commit()

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
for i in range(0, len(df.index)):
    print(df.loc[i, ['mesh_id']]['mesh_id'])
    print(df.loc[i, ['compound_name']]['compound_name'])
    print(df.loc[i, ['disease']]['disease'])

    db.execute(
        f"INSERT INTO {SCHEMA_NAME}.mesh_term (mesh_id, compound_name, disease) VALUES (\'{df.loc[i, ['mesh_id']]['mesh_id']}\', \'{df.loc[i, ['compound_name']]['compound_name']}\', \'{df.loc[i, ['disease']]['disease']}\')")
    db.commit()

print('script finished inserting records into database')

db.close()
