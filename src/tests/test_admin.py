import json
import unittest
from .. import create_app, config_dict, db

class TestAdmin(unittest.TestCase):

   def setUp(self) -> None:
      self.app = create_app(config=config_dict["testing"])
      self.client = self.app.test_client()
      self.app_context = self.app.app_context()
      self.app_context.push()
      db.create_all()
      print("database tables created successfully")
   
   def tearDown(self) -> None:
      db.drop_all()
      self.app_context.pop()
      self.client = None
      print("database tables dropped")

   def test_admin_registration(self):
      """
      test if an admin can be created 
      """
      url = "/api/v1/admin/register"
      data = {
         "first_name": "Antony",
         "last_name": "Kariuki",
         "email": "user@gmail.com",
         "password": "password"
      }
      response = self.client.post(url, json=json.dumps(data))
      self.assertEqual(response.status_code, 201)