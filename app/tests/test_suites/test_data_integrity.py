import sys
from unittest import TestCase

import pandas as pd
import sqlalchemy
from app.app import app
import json
import pandas
import os
from pathlib import Path

from configparser import ConfigParser

p = Path(sys.path[0])

# Import database configuration
config = ConfigParser()
config.read(str(p.parent.parent) + '\\database.conf')
DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"


class TestDataIntegrity(TestCase):
    # this test case examine each view contains "drug_id" as their primary key
    def test_check_for_drug_id(self):
        with app.test_client() as c:
            resp = c.get('/data/views')
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data(as_text=True))
            for i in data['views']:
                view = c.get('/data/view/' + i)
                data_view = json.loads(view.get_data(as_text=True))
                df = pandas.DataFrame(data_view['columns'])
                nbr = df.loc[df['column_name'] == 'drug_id', 'column_name'].size
                self.assertEqual(nbr, 1)
                print('number of primary key called drug_id found in view: ' + i + ', is: ' + str(nbr))

    # a test case to ensure a database called 'drugdata' exists
    def test_check_for_db_health(self):
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(f"SELECT datname FROM pg_database")
            result = [dict(row) for row in result]
            df = pandas.DataFrame(result)
            nbr = df.loc[df['datname'] == 'drugdata', 'datname'].size
            self.assertEqual(nbr, 1)
            print('there is one database up and running called drugdata')
            conn.close()

    # This test case to
    def test_duplicate_check_compound(self):
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as conn:
            count_distinct = conn.execute(f"select count(DISTINCT drug_id) FROM curated.compound")
            count_total = conn.execute(f"select count(*) FROM curated.compound")
            count_distinct = [dict(row) for row in count_distinct]
            count_total = [dict(row) for row in count_total]
            percentage = (count_distinct[0]['count'] / count_total[0]['count']) * 100
            self.assertGreater(int(percentage), 80, percentage)
            print('the unique percentage for this in view: compound is: ' + str(percentage))
            conn.close()
