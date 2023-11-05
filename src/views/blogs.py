from flask import Blueprint, request, jsonify, Response
from src.models.database import User, News, Business, Sports, Entertainment

blogs = Blueprint("view", __name__, url_prefix="/")

@blogs.route("/")
def home_page():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("pages", 3, type=int)

    response = Response(response=jsonify({
            
            "News": get_brief_home_news(News,page, per_page),
            "Business": get_brief_home_news(Business, page, per_page),
            "Sports": get_brief_home_news(Sports, page, per_page),
            "Entertainment": get_brief_home_news(Entertainment, page, per_page)

    }), status=200, 
    mimetype="application/json")

    return response


""" A module to get all the news blogs in the database """
@blogs.route("/news")
def get_all_news_blogs():

        all_news = News.query.order_by(News.id.desc()).all()
        serialized = []
        for news in all_news:
                user = User.query.filter_by(id=news.author_id).first()
                serialized.append(
                        {
                                "title": news.title,
                                "slug": news.slug,
                                "image_id": news.image_id,
                                "body": news.body,
                                "date_created": news.date_created,
                                "published_on": news.published_on,
                                "author":f"{user.first_name} {user.last_name}"
                        }
                )
        return serialized, 200

""" A module to get all the business blogs in the database """
@blogs.route("/business")
def get_all_business_blogs():

          all_business = Business.query.order_by(Business.id.desc()).all()
          serialized = []
          for business in all_business:
                  user = User.query.filter_by(id=business.author_id).first()
                  serialized.append(
                          {
                                  "title": business.title,
                                  "slug": business.slug,
                                  "image_id": business.image_id,
                                  "body": business.body,
                                  "date_created": business.date_created,
                                  "published_on": business.published_on,
                                  "author":f"{user.first_name} {user.last_name}"
                          }
                  )
          return serialized, 200

""" A module to get all the Sports blogs in the database """
@blogs.route("/sports")
def get_all_sports_blogs():

          all_sports = Sports.query.order_by(Sports.id.desc()).all()
          serialized = []
          for sport in all_sports:
                  user = User.query.filter_by(id=sport.author_id).first()
                  serialized.append(
                          {
                                  "title": sport.title,
                                  "slug": sport.slug,
                                  "image_id": sport.image_id,
                                  "body": sport.body,
                                  "date_created": sport.date_created,
                                  "published_on": sport.published_on,
                                  "author":f"{user.first_name} {user.last_name}"
                          }
                  )
          return serialized, 200

""" A module to get all the entertainment blogs in the database """
@blogs.route("/entertainment")
def get_all_entertainment_blogs():

          all_entertainment = Entertainment.query.order_by(Entertainment.id.desc()).all()
          serialized = []
          for entertainment in all_entertainment:
                  user = User.query.filter_by(id=entertainment.author_id).first()
                  serialized.append(
                          {
                                  "title": entertainment.title,
                                  "slug": entertainment.slug,
                                  "image_id": entertainment.image_id,
                                  "body": entertainment.body,
                                  "date_created": entertainment.date_created,
                                  "published_on": entertainment.published_on,
                                  "author":f"{user.first_name} {user.last_name}"
                          }
                  )

          return serialized, 200

""" This is a function to query and return the brief news found in the home page """
def get_brief_home_news(model, page, per_page):
        blogs = model.query.order_by(model.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        serialized = []
        for blog in blogs:
                serialized.append({
                        "image_id": blog.image_id,
                        "author": f"{blog.first_name} {blog.last_name}",
                        "title": blog.title
                })
        
        return serialized

          
# """ A module to create  a blog """
# @blogs.route("/createblog", methods=["POST"])
# @login_required
# def create_a_new_blog():
        
#         data = request.get_json()
#         owner_id = current_user.id
#         if validate_blog_data(data):
#                 new_blog = Blogs(title=data["title"], category=data["category"], content=data["content"],owner_id=owner_id)
#                 db.session.add(new_blog)
#                 db.session.commit()
#                 return jsonify({"success": "Blog created successfully"}), 200

        
#         return jsonify({"failed": "All fields are required"}), 400


# def validate_blog_data(user_input):
        
#         if "title" in user_input and "category" in user_input and "content" in user_input:
#                 return True
        
#         return False

# """ A module to get all the blogs written by the current user """
# @blogs.route("/userblogs")
# @login_required
# def create_get_all_user_blogs():
#         print("Hello world")
#         blogs = Blogs.query.filter_by(owner_id=current_user.id).order_by(Blogs.id.desc()).all()
#         serialized = []
#         for blog in blogs:
#                 serialized.append({
#                     "title": blog.title,
#                     "category": blog.category,
#                     "content": blog.content,
#                     "date_created": blog.date_created
#                 })
          
#         return serialized, 200