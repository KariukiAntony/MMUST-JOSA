import json
import unittest
from .. import create_app, config_dict, db
from werkzeug.security import generate_password_hash

class TestAdmin(unittest.TestCase):

   def setUp(self) -> None:
      self.app = create_app(config=config_dict["test"])
      self.client = self.app.test_client()
      self.app_context = self.app.app_context()
      self.app_context.push()
      db.create_all()
      print("database tables created successfully")

   def test_admin_registration(self):
      """
      test if an admin can be created 
      """
      url = "/api/v1/auth/register"
      data = {
         "first_name": "Antony",
         "last_name": "Kariuki",
         "email": "user@gmail.com",
         "password": "password",
         "confirm": "password"
      }
      response = self.client.post(url, data=json.dumps(data), content_type="application/json")
      # print(response.text)
      self.assertEqual(response.status_code, 201)

   def test_admin_login(self):
      data = {
         "email": "user@gmail.com",
         "password": "password"
      }
      url = "/api/v1/auth/login"
      response = self.client.post(url, json=data)
      print(response.text)
      self.assertEqual(response.status_code, 200)
      
   
   def tearDown(self) -> None:
      """drop the datebase tables
      """ 
      db.drop_all()
      self.client = None
      self.app_context.pop()