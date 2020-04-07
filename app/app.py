#!/usr/bin/env python3

import csv
import json
import os
import sys
from configparser import ConfigParser

import pandas
import sqlalchemy

from flask import Flask, render_template, abort, jsonify, send_from_directory, current_app, request
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

config = ConfigParser()
config.readfp(open(os.path.join(os.path.dirname(sys.path[0]), 'app\\config') + '\\' + 'configuration.conf'))


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
    # Query for full list of visualizations
    result = db.execute("SELECT * FROM application.visualizations;").fetchall()
    result = [dict(row) for row in result]

    return render_template('visualizations.html', page_title="Visualizations", result=result)


@app.route("/visualization/<vis_id>")
def render_visualization(vis_id):
    # Query for full list of visualizations
    result = db.execute(f"SELECT * FROM application.visualizations WHERE id = {vis_id};").fetchone()
    result = dict(result)

    return render_template('visualization.html', page_title="Visualization", result=result)


############################################
# Routes to visualization data go here
############################################
@app.route("/vis/<vis_data_name>/<data_format>")
def get_visualization_data(vis_data_name, data_format):
    query_result = db.execute(f"SELECT * FROM application.{vis_data_name}").fetchall()
    query_result = [dict(row) for row in query_result]

    popped_result = []

    # We don't want to IDs
    for item in query_result:
        item.pop("id")
        popped_result.append(item)

    # Return as a json file
    if data_format == "json":
        # Store values in a var to pass to js
        data = {}
        data["data"] = popped_result

        return(json.dumps(data))
    # Return as a CSV
    else:
        csv_output = ",".join(popped_result[0].keys())

        for row in popped_result:
            csv_output = csv_output + "\n" + ",".join(map(str, row.values()))

        return(csv_output)


############################################
# Routes to Reports
############################################

@app.route("/report/create", methods=['GET', 'POST'])
def create_custom_report():
    selected_views = ""
    try:
        view_list = get_all_view_names()
        if request.method == 'POST':
            view_names = request.form.to_dict()
            view_list = update_view_list(view_list, view_names)
            col_list = get_col_list(view_list)
            return render_template("custom_report.html", view_list=view_list, col_list=col_list)
        else:
            col_list = get_init_list(view_list)
            return render_template("custom_report.html", view_list=view_list, col_list=col_list)
    except Exception as e:
        return str(e)


@app.route("/report", methods=['GET', 'POST'])
def render_report():
    table_list = []
    test_string = ""
    try:
        if request.method == 'POST':
            table_list = request.form.getlist('checks[]')
            test_string = ','.join(map(str, table_list))
            connection = engine.connect()
            q1 = 'select drug_name, ' + test_string + ' from curated.m_report'
            result = connection.execute(q1)
            result = [dict(row) for row in result]
            df = pandas.DataFrame(result)
            df.to_csv("./file.csv", sep=',', index=False)
            uploads = os.path.join(current_app.root_path)
            return send_from_directory(directory=uploads, filename="file.csv", as_attachment=True)
        else:
            connection = engine.connect()
            q1 = 'SELECT trim(column_name) FROM information_schema.columns\r\n WHERE table_schema = \'curated\' AND table_name = \'report\''
            report = connection.execute(q1)
            for table in report:
                table_list.append(table[0])
            result = [row for row in report]
            connection.close()
            return render_template("report.html", table=table_list)
    except Exception as e:
        return str(e)


@app.route("/export", methods=['GET', 'POST'])
def export():
    export_list = request.form.getlist('ck[]')
    col_list = []
    view_list = []

    for item in export_list:
        x = item.split(":")
        col_list.append(
            'CAST("' + x[1].strip() + '"."' + x[0].strip() + '" AS VARCHAR(100)) AS "' + x[1].strip() + '_' + x[0].strip() + '"')
        view_list.append(x[1].strip())

    if len(view_list) > len(set(view_list)):
        join_condition = 'FROM "curated"' + '."' + view_list[0] + '"'
    else:
        join_condition = config.get('sql_config', 'join_condition')

    parameters = ','.join(map(str, col_list))
    query = 'select distinct ' + parameters + ' ' + join_condition

    uploads = generate_report(query)

    return send_from_directory(directory=uploads, filename="file.csv", as_attachment=True)


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
    return (json.dumps(table_data, indent=4, separators=(',', ': ')))


# API endpoint to list available views in the curated dataset
@app.route("/data/views", methods=['GET'])
def views():
    # Query tables in the 'curated' schema and serialize
    result = db.execute(f"SELECT * FROM information_schema.views")
    views = [dict(row) for row in result]

    # Return list of views as JSON object
    return (json.dumps(views, indent=4, separators=(',', ': ')))


############################################
# Utility Functions
############################################

def get_all_view_names():
    view_list = []
    connection = engine.connect()
    q1 = 'select trim(matviewname) as view_name, \'checked\' as selected_view from pg_matviews where schemaname = \'curated\' AND trim(matviewname) <> \'m_report\' '
    report = connection.execute(q1)
    report = [dict(row) for row in report]
    connection.close()
    return report


def update_view_list(view_list, view_names):
    view_list_df = pandas.DataFrame(view_list)
    view_names_df = pandas.DataFrame(view_names.keys(), columns=['view_name'])
    view_list_df.loc[(~view_list_df['view_name'].isin(view_names_df['view_name'])), 'selected_view'] = ''
    return view_list_df.to_dict(orient='records')


def get_col_list(view_names):
    view_list = []
    for table in view_names:
        if table['selected_view'] == 'checked':
            view_list.append('"' + table['view_name'] + '"')

    selected_columns = ','.join(map(str, view_list))
    q1 = 'SELECT view_name, col_name from application.get_view_attributes(' + "'{" + selected_columns + '}' + "'" + ');'
    connection = engine.connect()
    report = connection.execute(q1)
    report = [dict(row) for row in report]

    connection.close()
    return report


def get_init_list(view_names):
    view_list = []
    for table in view_names:
        view_list.append('"' + table['view_name'] + '"')
    selected_views = ','.join(map(str, view_list))
    q1 = 'SELECT view_name, col_name from application.get_view_attributes(' + "'{" + selected_views + '}' + "'" + ');'
    connection = engine.connect()
    report = connection.execute(q1)
    report = [dict(row) for row in report]
    connection.close()
    return report


def generate_report(query):
    connection = engine.connect()
    result = connection.execute(query)
    result = [dict(row) for row in result]
    df = pandas.DataFrame(result)
    df.to_csv("./file.csv", sep=',', index=False)
    uploads = os.path.join(current_app.root_path)
    return uploads


if __name__ == "__main__":
    app.run(debug=True)
