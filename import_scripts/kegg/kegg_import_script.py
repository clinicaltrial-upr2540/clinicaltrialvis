import glob
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

# get data file names
path = r'C:\Development\School\CSCI-E 599\M3\code_4_23_2020\test_cases\import_scripts\kegg\data'
filenames = glob.glob(path + "/*.csv")
DATABASE_URL = "postgresql://YOUR_USER:YOUR_PASS@localhost:5432/postgres"

SCHEMA_NAME = "kegg"
# # Set up database
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

with engine.connect() as conn:
    # Create the table if necessary
    conn.execute(f"CREATE SCHEMA  IF NOT EXISTS {SCHEMA_NAME};")
    conn.execute(f"set search_path to {SCHEMA_NAME};")
    conn.close()

dfs = []
for filename in filenames:
    if "anatomialclass.csv" in filename:
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        data.to_sql('anatomialclass', con=engine, if_exists='replace', schema=SCHEMA_NAME)
        db.commit()
        print('anatomialclass inserted')
    if "crudeClass.csv" in filename:
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        data.to_sql('crudeclass', con=engine, if_exists='replace', schema=SCHEMA_NAME)
        db.commit()
        print('crudeclass inserted')
    if "drugAtcCodeAssociation.csv" in filename:
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        data.to_sql('drugatccodeassociation', con=engine, if_exists='replace', schema=SCHEMA_NAME)
        db.commit()
        print('drugatccodeassociation inserted')
    if "targetclass.csv" in filename:
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        data.to_sql('targetclass', con=engine, if_exists='replace', schema=SCHEMA_NAME)
        db.commit()
        print('targetclass inserted')
    if "uspclass.csv" in filename:
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        data.to_sql('uspclass', con=engine, if_exists='replace', schema=SCHEMA_NAME)
        db.commit()
        print('uspclass inserted')
