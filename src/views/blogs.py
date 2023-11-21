from flask import Blueprint, request, jsonify, Response, json
from src.models.database import( User, News, Business, Sports, Entertainment,NewsComments,
BusinessComments, SportsComments, EntertainmentComments)
from ..models.database import db
from flask_cors import cross_origin
from datetime import datetime, timedelta

blogs = Blueprint("view", __name__,)

""" A function to convert time from GMT to EAT """
def covert_time_from_GMT_to_EAT(time_):
    input_time = datetime.strptime(time_, "%a, %d %b %Y %H:%M:%S %Z")
    time_in_eat = input_time + timedelta(hours=3)
    time_in_eat_str = time_in_eat.strftime("%a, %d %b %Y %H:%M:%S %Z")
    return time_in_eat
       

@blogs.route("/")
@cross_origin() 
def home_page():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("pages", 3, type=int)
    per_page_news = request.args.get("pages", 4, type=int)

    response = Response(response=json.dumps({
            
            "News": get_brief_home_news(News,page, per_page_news),
            "Business": get_brief_home_news(Business, page, per_page),
            "Sports": get_brief_home_news(Sports, page, per_page),
            "Entertainment": get_brief_home_news(Entertainment, page, per_page)

    }), status=200, 
    mimetype="application/json")

    return response


""" An endpoint to get all the news blogs in the database """
@blogs.route("/news")
@cross_origin() 
def get_all_news_blogs():

        all_news = get_all_blogs_with_category(model=News)
        return all_news, 200

""" An endpoint to get all the business blogs in the database """
@blogs.route("/business")
@cross_origin() 
def get_all_business_blogs():

        all_business = get_all_blogs_with_category(model=Business)

        return  all_business, 200


""" An endpoint to get all the Sports blogs in the database """
@blogs.route("/sports")
@cross_origin() 
def get_all_sports_blogs():

        all_sports = get_all_blogs_with_category(model=Sports)
        
        return all_sports, 200


""" An endpoint to get all the entertainment blogs in the database """
@blogs.route("/entertainment")
@cross_origin() 
def get_all_entertainment_blogs():

        all_entertainment = get_all_blogs_with_category(model=Entertainment)

        return all_entertainment, 200

"""  An endpoint to get the data associated with the id presented  """
@blogs.route('/<string:category>/<int:id>')
@cross_origin() 
def get_all_info(category, id): 
        error_message = {"error": f"{category} Image with id {id} does not exist"}        
        if category == "News":
                blog_data = get_blog_info(category=News, id=id)
                if blog_data:
                       return blog_data, 200
                
                return jsonify(error_message), 404
        
        elif category == "Business":
                blog_data = get_blog_info(category=Business, id=id)
                if blog_data:
                       return blog_data, 200
                
                return jsonify(error_message), 404
        
        elif category == "Sports":
                blog_data = get_blog_info(category=Sports, id=id)
                if blog_data:
                        return blog_data, 200
                
                return jsonify(error_message), 404
                
        elif category == "Entertainment":
                blog_data = get_blog_info(category=Entertainment, id=id)
                if blog_data:
                        return blog_data, 200
                
                return jsonify(error_message), 404
                
        return jsonify({"error": "Invalid category"}), 400

"""  An endpoint to get the latest blog in each category"""
@blogs.route('/blog/latest')
@cross_origin() 
def get_latest_blog_per_category() -> str:
     response = Response(response=json.dumps(
            {
                "News": get_latest_blog_per_category(News),
                "Business": get_latest_blog_per_category(Business),
                "Sports": get_latest_blog_per_category(Sports),
                "Entertainment": get_latest_blog_per_category(Entertainment)
                }
                ), 
                status=200, 
                mimetype="application/json")

     return response, 200
       
""" An endpoint to get all the blogs written by the current user """
@blogs.route("/authorblogs/<string:fullname>")
@cross_origin() 
def get_all_user_blogs(fullname):
        first_name = fullname.split(" ")[0]
        all_blogs = User.query.filter_by(first_name=first_name).first()
        if all_blogs:
               news_blogs = get_user_blogs_based_on_category(all_blogs.news)
               business_blogs = get_user_blogs_based_on_category(all_blogs.business)
               sports_blogs = get_user_blogs_based_on_category(all_blogs.sports)
               entertainment_blogs = get_user_blogs_based_on_category(all_blogs.entertainment)
               combined_blogs = news_blogs+business_blogs+sports_blogs+entertainment_blogs
               total_blogs = len(news_blogs) + len(business_blogs) + len(sports_blogs) + len(entertainment_blogs)
               print("Total blogs: ", total_blogs)
                
               return [total_blogs, combined_blogs], 200
        else:
            return {"error": f"No user with username {first_name}"}, 400


