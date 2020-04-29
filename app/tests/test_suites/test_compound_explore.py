import json
import sys
from dataclasses import dataclass
from typing import Optional, List, Any
from unittest import TestCase

import sqlalchemy
from dataclasses_json import dataclass_json
from app.basic_visuals import get_compounds_data, get_compound_data
from configparser import ConfigParser
from pathlib import Path

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

    def test_get_compound_data(self):
        engine = sqlalchemy.create_engine(DATABASE_URL)
        resp = get_compound_data('Adefovir dipivoxil',engine)
        self.assertEqual(resp[0]['compound_name'], 'Adefovir dipivoxil')
        print('test_get_compound_data PASSED with expected results')
