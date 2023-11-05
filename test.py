
import requests, json

def register_user():
        
        url = "http://127.0.0.1:5000/api/auth/register"

        headers = {
               
                "Content-Type": "application/json",
        }

        body = {
                "first_name": "Antony",
                "last_name": "Kariuki",
                "email": "email@gmail.com",
                "password":"password"
        }

        request = requests.post(url=url, headers=headers, json=body)
        print(request.status_code)
        response = request.json()
        print(json.dumps(response, sort_keys=False, ensure_ascii=True, indent=4, separators=(",", ": ")))


def login_user():
        
        url ="http://studentcrud1.pythonanywhere.com/api/auth/login"

        headers = {
                "Content-Type": "application/json",
        }

        body = {
                "first_name": "Antony",
                "last_name": "Kariuki",
                "email": "email@gmail.com",
                "password":"password"
        }

        request = requests.post(url=url, headers=headers, json=body)
        protected_response = requests.get("http://studentcrud1.pythonanywhere.com/api/views/userblogs", cookies=request.cookies)

    # Check the response from the protected endpoint
        if protected_response.status_code == 200:
           print(protected_response.json())

        response = request.json()
        print(json.dumps(response, sort_keys=False, ensure_ascii=True, indent=4, separators=(",", ": ")))


def short_hand_login():
       headers = {
                "Content-Type": "application/json",
        }
       data = {
              "email": "email@gmail.com",
              "password": "password"
       }
       response = requests.post("http://studentcrud1.pythonanywhere.com/api/auth/login", json=data, headers=headers)
       if response.status_code == 200:
              return response
       
       return None

def get_all_blogs():
        
        url = "http://studentcrud1.pythonanywhere.com/api/views/blogs"

        headers = {
                "Content-Type": "application/json",
        }
        res = short_hand_login()
        request = requests.get(url=url, headers=headers, cookies=res.cookies)
        print(request.status_code)
        response = request.json()
        print(json.dumps(response, sort_keys=False, ensure_ascii=True, indent=4, separators=(",", ": ")))

def get_all_user_blogs():
        
        url = "http://studentcrud1.pythonanywhere.com/api/views/userblogs"

        headers = {
                "Content-Type": "application/json",
        }

        request = requests.get(url=url, headers=headers)
        print(request.status_code)
        response = request.json()
        print(json.dumps(response, sort_keys=False, ensure_ascii=True, indent=4, separators=(",", ": ")))

def create_a_blog():
        
        url = "http://studentcrud1.pythonanywhere.com/api/views/createblog"

        headers = {
                "Content-Type": "application/json",
        }

        body = {

                "title": "why womwn deserve less", 
                "category": "mariage in general",
                 "content": "good content"
        }

        request = requests.post(url=url, headers=headers, json=body, cookies=short_hand_login().cookies)
        print(request.status_code)
        response = request.json()
        print(json.dumps(response, sort_keys=False, ensure_ascii=True, indent=4, separators=(",", ": ")))

if __name__ == "__main__":
        # get_all_user_blogs()
        # login_user()
        # get_all_blogs()
        # create_a_blog()
        register_user()