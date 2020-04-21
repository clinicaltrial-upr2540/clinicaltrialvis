#!/usr/bin/env python3

import json
import sqlalchemy
import pathlib
import datetime

from flask import Flask, render_template, request, make_response
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from configparser import ConfigParser

import random

app = Flask(__name__)
app.config['TESTING'] = True

############################################
# Startup tasks go here (load/check data)
############################################

# Connect to the database
# Set the DB URL and schema to use
# URL format: postgresql://<username>:<password>@<hostname>:<port>/<database>
DATABASE_URL = "postgresql://app_user:flask_app_user_role@drugdata.cgi8bzi5jc1o.us-east-1.rds.amazonaws.com:5432/drugdata"

# Set up and establish connection
engine = sqlalchemy.create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# What does this config do? Let's eliminate it if possible
config = ConfigParser()
config.readfp(open(f"{pathlib.Path(__file__).parent.absolute()}/config/configuration.conf"))


############################################
# Routes to web pages go here
############################################

# Route to homepage
@app.route("/")
def render_index():
    print(db)
    return render_template('home.html', page_title="Home")


# Route to API doc page
@app.route("/api")
def render_api_doc():
    return render_template('api.html', page_title="API Documentation")


# Menu to present all visualizations
@app.route("/visualizations")
def render_visualizations_page():
    # Query for full list of visualizations
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM application.visualizations;").fetchall()
    result_list = [dict(row) for row in result]

    return render_template('visualizations.html', page_title="Visualizations", result_list=result_list)


# Page to show a single d3 visualization
@app.route("/visualization/<vis_id>")
def render_visualization(vis_id):
    # Query for full list of visualizations
    with engine.connect() as conn:
        result = conn.execute(f"SELECT * FROM application.visualizations WHERE id = {vis_id};").fetchone()
    result = dict(result)

    return render_template('visualization.html', page_title="Visualization", result=result)


# Page to explore and explort data
@app.route("/explore")
def render_explorer():
    return render_template('explore.html', page_title="Explore")


############################################
# Routes to visualization data
############################################
@app.route("/vis/<vis_data_name>/<data_format>")
def get_visualization_data(vis_data_name, data_format):
    with engine.connect() as conn:
        query_result = conn.execute(f"SELECT * FROM application.{vis_data_name}").fetchall()
    query_result = [dict(row) for row in query_result]

    popped_result = []

    # We don't want to include IDs
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
# Routes to API endpoints go here
############################################

# API endpoint to list available views in the curated dataset
@app.route("/data/views", methods=['GET'])
def views():
    # Query tables in the 'curated' schema and serialize
    with engine.connect() as conn:
        result = conn.execute("""
            SELECT table_name
            FROM information_schema.views
            WHERE table_schema like 'curated';
        """)
    views = [dict(row).get("table_name") for row in result]
    response = {"views": views}
    # Return list of views as JSON object
    return (json.dumps(response, indent=4, separators=(',', ': ')))


@app.route("/data/view/<view_name>", methods=['GET'])
def view_info(view_name):
    from test_responses import sample_view_info

    with engine.connect() as conn:
        result = conn.execute(f"SELECT column_name, data_type \
            FROM information_schema.columns \
            WHERE table_name LIKE '{view_name}' \
            and table_schema like 'curated' \
            order by 1;")

    columns = [dict(row) for row in result]
    view_name = view_name

    return_data = {"view_name": view_name, "columns": columns}

    return (json.dumps(return_data, indent=4))


@app.route("/data/explore", methods=['GET', 'POST'])
def explore_data():
    # if method is POST
    if request.method == 'POST':
        payload = request.get_json()
        if validate_explore_request(payload) is False:
            return

        if payload.get("export") == "false":
            where_snippet = get_where_snippet(payload)
            from_snippet = get_from_snippet(payload)
            select_snippet = get_select_snippet(payload, False)
            limit_snippet = get_limit_snippet(payload)

            sql_string = select_snippet + from_snippet + where_snippet + limit_snippet
            results = get_explore_response(sql_string, payload)

            results["sql"] = sql_string
            return json.dumps(results, indent=4)

        elif payload.get("export") == "true":
            # IF this is a single file download, the data is exactly the same as render, just need to turn it into a file
            if payload.get("single_file") == "true":
                where_snippet = get_where_snippet(payload)
                from_snippet = get_from_snippet(payload)
                select_snippet = get_select_snippet(payload, True)
                limit_snippet = get_limit_snippet(payload)

                sql_string = select_snippet + from_snippet + where_snippet + limit_snippet
                results = get_explore_response_as_csv(sql_string, payload)

                # results["sql"] = sql_string

                # Create a response object and set headers so it will download as file
                response = make_response(results)
                response.headers['Content-Type'] = "application/octet-stream"
                response.headers['Content-Disposition'] = "attachment; filename=\"export.csv\""

                print("SEND DAT FILE")
                return(response)

            # ELSE we need to run multiple retrievals of the data using the same FROM and WHERE and LIMIT snippets
            # the only thing that is different is the SELECT statement
            else:
                pass

            # with each view, a JSON is constructed
            # from that JSON, a file is made and added to a zip file
            # once all views have been iterated thru, return the zip file

    # if the method is GET, then retrieve one of several sample responses.
    # useful for development and testing of frontend
    if request.method == 'GET':
        from test_responses import list_of_responses

        if request.args.get("download") == "true":
            return (json.dumps(list_of_responses[0], indent=4))
        else:
            return (json.dumps(random.choice(list_of_responses[1:4]), indent=4))


