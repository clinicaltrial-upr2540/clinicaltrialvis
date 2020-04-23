#!/usr/bin/env python3

# Script to demonstrate some SQLAlchemy examples

import sqlalchemy
import json

from sqlalchemy.orm import scoped_session, sessionmaker

# Set the DB URL and schema to use
# URL format: postgresql://<username>:<password>@<hostname>:<port>/<database>
DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"
SCHEMA_NAME = "example_schema"

# Set up and establish connection
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# Example of running raw queries
# Create a schema
db.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")

# Use the schema as a search path
db.execute(f"set search_path to {SCHEMA_NAME};")

# Create a table
db.execute("CREATE TABLE IF NOT EXISTS example_table (id SERIAL PRIMARY KEY, \
                                    name VARCHAR NOT NULL, \
                                    age BIGINT, \
                                    location VARCHAR);")

# Insert some data
db.execute("INSERT INTO example_table (name, age, location) VALUES (:name, :age, :location)", {"name": "jack", "age": 15, "location": "boston"})
db.execute("INSERT INTO example_table (name, age, location) VALUES (:name, :age, :location)", {"name": "lucille", "age": 84, "location": "louisiana"})
db.execute("INSERT INTO example_table (name, age, location) VALUES (:name, :age, :location)", {"name": "xi", "age": 53, "location": "peru"})

# Commit the changes - basically everything up to here is a script that we are now executing
db.commit()

# Select some stuff from the table
# 	fetchone() will return the first matchingrecord
# 	fetchall() gets all the matching records
records = db.execute("SELECT * FROM example_table").fetchall()

# Serialize as a nice dictionary
result = [dict(row) for row in records]

# Convert to JSON and pretty-print
print(json.dumps(result, indent=4, separators=(',', ': ')))

# Clean up the temp table and schema we created
db.execute("DROP TABLE IF EXISTS example_table;")
db.execute(f"DROP SCHEMA IF EXISTS {SCHEMA_NAME};")
db.commit()
