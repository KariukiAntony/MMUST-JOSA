import json
import unittest
from .. import create_app, config_dict, db
from werkzeug.security import generate_password_hash

class TestAdmin(unittest.TestCase):
   admin_relative_url = "/api/v1/admin"
   token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDc5MDc1MSwianRpIjoiYzk0OTI4ZjItYTZmNi00OTFjLTgwMTEtNmExY2RiZWUwMzI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNzA0NzkwNzUxLCJleHAiOjE3MDQ4NzcxNTF9.T5Mj-fDqzTmAZRaPrzEOIHV_KKhngIzJojXs9COabzg"

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
      # print(response.text)
      self.assertEqual(response.status_code, 200)
      
   def test_admin_total_blogs(self):
      headers = {
         "Authorization": f"Bearer {self.token}"
      }
      response = self.client.get(f"{self.admin_relative_url}/total/blogs", headers = headers)
      self.assertEqual(response.status_code, 200)

   def test_admin_total_comments(self):
      headers = {
         "Authorization": f"Bearer {self.token}"
      }
      response = self.client.get(f"{self.admin_relative_url}/total/comments", headers = headers)
      self.assertEqual(response.status_code, 200)

   def test_admin_latest_five_news(self):
      headers = {
         "Authorization": f"Bearer {self.token}"
      }
      response = self.client.get(f"{self.admin_relative_url}/news/latest", headers = headers)
      self.assertEqual(response.status_code, 200)
   
   def tearDown(self) -> None:
      """drop the datebase tables
      """ 
      db.drop_all()
      self.client = None
      self.app_context.pop()