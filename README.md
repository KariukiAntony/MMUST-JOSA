# student-management
This project contains code for a blogging web app which enables users to easily share, express and publish the contents in the form of blog.


### Technologies Used

* _python_
* _flask_

## Getting Started
### Installations
You can use the git clone  command as follows:
```sh 
user@username:~$ git clone https://github.com/parlgy/student-management.git  
user@username:~$ cd  student-management
user@username:~$ python -m venv my_venv # create a virtual env to manage your dependecies
user@username:~$ source my_venv/bin/activate  # for linux users
user@username:~$ pip3 install -r requirements.txt  #install all the dependecies used in this project
user@username:~$ flask run  # use this command to start the server
```  
### User registration    
#### User gets registered to the system by making a request to the endpoint below
   + url: POST  [http://studentcrud1.pythonanywhere.com/api/auth/register]()
   ```python
    headers: 
        Content-type: application/json

   request body:
       first_name: string,
       last_name: string,
       email: string,
       password: string
````
    
The status_code of the response == 201 if the registration is successfull else returns a bad request error.(400).
user should double check the registration credentials.

## User Login  
#### User gets logged into the system by making a post request to the following endpoint
 + url: POST  [http://studentcrud1.pythonanywhere.com/api/auth/login]()
   ```python
    headers: 
        Content-type: application/json

   request body:
       email: string,
       password: string
   ````
The status_code of the response == 200 if the login is successfull else returns unauthorized error.(401).

## Get all blogs in the system 
  + url: GET  [http://studentcrud1.pythonanywhere.com/api/views/blog]()
   +
     ```python
     headers:
     content-type: application/json
     ```

## Get all blogs assocciated with the current user
  + url: GET  [http://studentcrud1.pythonanywhere.com/api/views/userblogs]()
   + Login required
     ```python
     headers:
     content-type: application/json
     ```
     
