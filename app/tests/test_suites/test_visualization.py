import json
import sys
from dataclasses import dataclass
from typing import Optional, List, Any
from unittest import TestCase

import pandas

from app.app import app

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


class TestVisualization(TestCase):
    # validate the content of the splom data to ensure the CSV is returned and has content
    def test_get_visualization_data_splom_data(self):
        with app.test_client() as c:
            resp = c.get('/vis/splomdata/csv')
            self.assertEqual(resp.status_code, 200)
            self.assertGreater(resp.content_length, 0)

    # validate the content of the heat map data data to ensure the CSV is returned and has content
    def test_get_visualization_heat_map_data(self):
        with app.test_client() as c:
            resp = c.get('/vis/heatmapdata/csv')
            self.assertEqual(resp.status_code, 200)
            self.assertGreater(resp.content_length, 0)

    # validate the content of the cdc data to ensure the json is returned and has content
    # Validates at least one of the company name is 'AAIPHARMA LLC'
    def test_get_visualization_cdc_data(self):
        with app.test_client() as c:
            resp = c.get('/vis/cdcdata/json')
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data(as_text=True))
            self.assertGreater(len(data['data']), 0)
            df = pandas.DataFrame(data['data'])
            self.assertGreater(df.loc[df['company'] == 'AAIPHARMA LLC'].size, 0)
