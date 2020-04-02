#!/usr/bin/env python3

import json
import sqlalchemy

from flask import Flask, render_template, abort, jsonify
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
def render_visualizations_page():
    return render_template('visualizations.html', page_title="Visualizations")


@app.route("/visualization/<vis_id>")
def render_visualization(vis_id):

    vis_title = "Drug targets by companies"

    return render_template('visualization.html', page_title="Visualization", vis_title=vis_title)


@app.route("/report")
def render_report():
    table_list = []

    try:
        connection = engine.connect()
        q1 = 'SELECT trim(column_name) FROM information_schema.columns\r\n WHERE table_schema = \'curated\' AND table_name = \'report\''
        report = connection.execute(q1)
        for table in report:
            table_list.append(table[0])
        result = [row for row in report]
        return render_template("report.html", table=table_list)
    except Exception as e:
        return str(e)


############################################
# Routes to API endpoints go here
############################################

# API endpoint to list available tables in the curated dataset
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
    return (json.dumps(table_list, indent=4, separators=(',', ': ')))


# API endpoint to query sample data from each table in the curated dataset
@app.route("/data/tables/<table_name>", methods=['GET'])
def table_name(table_name):
    # Query tables in the 'curated' schema and serialize
    result = db.execute(f"SELECT * FROM curated.{table_name} LIMIT 100")
    table_data = [dict(row) for row in result]

    # Return as JSON object
    return(json.dumps(table_data, indent=4, separators=(',', ': ')))


# API endpoint to list available views in the curated dataset
@app.route("/data/views", methods=['GET'])
def views():
    # Query tables in the 'curated' schema and serialize
    result = db.execute(f"SELECT * FROM information_schema.views")
    views = [dict(row) for row in result]

    # Return list of views as JSON object
    return(json.dumps(views, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    app.run(debug=True)
