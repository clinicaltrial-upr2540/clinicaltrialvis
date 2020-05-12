#!/usr/bin/env python3

import os
import json
import sqlalchemy
import datetime
import zipfile
import random
import sys

from flask import Flask, render_template, request, make_response, send_file
from sqlalchemy.sql import text
from configparser import ConfigParser
from io import BytesIO

############################################
# Import local modules
############################################
APP_PATH = str(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(APP_PATH)

from explore_compounds import get_plot_png_test, get_plot_png, get_descriptor_payload, get_similar_dict, get_ba_dict
import visualization_setup

app = Flask(__name__)
app.config['TESTING'] = True

############################################
# Startup tasks go here (load/check config)
############################################

# Import database configuration from file
config = ConfigParser()
config.read(f"{APP_PATH}/database.conf")

# If environment variables are present, override config file
if "drugdata" not in config:
    config["drugdata"] = {}
if "DB_USER" in os.environ:
    config["drugdata"]["user"] = os.environ.get("DB_USER")
if "DB_PASSWORD" in os.environ:
    config["drugdata"]["password"] = os.environ.get("DB_PASSWORD")
if "DB_HOST" in os.environ:
    config["drugdata"]["host"] = os.environ.get("DB_HOST")
if "DB_PORT" in os.environ:
    config["drugdata"]["port"] = os.environ.get("DB_PORT")
if "DB_NAME" in os.environ:
    config["drugdata"]["database"] = os.environ.get("DB_NAME")

# Set up and establish database engine
# URL format: postgresql://<username>:<password>@<hostname>:<port>/<database>
DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"
engine = sqlalchemy.create_engine(DATABASE_URL)

# Refresh visualization data
try:
    visualization_setup.import_visualization_demos(engine)
except Exception:
    print("WARNING: Unable to refresh visualization data.")


############################################
# Routes to web pages go here
############################################

# Route to homepage
@app.route("/")
def render_index():
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

    return render_template('visualizations.html', page_title="Demo Visualizations", result_list=result_list)


# Unified visualization to explore drug companies
@app.route("/classes")
def render_drug_classes():
    return render_template('drug_classes.html', page_title="Explore Targets By Company", result={})


# Page to show a single d3 visualization
@app.route("/visualization/<vis_id>")
def render_visualization(vis_id):
    # Query for full list of visualizations
    with engine.connect() as conn:
        result = conn.execute(f"SELECT * FROM application.visualizations WHERE id = {vis_id};").fetchone()
    result = dict(result)

    return render_template('visualization.html', page_title="Visualization", result=result)


# Page to explore and explort data
@app.route("/explore/data")
def render_explorer():
    return render_template('explore.html', page_title="Explore Data")


# Page to look up a compound vs its therapeutic group's descriptors
@app.route("/explore/compound", methods=["GET", "POST"])
def render_compound_explorer():
    if request.method == "POST":
        compound_name = request.form.get("compound_name", '')
        if compound_name == '':
            compound_name = None

        # Build the response using the API functions
        descriptor_payload = get_descriptor_payload(compound_name)
        descriptor_data = data_explore_post(descriptor_payload)
        descriptor_dict = get_descriptor_dict(descriptor_data)
        if descriptor_dict is None:
            return render_template('explore_compound.html',
                                   no_compound="True",
                                   compound_name=compound_name,
                                   page_title="Explore A Compound"
                                   )
        else:
            warning_list = []

            try:
                descriptor_dict['molecular_weight'] = round(float(descriptor_dict['molecular_weight']), 3)
            except ValueError:
                pass
            ba_dict = get_ba_dict(engine, compound_name)
            similar_dict = get_similar_dict(engine, compound_name, descriptor_dict)

            if len(ba_dict) < 1:
                ba_dict = None
                warning_list.append("Bioavailability information not available.")

            if (similar_dict.get('molecular_weight') == []):
                similar_dict = None
                warning_list.append("Similar compound information not available.")

            return render_template('explore_compound.html',
                                   compound_name=descriptor_dict["compound_name"],
                                   warning_list=warning_list,
                                   descriptor_dict=descriptor_dict,
                                   ba_dict=ba_dict,
                                   similar_dict=similar_dict,
                                   page_title="Explore A Compound"
                                   )
    else:
        return render_template('explore_compound.html', page_title="Explore A Compound")


############################################
# Routes to API endpoints go here
############################################

# API endpoint to get a 9 descriptor plot for a compound
# Returns a PNG image to be embedded
@app.route("/compound/explore/<compound_name>/descriptors/png", methods=["GET"])
def compound_descriptors(compound_name):
    return get_plot_png(compound_name, engine)


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


# API endpoint to list the columns in a single view
@app.route("/data/view/<view_name>", methods=['GET'])
def view_info(view_name):
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


# API endpoint for querying data from one or more views in the curated dataset
# Supports returning results as a JSON object, as a single CSV, or as a zip file
#   containing one CSV for each view
@app.route("/data/explore", methods=['GET', 'POST'])
def explore_data():
    # If method is POST, this is a real API request
    if request.method == 'POST':
        payload = request.get_json()
        return data_explore_post(payload)
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

def get_descriptor_dict(descriptor_data):
    descriptor_data = json.loads(descriptor_data)
    data_obj = descriptor_data.get("data", {})

    view_column_names = data_obj.get("view_column_names", [])
    column_names = [item[1] for item in view_column_names]
    if len(data_obj.get("data", [])) > 0:
        data = data_obj.get("data", [])[0]

        return dict(zip(column_names, data))
    else:
        return None


def data_explore_post(payload):
    if validate_explore_request(payload) is False:
        return

    # If "export" is false, return a JSON object to build a preview table
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
        # Loop through views to run multiple retrievals of the data using the same FROM, WHERE and LIMIT snippets
        csv_data_dict = {}
        memory_file = BytesIO()
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y.%m.%d-%H.%M.%S")

        for view in payload["data_list"]:
            where_snippet = get_where_snippet(payload)
            from_snippet = get_from_snippet(payload)
            select_snippet = get_single_view_select_snippet(view)
            limit_snippet = get_limit_snippet(payload)

            sql_string = select_snippet + from_snippet + where_snippet + limit_snippet
            csv_data_dict[view["view_name"]] = get_explore_response_as_csv(sql_string, payload)

        # Add all views to an in-memory zip file and return
        with zipfile.ZipFile(memory_file, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for viewname, csvdata in csv_data_dict.items():
                file_name = str(viewname) + '-' + dt_string + '.csv'
                zf.writestr(file_name, csvdata)
        memory_file.seek(0)

        zip_name = f"export-{dt_string}.zip"
        return send_file(memory_file, attachment_filename=zip_name, as_attachment=True)


# Check if there is a valid APi request
# TODO: Replace this with a real 404 page
def validate_explore_request(payload):
    if payload is None:
        return "404 error needed"
    else:
        return True


# Function to build the "FROM" portion of a query, with join
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
        result = " SELECT DISTINCT  "
    else:
        result = " SELECT  "

    for item in payload.get("data_list"):
        view_name = item.get("view_name")
        column_list = item.get("column_list")
        for column_name in column_list:
            result += f'"{view_name}"."{column_name}", '
            counter += 1

    return result[0:len(result) - 2]
    # return " SELECT drug_id, compound_name, smiles, clogp "


# Function to return SELECT part of query for a multi-file download
# Only select fields from one view at a time
def get_single_view_select_snippet(view_data):
    counter = 1
    result = " SELECT DISTINCT "

    view_name = view_data.get("view_name")
    column_list = view_data.get("column_list")
    for column_name in column_list:
        result += f'"{view_name}"."{column_name}", '
        counter += 1

    return result[0:len(result) - 2]


# Function to build the "WHERE" portion of the query, with all fields
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
                operator = "ILIKE"
            target = filter_obj.get("target")

            if operator == "=" or operator == "!=":
                this_snip = f' {condition_term} "{view_name}"."{column_name}" {operator} \'{target}\' '
            else:
                this_snip = f' {condition_term} "{view_name}"."{column_name}" {operator} \'%{target}%\' '

            result += this_snip
            condition_term = " AND "

    return result


# Function to define the "LIMIT" portion of a query
def get_limit_snippet(payload):
    if payload.get("export") == "true":
        return ""
    limit = payload.get("limit", 10)
    return f" LIMIT {limit} "


# Query the database and serialize results as a Python dict
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


# Query the database and serialize the results as a CSV
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
    result = ','.join(view_column_names) + '\n' + result

    return(result)


# Convert a single datum to a clean format for the CSV
def clean_csv_value(value):
    if value is None or value == "null":
        return("")
    elif isinstance(value, str):
        return('"' + value.replace('"', '""') + '"')
    else:
        return(str(value))


# Convert a single datum to a clean format for a JSON API response
def clean_json_value(value):
    if value is None or value == "null":
        return("")
    else:
        return(value)


# Get the list of views included in an API request
def get_view_names_from_payload(payload):
    view_names = []

    for item in payload.get("data_list"):
        view_name = item.get("view_name")
        view_names.append(view_name)
    return view_names


# Get the list of columns included in an API request
# Returns a list of tuples (view, column)
def get_view_column_names_from_payload(payload):
    view_column_names = []

    for item in payload.get("data_list"):
        view_name = item.get("view_name")
        column_list = item.get("column_list")
        for column_name in column_list:
            view_column_names.append([view_name, column_name])
    return view_column_names


# Get the list of columns included in an API request
# This is run against individual views, so it returns only a list of columns
def get_column_names_from_payload(payload):
    column_names = []

    for item in payload.get("data_list"):
        column_list = item.get("column_list")
        for column_name in column_list:
            column_names.append(column_name)
    return column_names


# Function to serialize a SQL response as a Python list
def get_data_list_obj_from_data(data):
    return [list(map(clean_json_value, list(row))) for row in data]


# Necessary to run app if app.py is executed as a script
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
