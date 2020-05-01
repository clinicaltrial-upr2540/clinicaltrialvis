import json
import sys
import time
from configparser import ConfigParser
from pathlib import Path
from unittest import TestCase
import requests

import sqlalchemy

from app.app import app
from app.explore_compounds import get_compounds_data, get_compound_data, get_descriptor_payload, get_ba_dict

p = Path(sys.path[0])

# Import database configuration
config = ConfigParser()
config.read(str(p.parent.parent) + '\\database.conf')
DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']}"


class TestCompoundExplore(TestCase):
    # validate the content of the json to ensure the number of return views are greater than 1
    def test_get_compounds_data(self):
        engine = sqlalchemy.create_engine(DATABASE_URL)
        resp = get_compounds_data(engine)
        self.assertGreater(len(resp), 0)
        print('test_compound_get_compounds_data PASSED with results')

    def test_get_descriptor_payload(self):
        resp = get_descriptor_payload('Amikacin')
        self.assertEqual(resp['data_list'][0]['filters'][0]['target'], 'Amikacin')

    def test_get_compound_data(self):
        engine = sqlalchemy.create_engine(DATABASE_URL)
        resp = get_compound_data('Adefovir dipivoxil', engine)
        self.assertEqual(resp[0]['compound_name'], 'Adefovir dipivoxil')
        print('test_get_compound_data PASSED with expected results')

    def test_render_compound_explorer(self):
        with app.test_client() as c:
            req = requests.Request
            req.data = '{"compound_name": "Atorvastatin"}'
            resp = c.get('/compound/explore')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.default_mimetype, 'text/html')

    def test_explore_data(self):
        with app.test_client() as c:
            req = requests.Request
            req.data = '{"compound_name": "Atorvastatin"}'
            resp = c.get('/data/explore')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.default_mimetype, 'text/html')

    def test_compound_descriptors(self):
        with app.test_client() as c:
            resp = c.get('compound/explore/Amikacin/descriptors/png')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, 'image/png')

    def test_get_ba_dict(self):
        engine = sqlalchemy.create_engine(DATABASE_URL)
        resp = get_ba_dict(engine, 'Amikacin')
        self.assertGreater(len(resp[0]), 0)
        print('test_test_get_ba_dict PASSED with results')