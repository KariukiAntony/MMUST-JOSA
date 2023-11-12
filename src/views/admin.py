from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from ..models.database import db
from src.models.database import( User, News, Business, Sports, Entertainment,NewsComments,
BusinessComments, SportsComments, EntertainmentComments)
from flask_jwt_extended import get_jwt_identity, jwt_required
import requests
import logging
from .blogs import get_good_time

admin = Blueprint("admin", __name__,)


""" An endpoint to get the total number of blogs owned by admin """
@admin.route("/totalblogs")
@cross_origin()
@jwt_required()
def get_admin_total_blogs():
    user_id = get_jwt_identity()
    author = User.query.filter_by(id=user_id).first()
    author_first_name = author.first_name
    try:
        res = requests.get(f"http://127.0.0.1:5000/api/v1/blogs/authorblogs/{author_first_name}")
        if res.status_code == 200:
            total_blogs = res.json()[0]
            return str(total_blogs), 200

        logging.error(f"failed to send the request with status code: {res.status_code}")

    except Exception as e:
          logging.error(f"An error has occured: {e}")
    
    return author_first_name, 200



""" An endpoint to get the latest five news blogs """
@admin.route("/news/latest")
@cross_origin()
@jwt_required()
def get_latest_five_news_blogs():
    user_id = get_jwt_identity()
    latest_blogs = News.query.filter_by(author_id=user_id).order_by(News.id.desc()).paginate(page=1, per_page=5, error_out=False)
    serialized = []
    for blog in latest_blogs:
            serialized.append({
                    "image_id": blog.image_id,
                    "title": blog.title,
                    "published_on": get_good_time(blog.published_on)
            })
    
    return serialized

""" An endpoint to update the blogs in the admin dashboard """
@admin.route("/news/latest/update/<string:image_id>", methods = ["PUT"])
@cross_origin()
def update_blog_in_latest_news(image_id):
      data = request.get_json()
      blog = News.query.filter_by(image_id=image_id).first()
      if blog:
            blog.title = data.get("title")
            blog.slug = data.get("slug")
            blog.body = data.get("body")
            db.session.commit()
            return make_response(jsonify({"success": "Blog updated successfully"})), 202
      
      return make_response(jsonify({"error": f"News blog with image_id {image_id} was not found!"})), 404


""" An endpoint to delete the five latest blogs in admin homepage """
@admin.route("/news/latest/delete/<string:image_id>", methods=["DELETE"])
@cross_origin()
def delete_blog_in_latest(image_id):
      blog = News.query.filter_by(image_id=image_id).first()
      if blog:
            db.session.delete(blog)
            db.session.commit()
            return jsonify({"success": "Image deleted succesfully"}), 204
      
      return {"error": f"Image with id {image_id} not found"}, 404


""" An endpoint to get all the News blogs written by admin """
@admin.route("/blogs/news")
@cross_origin()
@jwt_required()
def get_all_user_news__blogs():
    user_id = get_jwt_identity()
    user_news_blogs =  News.query.filter_by(author_id=user_id).order_by(News.id.desc()).all()
    seliarized_blogs = seliarize_user_news__blogs(user_blogs=user_news_blogs, comments_model=NewsComments)
    return seliarized_blogs, 200


""" An endpoint to get all the Business blogs written by admin """
@admin.route("/blogs/business")
@cross_origin()
@jwt_required()
def get_all_user_business_blogs():
    user_id = get_jwt_identity()
    user_news_blogs =  Business.query.filter_by(author_id=user_id).order_by(Business.id.desc()).all()
    seliarized_blogs = seliarize_user_news__blogs(user_blogs=user_news_blogs, comments_model=BusinessComments)
    return seliarized_blogs, 200


""" An endpoint to get all the Sports blogs written by admin """
@admin.route("/blogs/sports")
@cross_origin()
@jwt_required()
def get_all_user_sports_blogs():
    user_id = get_jwt_identity()
    user_news_blogs =  Sports.query.filter_by(author_id=user_id).order_by(Sports.id.desc()).all()
    seliarized_blogs = seliarize_user_news__blogs(user_blogs=user_news_blogs, comments_model=SportsComments)
    return seliarized_blogs, 200


""" An endpoint to get all the Sports blogs written by admin """
@admin.route("/blogs/entertainment")
@cross_origin()
@jwt_required()
def get_all_user_entertainment_blogs():
    user_id = get_jwt_identity()
    user_news_blogs =  Entertainment.query.filter_by(author_id=user_id).order_by(Entertainment.id.desc()).all()
    seliarized_blogs = seliarize_user_news__blogs(user_blogs=user_news_blogs, comments_model=EntertainmentComments)
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
                    return jsonify({"success": f"A new {data['category']} Blog created successfully"}), 201
                
                elif data["category"] == "Business":
                    add_new_blog_data(Business, data, user_id)
                    return jsonify({"success": f"A new {data['category']} Blog created successfully"}), 201
                
                elif data["category"] == "Sports":
                    add_new_blog_data(Sports, data, user_id)
                    return jsonify({"success": f"A new {data['category']} Blog created successfully"}), 201
                
                elif data["category"] == "Entertainment":
                    add_new_blog_data(Entertainment, data, user_id)
                    return jsonify({"success": f"A new {data['category']} Blog created successfully"}), 201

        
        return jsonify({"failed": "All fields are required"}), 400


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
                    "commented_on": get_good_time(comment.date_created)
                }
            )
        seliarized.append({
             "title": blog.title,
             "slug": blog.slug,
             "image_id": blog.image_id,
             "body": blog.body,
             "published_on": get_good_time(blog.published_on),
             "comments": selialized_comments
        })
            
    return seliarized

        
          
            

