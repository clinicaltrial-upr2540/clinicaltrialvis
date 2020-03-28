#!/usr/bin/env python3

import json
import sqlalchemy

from flask import Flask, render_template
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
app.config['TESTING'] = True

############################################
# Startup tasks go here (load/check data)
############################################

# Connect to the database
# Set the DB URL and schema to use
# URL format: postgresql://<username>:<password>@<hostname>:<port>/<database>
DATABASE_URL = "postgresql://postgres:y9fBsh5xEeYvkUkCQ5q3@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"

# Set up and establish connection
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


############################################
# Routes to web pages go here
############################################

# Route to homepage
@app.route("/")
def render_index():
    print(db)
    return render_template('home.html', page_title="Home")


@app.route("/test")
def render_test():
    return render_template('test.html', page_title="Test Page")


@app.route("/visualizations")
def render_visualizations():
    return render_template('visualizations.html', page_title="Visualizations")


############################################
# Routes to API endpoints go here
############################################

@app.route("/data/tables")
def data_tables():
    table_list = []

    # Query tables in the 'curated' schema and serialize
    result = db.execute(f"SELECT * FROM information_schema.tables WHERE table_schema = \'curated\';")
    result = [dict(row) for row in result]

    # Loop through and pull out table names
    for table in result:
        table_list.append(table["table_name"])

    # Return table name as JSON object
    return(json.dumps(table_list, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    app.run(debug=True)
