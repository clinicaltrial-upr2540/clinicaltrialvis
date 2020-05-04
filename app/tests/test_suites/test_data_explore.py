from unittest import TestCase
from app.app import app
import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, List, Any


class TestDataExplore(TestCase):

    # validate the content of the json to ensure the number of return views are greater than 1
    # this test case makes a post case and validate the data['data'] of the response is returning rows from database
    def test_data_explore_with_download(self):
        with app.test_client() as c:
            # create a sample request
            request = PayloadRequest()
            request.export = "true"
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
            self.assertGreater(len(resp.get_data()), 0)

        # validate the content of the json to ensure the number of return views are greater than 1
        # this test case makes a post case and validate the data['data'] of the response is returning rows from database

    def test_data_explore_with_single_file(self):
        with app.test_client() as c:
            # create a sample request
            request = PayloadRequest()
            request.export = "true"
            request.single_file = "true"
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
            self.assertGreater(len(resp.get_data()), 0)
            self.assertEqual(resp.content_type, 'application/x-zip-compressed')

    def test_data_explore_with_filters(self):
        with app.test_client() as c:
            # create a sample request
            request = PayloadRequest()
            request.export = "false"
            request.single_file = "true"
            request.join_style = "inner"
            request.single_file = "false"
            request.limit = 25
            datalist = DataList()
            datalist.view_name = "compounds"
            datalist.column_list = ["atc_level_4"]
            filter_object = Filter()
            filter_object.column_name = "atc_level_4"
            filter_object.operator = "matches"
            filter_object.target = "RESPIRATORY SYSTEM"
            datalist.filters = [filter_object]
            request.data_list = [datalist]
            resp = c.post('/data/explore', data=request.to_json(), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertGreater(len(resp.get_data()), 0)

    def test_data_explore_filters_and_export(self):
        with app.test_client() as c:
            # create a sample request
            request = PayloadRequest()
            request.export = "true"
            request.single_file = "true"
            request.join_style = "inner"
            request.limit = 25
            datalist = DataList()
            datalist.view_name = "compounds"
            datalist.column_list = ["atc_level_4"]
            filter_object = Filter()
            filter_object.column_name = "atc_level_4"
            filter_object.operator = "matches"
            filter_object.target = "RESPIRATORY SYSTEM"
            datalist.filters = [filter_object]
            request.data_list = [datalist]
            resp = c.post('/data/explore', data=request.to_json(), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertGreater(len(resp.get_data()), 0)

    # validate the content of the json to ensure the number of return views are greater than 1
    # this test case makes a post case and validate the data['data'] of the response is returning rows from database
    def test_data_explore_get(self):
        with app.test_client() as c:
            resp = c.get('/data/explore')
            self.assertEqual(resp.status_code, 200)
            self.assertGreater(len(resp.get_data()), 0)


@dataclass_json
@dataclass
class DataList:
    view_name: Optional[str] = None
    column_list: Optional[List[str]] = None
    filters: Optional[List[Any]] = None


@dataclass_json
@dataclass
class Filter:
    column_name: Optional[str] = None
    operator: Optional[str] = None
    target: Optional[str] = None


@dataclass_json
@dataclass
class PayloadRequest:
    export: Optional[bool] = None
    single_file: Optional[bool] = None
    data_list: Optional[DataList] = None
    join_style: Optional[str] = None
    limit: Optional[int] = None
