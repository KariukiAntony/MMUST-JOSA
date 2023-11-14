from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from ..models.database import db
from src.models.database import( User, News, Business, Sports, Entertainment,NewsComments,
BusinessComments, SportsComments, EntertainmentComments)
from flask_jwt_extended import get_jwt_identity, jwt_required
import requests
import logging

admin = Blueprint("admin", __name__,)


""" An endpoint to get the total number of blogs owned by admin """
@admin.route("/total/blogs")
@cross_origin()
@jwt_required()
def get_admin_total_blogs():
    user_id = get_jwt_identity()
    author = User.query.filter_by(id=user_id).first()
    author_first_name = author.first_name
    try:
        res = requests.get(f"https://mmust-jowa.onrender.com/api/v1/user/authorblogs/{author_first_name}")
        if res.status_code == 200:
            total_blogs = res.json()[0]
            return str(total_blogs), 200

        logging.error(f"failed to send the request with status code: {res.status_code}")

    except Exception as e:
          logging.error(f"An error has occured: {e}")
    
    return author_first_name, 200

""" An endpoint to get the total number of comments owned by admin """
@admin.route("/total/comments")
@cross_origin()
@jwt_required()
def get_admin_total_comments():
    user_id = get_jwt_identity()
    news_comments = get_news_and_comments(user_id=user_id)[1]
    business_comments = get_business_and_comments(user_id=user_id)[1]
    sports_comments = get_sports_and_comments(user_id=user_id)[1]
    entertainment_comments = get_entertainment_and_comments(user_id=user_id)[1]
    total_comments = news_comments + business_comments+\
    sports_comments + entertainment_comments
    
    return str(total_comments), 200



""" An endpoint to get the latest five news blogs """
@admin.route("/news/latest")
@cross_origin()
@jwt_required()
def get_latest_five_news_blogs():
    user_id = get_jwt_identity()
    latest_blogs = News.query.filter_by(author_id=user_id).order_by(News.id.desc()).paginate(page=1, per_page=5, error_out=False)
    serialized = []
    for blog in latest_blogs:
        total_comments = len(blog.comments)
        serialized.append({
                "id": blog.id,
                "image_id": blog.image_id,
                "title": blog.title,
                "published_on": blog.published_on,
                "total_comments": total_comments
        })
    
    return serialized

""" An endpoint to update the blogs based on the category dashboard """
@admin.route("/blogs/update/<string:category>/<int:id>", methods = ["PUT"])
@cross_origin()
def update_blog_in_latest_news(category, id):
    success_msg = "Blog updated successfully"
    error_msg = "invalid id passed"
    data = request.get_json()
    if category == "News":
        if update_blog(category=News, id=id, data=data):
           return make_response(jsonify({"success": success_msg})), 202
        
        return make_response(jsonify({"error": error_msg})), 404

    elif category == "Business":
        if update_blog(category=Business, id=id, data=data):
           return make_response(jsonify({"success": success_msg})), 202
        
        return make_response(jsonify({"error": error_msg})), 404

    elif category == "Sports":
        if update_blog(category=Sports, id=id, data=data):
           return make_response(jsonify({"success": success_msg})), 202
        
        return make_response(jsonify({"error": error_msg})), 404

    elif category == "Entertainment":
        if update_blog(category=Entertainment, id=id, data=data):
           return make_response(jsonify({"success": success_msg})), 202
        
        return make_response(jsonify({"error": error_msg})), 404

    
    return make_response(jsonify({"error":"Invalid category passed"})), 400


