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


# Function to import chembl data
def import_chembl(config, engine, FORCE):
    # If the schema doesn't exist of FORCE is specified, run the import
    if FORCE or not check_for_schema(engine, "chembl_26"):
        uberprint("IMPORTING ChemBL")

        # Decompress the tar
        chembl_tarfile = tarfile.open('data/chembl_26_postgresql.tar.gz')
        chembl_tarfile.extractall('data')  # specify which folder to extract to
        chembl_tarfile.close()

        # Do some database setup
        with engine.connect() as conn:
            try:
                conn.execute("CREATE ROLE \"user\" superuser;")
            except ProgrammingError:
                pass
            conn.execute("drop schema if exists chembl_26 cascade;")

        # Build command to import chmbl data
        command = f"/usr/local/bin/pg_restore " \
            f"-h {config['drugdata']['host']} " \
            f"-d {config['drugdata']['database']} " \
            f"-p {config['drugdata']['port']} " \
            f"-U {config['drugdata']['user']} " \
            f"-w -j 2 ./data/chembl_26/chembl_26_postgresql/chembl_26_postgresql.dmp"

        # Run the import
        p = Popen(command, shell=True, env={
            'PGPASSWORD': config['drugdata']['password']
        })
        p.wait()

        # Rename the public schema and make a new one
        with engine.connect() as conn:
            conn.execute("alter schema public rename to chembl_26;")
            conn.execute("create schema public;")

        uberprint("IMPORT OF ChemBL COMPLETE")
    else:
        uberprint("SKIPPING IMPORT OF ChemBL")