""" An endpoint to create comment associated with a blog """
@blogs.route('/comment/<string:category>/<int:id>', methods=['POST'])
@cross_origin() 
def create_comment(category, id):
        success_message = f"new {category} comment added successfully"
        error_message = f"Failed to create a new comment. check the image id provided"
        data = request.get_json()
        if not "content" in data:
              return jsonify({"Error": "content required"}), 400
        
        elif category == "News":
               if create_comment(category=NewsComments,category1=News, id=id, data=data):
                      return jsonify({"success": success_message}), 201
               
               return jsonify({"error": error_message}), 404
        
        elif category == "Business":
               if create_comment(category=BusinessComments, category1=Business, id=id, data=data):
                      return jsonify({"success": success_message}), 201
               
               return jsonify({"error": error_message}), 404
        
        elif category == "Sports":
               if create_comment(category=SportsComments,category1=Sports, id=id, data=data):
                      return jsonify({"success": success_message}), 201
               
               return jsonify({"error": error_message}), 404
        
        elif category == "Entertainment":
               if create_comment(category=EntertainmentComments,category1=Entertainment, id=id, data=data):
                      return jsonify({"success": success_message}), 201
               
               return jsonify({"error": error_message}), 404
        
        else:
               return jsonify({"error": "Invalid category"}), 400


""" This is a function to query and return the 
    brief news found in the home page         """
def get_brief_home_news(model, page, per_page):
        blogs = model.query.order_by(model.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        serialized = []
        for blog in blogs:
                serialized.append({
                       "id": blog.id,
                        "image": blog.image_id,
                        "author": get_the_user_based_on_author_id(blog.author_id),
                        "title": blog.title,
                        "slug": blog.slug,
                        "published_on": blog.published_on
                })
        
        return serialized

""" A function to get the user associated with blogs in the home page """
def get_the_user_based_on_author_id(author_id):
       user = User.query.filter_by(id=author_id).first()
       if user:
              return f"{user.first_name} {user.last_name}"
       
       return None

""" This is a function to query and return all 
    the blogs associated with a certain category   """
def get_all_blogs_with_category(model)-> list:
        all_blogs = model.query.order_by(model.id.desc()).all()
        serialized = []
        for blog in all_blogs:
                serialized.append(
                        {
                          "id": blog.id,
                          "title": blog.title,
                          "slug": blog.slug,
                          "image_id": blog.image_id,
                          "published_on": blog.published_on,
                        }
                )
        
        return serialized

""" A function to get the all the data of an blog  """
def get_blog_info (category, id):
        data = category.query.filter_by(id=id).first()
        if data:
           author = User.query.filter_by(id=data.author_id).first()
           return jsonify({
                "title": data.title,
                "slug": data.slug,
                "image": data.image_id,
                "body": data.body,
                "author": f"{author.first_name} {author.last_name}",
                "published_on": data.published_on,
                "author_image": author.image_id
                 }
                 )
        else:
            return False

""" A function to loop through a specific user blogs """
def get_user_blogs_based_on_category(blogs):
        serialized = []
        for blog in blogs:
                serialized.append({
                        "image_id": blog.image_id,
                        "title": blog.title,
                        "slug": blog.slug,
                        "published_on": blog.published_on
                })

        return serialized


""" A function to create a comment"""
def create_comment (category, category1, id, data):
        content = data["content"]
        is_anonymous = data.get("is_anonymous", True)
        blog = category1.query.filter_by(id=id).first()
        if blog:
           new_comment = category(content=content, is_anonymous = is_anonymous , blog_id= blog.id)
           db.session.add(new_comment)
           db.session.commit()
           return True

        return False

""" A function to get the latest blog per category """
def get_latest_blog_per_category(model):
        blog = model.query.order_by(model.id.desc()).first()
        serialized = {
                       "id": blog.id,
                        "image": blog.image_id,
                        "title": blog.title,
                        "published_on": blog.published_on
                }
        
        return serialized


