from flask import Blueprint, request, jsonify
from src.models.database import User, News, Business, Sports, Entertainment

views = Blueprint("view", __name__, url_prefix="/api/views")

""" A module to get all the news blogs in the database """
@views.route("/news")
def get_all_news_blogs():

          all_news = News.query.order_by(News.id.desc()).all()
          serialized = []
          for news in all_news:
                  user = User.query.filter_by(id=news.author_id).first()
                  serialized.append(
                          {
                                  "title": news.title,
                                  "category": news.slug,
                                  "content": news.body,
                                  "date_created": news.date_created,
                                  "published_on": news.published_on,
                                  "author":f"{user.first_name} {user.last_name}"
                          }
                  )
          return serialized, 200

""" A module to get all the business blogs in the database """
@views.route("/business")
def get_all_business_blogs():

          all_business = Business.query.order_by(Business.id.desc()).all()
          serialized = []
          for business in all_business:
                  user = User.query.filter_by(id=business.author_id).first()
                  serialized.append(
                          {
                                  "title": business.title,
                                  "category": business.slug,
                                  "content": business.body,
                                  "date_created": business.date_created,
                                  "published_on": business.published_on,
                                  "author":f"{user.first_name} {user.last_name}"
                          }
                  )
          return serialized, 200

""" A module to get all the Sports blogs in the database """
@views.route("/sports")
def get_all_sports_blogs():

          all_sports = Sports.query.order_by(Sports.id.desc()).all()
          serialized = []
          for sport in all_sports:
                  user = User.query.filter_by(id=sport.author_id).first()
                  serialized.append(
                          {
                                  "title": sport.title,
                                  "category": sport.slug,
                                  "content": sport.body,
                                  "date_created": sport.date_created,
                                  "published_on": sport.published_on,
                                  "author":f"{user.first_name} {user.last_name}"
                          }
                  )
          return serialized, 200

""" A module to get all the entertainment blogs in the database """
@views.route("/entertainment")
def get_all_entertainment_blogs():

          all_entertainment = Entertainment.query.order_by(Entertainment.id.desc()).all()
          serialized = []
          for entertainment in all_entertainment:
                  user = User.query.filter_by(id=entertainment.author_id).first()
                  serialized.append(
                          {
                                  "title": entertainment.title,
                                  "category": entertainment.slug,
                                  "content": entertainment.body,
                                  "date_created": entertainment.date_created,
                                  "published_on": entertainment.published_on,
                                  "author":f"{user.first_name} {user.last_name}"
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