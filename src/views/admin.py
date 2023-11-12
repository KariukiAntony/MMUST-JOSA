from flask import Blueprint, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

admin = Blueprint("admin", __name__,)

@admin.route("/")
def admin_index():
    return jsonify({"message": "Hello world"}),200

""" An endpoint to get the latest five news blogs """
# @admin.route("/latest")
# @cross_origin()
# @jwt_required()
# def get_latest_five_news_blogs():
#     user_id = get_jwt_identity()
#     latest_blogs = News.query.filter_by(author_id=user_id).order_by(News.id.desc()).paginate(page=1, per_page=5, error_out=False)
#     serialized = []
#     for blog in latest_blogs:
#             serialized.append({
#                     "image_id": blog.image_id,
#                     "title": blog.title,
#                     "published_on": blog.published_on
#             })
    
#     return serialized


# @admin.route("/latest/delete/<string:image_id>")
# @cross_origin()
# def delete_image_in_latest(image_id):
#       blog = News.query.filter_by(image_id=image_id).first()
#       if blog:
#             db.session.delete(blog)
#             db.session.commit()
#             return jsonify({"success": "Image deleted succesfully"}), 204
      
#       return {"error": f"Image with id {image_id} not found"}, 404

# """ An endpoint to give all the News blogs written by a user """
# @admin.route("/blogs/News")
# @cross_origin()
# @jwt_required()
# def get_all_user_blogs():
#     user_id = get_jwt_identity()
#     user_news_blogs =  News.query.filter_by(author_id=user_id).order_by(News.id.desc()).all()
#     seliarized_blogs = seliarize_user_blogs(user_blogs=user_news_blogs)


# def seliarize_user_blogs(user_blogs):
#     seliarized = []
#     for blog in user_blogs:
#         selialized_comments = []
#         for comment in blog.comment:
#             selialized_comments.append(
#                 {
#                     "content": comment.content,
#                     "is_is_anonymous": comment.is_anonymous
#                 }
#             )
#         seliarized.append({
#              "title": blog.title,
#              "slug": blog.slug,
#              "image_id": blog.image_id,
#              "body": blog.body,
#              "published_on": blog.published_on,
#              "comments": selialized_comments
#         })
            
#     return seliarized

        
          
            

