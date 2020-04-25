from unittest import TestCase
from app.app import app
import json
import pandas


class TestDataIntegrity(TestCase):

    # this test case examine each view contains "drug_id" as their primary key
    def test_data_integrity(self):
        with app.test_client() as c:
            resp = c.get('/data/views')
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data(as_text=True))
            for i in data['views']:
                view = c.get('/data/view/'+i)
                data_view = json.loads(view.get_data(as_text=True))
                df = pandas.DataFrame(data_view['columns'])
                nbr = df.loc[df['column_name'] == 'drug_id', 'column_name'].size
                self.assertEqual(nbr, 1)
                print('number of primary key called drug_id found in view: ' + i + ', is: ' + str(nbr))