""" An endpoint to delete the five latest blogs in admin homepage """
@admin.route("/news/latest/delete/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_blog_in_latest(id):
      blog = News.query.filter_by(id=id).first()
      if blog:
            db.session.delete(blog)
            db.session.commit()
            return jsonify({"success": "Image deleted succesfully"}), 204
      
      return {"error": f"Image with id {id} not found"}, 404


""" An endpoint to get the total number of news blogs owned by author """
@admin.route("/total/news")
@cross_origin()
@jwt_required()
def get_admin_total_news_blogs():
    user_id = get_jwt_identity()
    total_news = get_news_and_comments(user_id=user_id)[0]
    
    return str(total_news), 200

""" An endpoint to get the total number of comments associated with all news blogs """
@admin.route("/total/news/comments")
@cross_origin()
@jwt_required()
def get_admin_total_news_comments():
    user_id = get_jwt_identity()
    total_news = get_news_and_comments(user_id=user_id)[1]
    
    return str(total_news), 200



""" An endpoint to get all the News blogs written by admin """
@admin.route("/blogs/news")
@cross_origin()
@jwt_required()
def get_all_user_news__blogs():
    user_id = get_jwt_identity()
    user_news_blogs =  News.query.filter_by(author_id=user_id).\
        order_by(News.id.desc()).all()
    seliarized_blogs = seliarize_user_news__blogs\
        (user_blogs=user_news_blogs, comments_model=NewsComments)
    return seliarized_blogs, 200

""" An endpoint to get the total number of business blogs owned by author """
@admin.route("/total/business")
@cross_origin()
@jwt_required()
def get_admin_total_business_blogs():
    user_id = get_jwt_identity()
    total_business = get_business_and_comments(user_id=user_id)[0]
    
    return str(total_business), 200

""" An endpoint to get the total number of comments associated with all business blogs """
@admin.route("/total/business/comments")
@cross_origin()
@jwt_required()
def get_admin_total_business_comments():
    user_id = get_jwt_identity()
    total_business = get_business_and_comments(user_id=user_id)[1]
    
    return str(total_business), 200

""" An endpoint to get all the Business blogs written by admin """
@admin.route("/blogs/business")
@cross_origin()
@jwt_required()
def get_all_user_business_blogs():
    user_id = get_jwt_identity()
    user_news_blogs =  Business.query.filter_by(author_id=user_id).\
        order_by(Business.id.desc()).all()
    seliarized_blogs = seliarize_user_news__blogs\
        (user_blogs=user_news_blogs, comments_model=BusinessComments)
    return seliarized_blogs, 200

""" An endpoint to get the total number of sports blogs owned by author """
@admin.route("/total/sports")
@cross_origin()
@jwt_required()
def get_admin_total_sports_blogs():
    user_id = get_jwt_identity()
    total_sports = get_sports_and_comments(user_id=user_id)[0]
    
    return str(total_sports), 200

""" An endpoint to get the total number of comments associated with all business blogs """
@admin.route("/total/sports/comments")
@cross_origin()
@jwt_required()
def get_admin_total_sports_comments():
    user_id = get_jwt_identity()
    total_sports = get_sports_and_comments(user_id=user_id)[1]
    
    return str(total_sports), 200


""" An endpoint to get all the Sports blogs written by admin """
@admin.route("/blogs/sports")
@cross_origin()
@jwt_required()
def get_all_user_sports_blogs():
    user_id = get_jwt_identity()
    user_news_blogs =  Sports.query.filter_by(author_id=user_id).\
        order_by(Sports.id.desc()).all()
    seliarized_blogs = seliarize_user_news__blogs\
        (user_blogs=user_news_blogs, comments_model=SportsComments)
    return seliarized_blogs, 200

""" An endpoint to get the total number of sports blogs owned by author """
@admin.route("/total/entertainment")
@cross_origin()
@jwt_required()
def get_admin_total_entertainment_blogs():
    user_id = get_jwt_identity()
    total_entertainment = get_entertainment_and_comments(user_id=user_id)[0]
    
    return str(total_entertainment), 200

""" An endpoint to get the total number of comments associated with all business blogs """
@admin.route("/total/entertainment/comments")
@cross_origin()
@jwt_required()
def get_admin_total_entertainment_comments():
    user_id = get_jwt_identity()
    total_entertainment = get_entertainment_and_comments(user_id=user_id)[1]
    
    return str(total_entertainment), 200


""" An endpoint to get all the Sports blogs written by admin """
@admin.route("/blogs/entertainment")
@cross_origin()
@jwt_required()
def get_all_user_entertainment_blogs():
    user_id = get_jwt_identity()
    user_news_blogs =  Entertainment.query.filter_by\
        (author_id=user_id).order_by(Entertainment.id.desc()).all()
    seliarized_blogs = seliarize_user_news__blogs\
        (user_blogs=user_news_blogs, comments_model=EntertainmentComments)
    return seliarized_blogs, 200


""" An endpoint to create  a blog """
@admin.route("/createblog", methods=["POST"])
@cross_origin() 
@jwt_required()
def create_a_new_blog():
    if not request.content_type == "application/json":
            return jsonify({"failed": "content_type must be application/json"}), 400
    user_id = get_jwt_identity()
    data = request.get_json()
    print(data)
    if validate_blog_data(data):
        if data["category"] == "News":
            add_new_blog_data(News, data, user_id)
            return jsonify({"success": f"A new {data['category']}\
                    Blog created successfully"}), 201
        
        elif data["category"] == "Business":
            add_new_blog_data(Business, data, user_id)
            return jsonify({"success": f"A new {data['category']}\
                    Blog created successfully"}), 201
        
        elif data["category"] == "Sports":
            add_new_blog_data(Sports, data, user_id)
            return jsonify({"success": f"A new {data['category']}\
                    Blog created successfully"}), 201
        
        elif data["category"] == "Entertainment":
            add_new_blog_data(Entertainment, data, user_id)
            return jsonify({"success": f"A new {data['category']} \
                Blog created successfully"}), 201

    
    return jsonify({"failed": "All fields are required"}), 400

""" An endpoint to delete a blog based on the category """
@admin.route("/blogs/delete/<string:category>/<int:id>", methods=["DELETE"])
def delete_blog(category, id):
    if category == "News":
        if delete_blog(category=News, id=id):
             return " ", 204

        return jsonify({"failed": "double check the image_id"}), 404

    elif category == "Business":
        if delete_blog(category=Business, id=id):
             return " ", 204

        return jsonify({"failed": "double check the image_id"}), 404
    
    elif category == "Sports":
        if delete_blog(category=Sports, id=id):
             return " ", 204

        return jsonify({"failed": "double check the image_id"}), 404

    elif category == "Entertainment":
        if delete_blog(category=Entertainment, id=id):
             return " ", 204

        return jsonify({"failed": "double check the image_id"}), 404

    else:
        return jsonify({"failed": "Invalid category passed"}), 404


""" A function to add blogs according to its category """
def add_new_blog_data(model, data, author_id)-> None:
        new_blog = model(title=data["title"],
                          slug=data["slug"], 
                          image_id=data["image_id"],
                          body=data["body"],
                          author_id = author_id
                          ) 
        db.session.add(new_blog)
        db.session.commit()

""" A function to validate blogs info """
def validate_blog_data(user_input) -> bool:
        
        if "title" in user_input and "slug" in user_input and "body" \
            in user_input and "image_id" in user_input \
                  and "category" in user_input:
                return True
        
        return False

""" A function to seliarize all blogs owned by admin according to blogs passed"""
def seliarize_user_news__blogs(user_blogs, comments_model) -> list:
    seliarized = []
    for blog in user_blogs:
        selialized_comments = []
        blog_comments = comments_model.query.filter_by(blog_id=blog.id).order_by(comments_model.id.desc()).all()
        for comment in blog_comments:
            selialized_comments.append(
                {
                    "content": comment.content,
                    "is_anonymous": comment.is_anonymous,
                    "commented_on": comment.date_created
                }
            )
        seliarized.append({
             "id": blog.id,
             "title": blog.title,
             "slug": blog.slug,
             "image_id": blog.image_id,
             "body": blog.body,
             "published_on": blog.published_on,
             "comments": selialized_comments
        })
            
    return seliarized

""" A function to delete a blog """
def delete_blog(category, id) -> bool:
    data = category.query.filter_by(id=id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
        return True

    return False

""" A function to update  a blog """
def update_blog(category, id, data) -> bool:
    data = category.query.filter_by(id=id).first()
    if data:
        data.title = data.get("title")
        data.slug = data.get("slug")
        data.body = data.get("body")
        data.image_id = data.image_id
        db.session.commit()
        return True

    return False

""" A function to get the number of news post and associated comments """
def get_news_and_comments(user_id: int) -> str:
    news_blogs = News.query.filter_by(author_id= user_id).all()
    total_news = len(news_blogs)
    comments = 0
    for blog in news_blogs:
         comments += len(blog.comments)
  
    return [total_news, comments]

""" A function to get the number of business post and associated comments """
def get_business_and_comments(user_id: int) -> str:
    business_blogs = Business.query.filter_by(author_id= user_id).all()
    total_business = len(business_blogs)
    comments = 0
    for blog in business_blogs:
         comments += len(blog.comment)
  
    return [total_business, comments]

""" A function to get the number of sports post and associated comments """
def get_sports_and_comments(user_id: int) -> str:
    sports_blogs = Sports.query.filter_by(author_id= user_id).all()
    total_sports = len(sports_blogs)
    comments = 0
    for blog in sports_blogs:
         comments += len(blog.comment)
  
    return [total_sports, comments]

""" A function to get the number of entertainment post and associated comments """
def get_entertainment_and_comments(user_id: int) -> str:
    news_blogs = Entertainment.query.filter_by(author_id= user_id).all()
    total_news = len(news_blogs)
    comments = 0
    for blog in news_blogs:
         comments += len(blog.comment)
  
    return [total_news, comments]
    

        
          
            

