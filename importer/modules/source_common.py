#!/usr/bin/env python3

import requests


def uberprint(toprint):
    print("\n" + ("*" * len(toprint)) + "****")
    print(f"* {toprint} *")
    print("*" * len(toprint) + "****\n")


def check_for_schema(engine, schema):
    with engine.connect() as conn:
        result = conn.execute(f"SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = '{schema}');").fetchone()

    if list(result)[0] is True:
        return True
    else:
        return False


# Function to confirm there's data present in a table
# Returns True if data is present, False if not
def validate_table(engine, schema, table):
    with engine.connect() as conn:
        result = conn.execute(f"SELECT COUNT(*) FROM {schema}.{table};").fetchone()

    if int(list(result)[0]) > 0:
        return True
    else:
        return False


def download_http(url, filename, PATH):
    filedata = requests.get(url)

    with open(f"{PATH}/data/{filename}", 'wb') as f:
        f.write(filedata.content)
