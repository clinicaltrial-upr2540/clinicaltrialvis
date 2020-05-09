#!/usr/bin/env python3

import tarfile
import gzip

from subprocess import Popen
from sqlalchemy.exc import ProgrammingError


# Function to import DrugCentral
def import_drugcentral(config, engine, FORCE):
    # If the schema doesn't exist of FORCE is specified, run the import
    if FORCE or not check_for_schema(engine, "central_drug"):
        uberprint("IMPORTING CentralDrug")

        # Decompress the zip
        with gzip.open('data/drugcentral.sql.gz', 'rb') as infile:
            with open('data/drugcentral.sql', 'wb') as outfile:
                drugcentral_data = infile.read()
                outfile.write(drugcentral_data)

        with engine.connect() as conn:
            conn.execute("drop schema if exists central_drug cascade;")

        # Build command to import DrugCentral data
        command = f"/usr/local/bin/psql -h {config['drugdata']['host']} " \
            f"-d {config['drugdata']['database']} " \
            f"-p {config['drugdata']['port']} " \
            f"-U {config['drugdata']['user']} " \
            f"-f ./data/drugcentral.sql"

        # Run the command
        p = Popen(command, shell=True, env={
            'PGPASSWORD': config['drugdata']['password']
        })
        p.wait()

        # Rename the public schema and make a new one
        with engine.connect() as conn:
            conn.execute("alter schema public rename to central_drug;")
            conn.execute("create schema public;")

        uberprint("IMPORT OF CentralDrug COMPLETE")
    else:
        uberprint("SKIPPING IMPORT OF CentralDrug")
