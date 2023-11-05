from flask import Blueprint, request, jsonify, Response, json
from src.models.database import User, News, Business, Sports, Entertainment

blogs = Blueprint("view", __name__, url_prefix="/")

@blogs.route("/")
def home_page():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("pages", 3, type=int)

    response = Response(response=json.dumps({
            
            "News": get_brief_home_news(News,page, per_page),
            "Business": get_brief_home_news(Business, page, per_page),
            "Sports": get_brief_home_news(Sports, page, per_page),
            "Entertainment": get_brief_home_news(Entertainment, page, per_page)

    }), status=200, 
    mimetype="application/json")

    return response


""" An endpoint to get all the news blogs in the database """
@blogs.route("/news")
def get_all_news_blogs():

        all_news = get_all_blogs_with_category(model=News)
        return all_news, 200

""" An endpoint to get all the business blogs in the database """
@blogs.route("/business")
def get_all_business_blogs():

        all_business = get_all_blogs_with_category(model=Business)

        return  all_business, 200


""" An endpoint to get all the Sports blogs in the database """
@blogs.route("/sports")
def get_all_sports_blogs():

        all_sports = get_all_blogs_with_category(model=Sports)
        
        return all_sports, 200


""" An endpoint to get all the entertainment blogs in the database """
@blogs.route("/entertainment")
def get_all_entertainment_blogs():

        all_entertainment = get_all_blogs_with_category(model=Entertainment)

        return all_entertainment, 200

""" An endpoint to get the data associated with and image """
@blogs.route('/blogs/<string:category>/<string:image_id>')
def get_all_info(category, image_id): 
        error_mesage = {"error": "The category deos not exist"}          
        if category == "News":
                data = get_blog_info (News, image_id)
                if data:
                       return data, 200
                return jsonify(error_mesage)
        elif category == "Business":
                data = get_blog_info (Business, image_id)
                if data:
                       return data, 200
                return jsonify(error_mesage)
        
        elif category == "Sports":
                data = get_blog_info (Sports, image_id)
                if data:
                       return data, 200
                return jsonify(error_mesage)

        elif category == "Entertainment":
                return (get_blog_info (Entertainment, image_id))



""" This is a function to query and return all 
    the blogs associated with a certain category   """
def get_all_blogs_with_category(model)-> list:
        all_blogs = model.query.order_by(model.id.desc()).all()
        serialized = []
        for blog in all_blogs:
                serialized.append(
                        {
                                "title": blog.title,
                                "image_id": blog.image_id,
                                "published_on": blog.published_on,
                        }
                )
        
        return serialized

""" This is a function to query and return the 
    brief news found in the home page         """
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

""" A function to get the all the data of an blog  """

def get_blog_info (category, image_id):
        data = category.query.filter_by(image_id=image_id).first()
        print(data)
        author = User.query.filter_by(id=data.id).first()
        return jsonify({
        "title": data.title,
        "author": f"{author.first_name} {author.last_name}",
        "published on": data.published_on,
        "image_id": data.image_id
})



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