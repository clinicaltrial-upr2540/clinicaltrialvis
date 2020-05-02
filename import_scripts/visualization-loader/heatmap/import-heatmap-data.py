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
db.execute("CREATE TABLE IF NOT EXISTS heatmapdata (id SERIAL PRIMARY KEY, \
                                \"group\" VARCHAR NOT NULL, \
                                variable VARCHAR NOT NULL, \
                                value REAL);")
db.commit()

# Truncate the tables we want
db.execute(f"truncate table {SCHEMA_NAME}.heatmapdata;")
db.commit()

# Open the data file
in_file = open('heatmap_data_CO6.csv')
data = csv.DictReader(in_file)

for item in data:
    # Insert a record
    db.execute(f"INSERT INTO {SCHEMA_NAME}.heatmapdata (\"group\", variable, value) VALUES (\'{item['group']}\', \'{item['variable']}\', {item['value']})")
    db.commit()

db.close()