############################################
# Utility Functions
############################################

def validate_explore_request(payload):
    if payload is None:
        return "404 error needed"
    else:
        return True


def get_from_snippet(payload):
    join_options = {"inner": "INNER", "left": "LEFT OUTER"}
    join_term = join_options.get(payload.get("join_style"), "INNER")
    counter = 1
    result = ""
    for item in payload.get("data_list"):
        view_name = item.get("view_name")
        this_snip = ""
        if counter == 1:
            this_snip = f' FROM curated."{view_name}"'
        else:
            this_snip = f' {join_term} JOIN curated."{view_name}" using (drug_id)'
        counter += 1
        result += this_snip
    return result


# if not download, do not use DISTINCT
# if download, add distinct
# if multi file download, this will be run multiple times each time with columns from one view
def get_select_snippet(payload, download):
    counter = 1
    if download:
        result = " SELECT DISTINCT "
    else:
        result = " SELECT "

    for item in payload.get("data_list"):
        view_name = item.get("view_name")
        column_list = item.get("column_list")
        for column_name in column_list:
            result += f'"{view_name}"."{column_name}", '
            counter += 1

    return result[0:len(result) - 2]
    # return " SELECT drug_id, compound_name, smiles, clogp "


def get_where_snippet(payload):
    result = " "
    condition_term = " WHERE "
    for item in payload.get("data_list"):
        view_name = item.get("view_name")
        filter_list = item.get("filters", [])
        for filter_obj in filter_list:
            column_name = filter_obj.get("column_name")
            operator = filter_obj.get("operator")
            if operator not in ["matches", ">", "<", "=", "!="]:
                operator = "="
            if operator == "matches":
                operator = "LIKE"
            target = filter_obj.get("target")

            this_snip = f' {condition_term} "{view_name}"."{column_name}" {operator} \'%{target}%\' '
            result += this_snip
            condition_term = " AND "

    return result


def get_limit_snippet(payload):
    if payload.get("export") == "true":
        return ""
    limit = payload.get("limit", 10)
    return f" LIMIT {limit} "


def get_explore_response(sql_string, payload):
    cmd = text(sql_string)
    data = None
    with engine.connect() as conn:
        data = conn.execute(cmd)
    results = {
        "download": False,
        "files_to_prepare": 0,
        "data": [],
    }

    data_list_obj = {
        "view_names": get_view_names_from_payload(payload),
        "view_column_names": get_view_column_names_from_payload(payload),
        "data": get_data_list_obj_from_data(data),
    }

    results["data"] = data_list_obj

    return results


def get_explore_response_as_csv(sql_string, payload):
    cmd = text(sql_string)
    data = None
    print(str(datetime.datetime.now()) + " QUERYING DATABASE")
    with engine.connect() as conn:
        data = conn.execute(cmd)

    print(str(datetime.datetime.now()) + " EXTRACTING COLUMN HEADERS")
    # Get column names for first row in the CSV
    view_column_names = get_column_names_from_payload(payload)

    print(str(datetime.datetime.now()) + " SERIALIZING DATA")
    # Serialize as a CSV
    result = [','.join(map(clean_csv_value, list(row))) for row in data]
    result = '\n'.join(result)

    print(str(datetime.datetime.now()) + " PREPENDING COLUMN HEADERS")
    # Prepend column headings
    print(view_column_names)
    result = ','.join(view_column_names) + '\n' + result

    return(result)


def clean_csv_value(value):
    if isinstance(value, str):
        return('"' + value.replace('"', '""') + '"')
    else:
        return(str(value))


def get_view_names_from_payload(payload):
    view_names = []

    for item in payload.get("data_list"):
        view_name = item.get("view_name")
        view_names.append(view_name)
    return view_names


def get_view_column_names_from_payload(payload):
    view_column_names = []

    for item in payload.get("data_list"):
        view_name = item.get("view_name")
        column_list = item.get("column_list")
        for column_name in column_list:
            view_column_names.append([view_name, column_name])
    return view_column_names


def get_column_names_from_payload(payload):
    column_names = []

    for item in payload.get("data_list"):
        column_list = item.get("column_list")
        for column_name in column_list:
            column_names.append(column_name)
    return column_names


def get_data_list_obj_from_data(data):
    return [list(row) for row in data]


if __name__ == "__main__":
    app.run(debug=True)
