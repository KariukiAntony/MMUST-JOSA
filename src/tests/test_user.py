import unittest
from .. import create_app, config_dict, db


class TestUser(unittest.TestCase):
   user_relative_url = "/api/v1/user"
   def setUp(self) -> None:
      self.app = create_app(config=config_dict["test"])
      self.client = self.app.test_client()
      self.app_context = self.app.app_context()
      self.app_context.push()
      db.create_all()

   def test_homepage_blogs(self):
      response = self.client.get(f"{self.user_relative_url}/")
      self.assertEqual(response.status_code, 200)
   
   def test_news_blogs(self):
      response = self.client.get(f"{self.user_relative_url}/news")
      self.assertEqual(response.status_code, 200)
   
   def test_business_blogs(self):
      response = self.client.get(f"{self.user_relative_url}/business")
      self.assertEqual(response.status_code, 200)

   def test_sports_blogs(self):
      response = self.client.get(f"{self.user_relative_url}/sports")
      self.assertEqual(response.status_code, 200)

   def test_entertainment_blogs(self):
      response = self.client.get(f"{self.user_relative_url}/entertainment")
      self.assertEqual(response.status_code, 200)

   def tearDown(self) -> None:
      db.drop_all()
      self.app_context.pop()
      self.client = None

