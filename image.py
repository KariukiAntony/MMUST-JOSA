import os
import base64
import uuid
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image
from decouple import config
UPLOAD_DIRECTORY = config("UPLOAD_DIRECTORY")

""" An endpoint to create  a blog """
@admin.route("/createblog", methods=["POST"])
@cross_origin() 
# @jwt_required()
def create_a_new_blog():
        data = request.get_json()
        base64_string = data['image']

        base64_string = base64_string.split(",")[1]
        print("Hello world")
        image_data = BytesIO(base64.b64decode(base64_string))
        image = Image.open(image_data)

        result = upload(image_data)
        print("This is after execution")

        # Get the URL of the uploaded image
        image_url = result['secure_url']
        print(image_url)
    if not request.content_type == "application/json":
            return jsonify({"failed": "content_type must be application/json"}), 400
    if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)
    user_id = get_jwt_identity()
    data = request.get_json()
    base64_string = data['image']
    base64_string = base64_string.split(",")[1]
    image_data = BytesIO(base64.b64decode(base64_string))
    file = Image.open(image_data)
    filename = str(uuid.uuid1()) + ".png"
    file_path = os.path.join(UPLOAD_DIRECTORY, secure_filename(filename))
    file.save(file_path)
    
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