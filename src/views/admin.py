from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from ..models.database import db
from src.models.database import( User, News, Business, Sports, Entertainment,NewsComments,
BusinessComments, SportsComments, EntertainmentComments)
from flask_jwt_extended import get_jwt_identity, jwt_required
import requests

admin = Blueprint("admin", __name__,)


""" An endpoint to get the latest five news blogs """
@admin.route("/latest")
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
                    "published_on": blog.published_on
            })
    
    return serialized

""" An endpoint to update the blogs in the admin dashboard """
@admin.route("/News/latest/update/<string:image_id>", methods = ["POST"])
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
@admin.route("/News/latest/delete/<string:image_id>")
@cross_origin()
def delete_blog_in_latest(image_id):
      blog = News.query.filter_by(image_id=image_id).first()
      if blog:
            db.session.delete(blog)
            db.session.commit()
            return jsonify({"success": "Image deleted succesfully"}), 204
      
      return {"error": f"Image with id {image_id} not found"}, 404


""" An endpoint to give all the News blogs written by admin """
@admin.route("/blogs/News")
@cross_origin()
@jwt_required()
def get_all_user_blogs():
    user_id = get_jwt_identity()
    print(user_id)
    user_news_blogs =  News.query.filter_by(author_id=user_id).order_by(News.id.desc()).all()
    seliarized_blogs = seliarize_user_blogs(user_blogs=user_news_blogs)
    return seliarized_blogs, 200


def seliarize_user_blogs(user_blogs):
    seliarized = []
    for blog in user_blogs:
        selialized_comments = []
        for comment in blog.comments:
            selialized_comments.append(
                {
                    "content": comment.content,
                    "is_is_anonymous": comment.is_anonymous
                }
            )
        seliarized.append({
             "title": blog.title,
             "slug": blog.slug,
             "image_id": blog.image_id,
             "body": blog.body,
             "published_on": blog.published_on,
             "comments": selialized_comments
        })
            
    return seliarized

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
def add_new_blog_data(model, data, author_id):
        new_blog = model(title=data["title"],
                          slug=data["slug"], 
                          image_id=data["image_id"],
                          body=data["body"],
                          author_id = author_id
                          ) 
        db.session.add(new_blog)
        db.session.commit()

""" A function to validate blogs info """
def validate_blog_data(user_input):
        
        if "title" in user_input and "slug" in user_input and "body" \
            in user_input and "image_id" in user_input \
                  and "category" in user_input:
                return True
        
        return False

        
          
            

