# MMUST-JOWA
This project contains code for a blogging web app which enables users to easily share, express and publish the contents in the form of blog.


### Technologies Used

* _python_
* _flask_

## Getting Started
### Installations
You can use the git clone  command as follows:
```sh 
user@username:~$ git clone https://github.com/BudhaBudha/Mmust-Jowa.git 
user@username:~$ cd  Mmust-Jowa
user@username:~$ python -m venv my_venv # create a virtual env to manage your dependecies
user@username:~$ source my_venv/bin/activate  # for linux users
user@username:~$ pip3 install -r requirements.txt  #install all the dependecies used in this project
user@username:~$ flask run  # use this command to start the server
```  
### User registration    
#### User gets registered to the system by making a request to the endpoint below
   + url: POST  [https://mmust-jowa.onrender.com/api/auth/register]()
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
https://mmust-jowa.onrender.com/
 + url: POST  [https://mmust-jowa.onrender.com/api/auth/login]()
   ```python
    headers: 
        Content-type: application/json

   request body:
       email: string,
       password: string
   ````
User is given an access token, with The status_code of the response == 200 if the login is successfull else returns unauthorized error.(401).

## Create Blogs 
#### Only users with access previledges are able to create blogs.
  + url:  POST  [https://mmust-jowa.onrender.com/createblog]()
  +
    ```python
    headers:
      content-type: application/json
      Authorization: Bearer <token>
    ```
  +
    ```python
    Request Body:
        title: string
        slug: string 
        body: string 
        image_id: string 
        category: string

    Example of a request body
       { 
        "title": "Title of the blog",
        "slug": "a brief description about the blog",
        "body": "The body of the blog",
        "image_id": "A unique id of an image associated with the blog",
        "category": "Either of the following: [News, Business, Sports, Entertainment]"

       }
    ```
     The status_code of the response == 201 if the blog was created successfully else a bad request error(400) is thrown. user should ensure that all the fields above are included.


## Home page of the blog app
A limited number of blogs from each category are displayed here . Blogs are displayed according to the time they were created with the latest blog being the first.
  + url: GET  [https://mmust-jowa.onrender.com/]()

  + The response  body of the  * _RESPONSE_* have the following fields
    
      +
    ```python
    Exampe of a Response Body:

     News:
        title: string
        slug: string 
        author: string 
        image_id: string 
        published_on: string

     Business:
       title: string
       slug: string 
       author: string 
       image_id: string 
       published_on: string
    ```
  + Note: Only three blogs per category are returned in the response


  ## News Blogs
  when a user clicks on the news button on the navbar, the frontend sends a request to the backed which then returnes all blogs associated with the news category.

  + url: GET  [https://mmust-jowa.onrender.com/news]()

  + The response  body  is a list/array of all the news blogs.
    
  +
    ```python
    Response Body of a single blog in the array:

        title: string
        slug: string 
        author: string 
        image_id: string 
        published_on: string
    
    Exampe of a Response Body of a single blog in the array
      {
		"image_id": "0123456712325.jpg",
		"published_on": "Tue, 07 Nov 2023 11:14:27 GMT",
		"slug": "This is a long blog",
		"title": "This is a long blog"
	}
    ```


 ## Business Blogs
  when a user clicks on the business button on the navbar, the frontend sends a request to the backed which then returnes all blogs associated with the business category.

  + url: GET  [https://mmust-jowa.onrender.com/business]()

  + The response  body  is a list/array of all the business blogs.
    
  +
    ```python
    Response Body of a single blog in the array:

        title: string
        slug: string 
        author: string 
        image_id: string 
        published_on: string
    
    Exampe of a Response Body of a single blog in the array
      {
		"image_id": "0123456712325.jpg",
		"published_on": "Tue, 07 Nov 2023 11:14:27 GMT",
		"slug": "This is a long blog",
		"title": "This is a long blog"
	}
    ```


 ## Sports Blogs

  + url: GET  [https://mmust-jowa.onrender.com/sports]()
    
  +
    ```python
    Response Body of a single blog in the array:

        title: string
        slug: string 
        author: string 
        image_id: string 
        published_on: string
    
    Exampe of a Response Body of a single blog in the array
      {
		"image_id": "0123456712325.jpg",
		"published_on": "Tue, 07 Nov 2023 11:14:27 GMT",
		"slug": "This is a long blog",
		"title": "This is a long blog"
	}
    ```


 ## Entertainment Blogs

  + url: GET  [https://mmust-jowa.onrender.com/entertainment]()
    
  +
    ```python
    Response Body of a single blog in the array:

        title: string
        slug: string 
        author: string 
        image_id: string 
        published_on: string
    
    Exampe of a Response Body of a single blog in the array
      {
		"image_id": "0123456712325.jpg",
		"published_on": "Tue, 07 Nov 2023 11:14:27 GMT",
		"slug": "This is a long blog",
		"title": "This is a long blog"
	}
    ```

