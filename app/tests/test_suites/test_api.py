from unittest import TestCase
from app.app import app
import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, List, Any


class TestAPI(TestCase):
    # validate the content of the json to ensure the number of return views are greater than 1
    def test_data_views(self):
        with app.test_client() as c:
            resp = c.get('/data/views')
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data(as_text=True))
            self.assertGreater(len(data['views']), 0)

    # this test case makes a post case and validate the data['data'] of the response is returning rows from database
    def test_data_explore(self):
        with app.test_client() as c:
            # create a sample request
            request = PayloadRequest()
            request.export = "false"
            request.join_style = "inner"
            request.single_file = "false"
            request.limit = 25
            datalist = DataList()
            datalist.view_name = "compounds"
            datalist.column_list = ["drug_id"]
            datalist.filters = []
            request.data_list = [datalist]
            resp = c.post('/data/explore', data=request.to_json(), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.get_data(as_text=True))
            self.assertGreater(len(data['data']), 0)


@dataclass_json
@dataclass
class DataList:
    view_name: Optional[str] = None
    column_list: Optional[List[str]] = None
    filters: Optional[List[Any]] = None


@dataclass_json
@dataclass
class PayloadRequest:
    export: Optional[bool] = None
    single_file: Optional[bool] = None
    data_list: Optional[DataList] = None
    join_style: Optional[str] = None
    limit: Optional[int] = None
