from unittest import TestCase
from app.app import app


class TestPages(TestCase):
    # this test case hits the homepage of the application and checks that the home page is up and running
    def test_home_page(self):
        with app.test_client() as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 200)

    # this test case hits the explore of the application and checks that the explore page is up and running
    def test_explore_page(self):
        with app.test_client() as c:
            resp = c.get('/explore')
            self.assertEqual(resp.status_code, 200)

    # this test case hits the visualizations of the application and checks that the visualizations page is up and
    # running
    def test_visualizations_page(self):
        with app.test_client() as c:
            resp = c.get('/visualizations')
            self.assertEqual(resp.status_code, 200)

    # this test case hits the api of the application and checks that the api page is up and running
    def test_api_page(self):
        with app.test_client() as c:
            resp = c.get('/api')
            self.assertEqual(resp.status_code, 200)

    # this test case hits the compound/explore of the application
    def test_compound_explore_page(self):
        with app.test_client() as c:
            resp = c.get('/compound/explore')
            self.assertEqual(resp.status_code, 200)

    def test_render_drug_classes(self):
        with app.test_client() as c:
            resp = c.get('/classes')
            self.assertEqual(resp.status_code, 200)
