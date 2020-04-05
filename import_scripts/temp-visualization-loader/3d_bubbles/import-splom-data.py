#!/usr/bin/env python3

# This script is used to import data for dotmatrix vis

import csv
import sqlalchemy

from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"
# DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@localhost:54320/postgres"
SCHEMA_NAME = "application"

# Set up database
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# # Does the schema exist? If not, create
db.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
db.commit()

# Create the table if necessary
db.execute(f"set search_path to {SCHEMA_NAME};")
db.execute("CREATE TABLE IF NOT EXISTS splomdata (id SERIAL PRIMARY KEY, \
                                \"group\" VARCHAR NOT NULL, \
                                variable VARCHAR NOT NULL, \
                                mw REAL, \
                                clogp REAL, \
                                psa REAL, \
                                hba BIGINT, \
                                hbd BIGINT);")
db.commit()

# Truncate the tables we want
db.execute(f"truncate table {SCHEMA_NAME}.splomdata;")
db.commit()

# Open the data file
in_file = open('splom_data_C14.csv')
data = csv.DictReader(in_file)

for item in data:
    # Insert a record
    db.execute(f"INSERT INTO {SCHEMA_NAME}.splomdata (\"group\", variable, mw, clogp, psa, hba, hbd) VALUES \
                (\'{item['group']}\', \'{item['variable']}\', {item['mw']}, {item['clogp']}, {item['psa']}, {item['hba']}, {item['hbd']})")
    db.commit()

db.close()
