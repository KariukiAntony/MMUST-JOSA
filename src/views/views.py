from flask import Blueprint, request, jsonify
from src.models.database import Blogs, User, db
from flask_login import login_required, current_user

views = Blueprint("view", __name__, url_prefix="/api/views")

""" A module to get all the blogs in the database """
@views.route("/blogs")
@login_required
def get_all_blogs():

          blogs = Blogs.query.order_by(Blogs.id.desc()).all()
          serialized = []
          for blog in blogs:
                  user = User.query.filter_by(id=blog.owner_id).first()
                  serialized.append(
                          {
                                  "title": blog.title,
                                  "category": blog.category,
                                  "content": blog.content,
                                  "date_created": blog.date_created,
                                  "first_name":user.first_name,
                                  "last_name": user.last_name
                          }
                  )

          return serialized, 200
          
""" A module to create  a blog """
@views.route("/createblog", methods=["POST"])
@login_required
def create_a_new_blog():
        
        data = request.get_json()
        owner_id = current_user.id
        if validate_blog_data(data):
                new_blog = Blogs(title=data["title"], category=data["category"], content=data["content"],owner_id=owner_id)
                db.session.add(new_blog)
                db.session.commit()
                return jsonify({"success": "Blog created successfully"}), 200

        
        return jsonify({"failed": "All fields are required"}), 400


def validate_blog_data(user_input):
        
        if "title" in user_input and "category" in user_input and "content" in user_input:
                return True
        
        return False

""" A module to get all the blogs written by the current user """
@views.route("/userblogs")
@login_required
def create_get_all_user_blogs():
        print("Hello world")
        blogs = Blogs.query.filter_by(owner_id=current_user.id).order_by(Blogs.id.desc()).all()
        serialized = []
        for blog in blogs:
                serialized.append({
                    "title": blog.title,
                    "category": blog.category,
                    "content": blog.content,
                    "date_created": blog.date_created
                })
          
        return serialized, 200