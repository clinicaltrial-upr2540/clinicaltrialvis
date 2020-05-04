import sys
from configparser import ConfigParser
from pathlib import Path
from unittest import TestCase

import pandas as pd

from app.app import app

p = Path(sys.path[0])

# Import database configuration
config = ConfigParser()
config.read(str(p.parent.parent) + '\\database.conf')
DATABASE_URL = f"postgresql://{config['drugdata']['user']}:{config['drugdata']['password']}@{config['drugdata']['host']}:{config['drugdata']['port']}/{config['drugdata']['database']} "


class TestVisualization(TestCase):
    # validate the content of the splom data to ensure the CSV is returned and has content
    def test_vis_splom_data_structure(self):
        filename = str(p.parent.parent) + '\\static\\visualizations\datafiles\splom_data_C14.csv'
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        column_names = ['group', 'variable', 'mw', 'clogp', 'psa', 'hba', 'hbd']
        df_ = pd.DataFrame(columns=column_names)
        result = data.columns.intersection(df_.columns)
        self.assertEqual(result.size, 7)

    def test_vis_splom_data_range(self):
        filename = str(p.parent.parent) + '\\static\\visualizations\datafiles\splom_data_C14.csv'
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        self.assertFalse(any(data['mw'] < 0))
        self.assertFalse(any(data['psa'] < 0))
        self.assertFalse(any(data['hba'] < 0))
        self.assertFalse(any(data['hbd'] < 0))

    # validate the content of the heat map data data to ensure the CSV is returned and has content
    def test_get_vis_heat_map_data_range(self):
        filename = str(p.parent.parent) + '\\static\\visualizations\\datafiles\\heatmap_data_CO6.csv'
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        self.assertFalse(any(data['value'] < 0))

        # validate the content of the heat map data data to ensure the CSV is returned and has content

    def test_get_vis_heat_map_data_structure(self):
        filename = str(p.parent.parent) + '\\static\\visualizations\\datafiles\\heatmap_data_CO6.csv'
        data = pd.read_csv(filename, header=0, error_bad_lines=False, sep=',')
        column_names = ['group', 'variable', 'value']
        df_ = pd.DataFrame(columns=column_names)
        result = data.columns.intersection(df_.columns)
        self.assertEqual(result.size, 3)

    # validate the content of the cdc data to ensure the json is returned and has content
    # Validates at least one of the company name is 'AAIPHARMA LLC'
    def test_get_vis_cdc_data(self):
        filename = str(p.parent.parent) + '\\static\\visualizations\\datafiles\\cdc_data.json'
        data = pd.read_json(filename)
        self.assertGreater(len(data['data']), 0)

    # validate the content of the cdc data to ensure the json is returned and has content
    # Validates at least one of the company name is 'AAIPHARMA LLC'
    def test_render_visualization_id(self):
        with app.test_client() as c:
            resp = c.get('/visualization/1')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.mimetype, 'text/html')
