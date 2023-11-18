from io import BytesIO
import base64
from PIL import Image
import uuid
import os
from werkzeug.utils import secure_filename
from .admin import admin, request, jwt_required, get_jwt_identity, UPLOAD_DIRECTORY
from flask import make_response, jsonify
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.database import User, db
from .uploads import send_image_to_cloudinary

""" An endpoint to update admin profile """
@admin.route("/update/profile", methods=["PUT"])
@cross_origin()
@jwt_required()
def update_admin_profile():
    admin_id = get_jwt_identity()
    data = request.get_json()
    admin = User.query.filter_by(id=admin_id).first()

    if "image" in data:
        base64_string = data['image']
        base64_string = base64_string.split(",")[1]
        image_data = BytesIO(base64.b64decode(base64_string))
        file = Image.open(image_data)
        filename = str(uuid.uuid1()) + ".png"
        file_path = os.path.join(UPLOAD_DIRECTORY, secure_filename(filename))
        file.save(file_path)
        admin.image_id = send_image_to_cloudinary(filename=filename)
        print(f"{filename} send to cloudinary")

    # if "old_password" in data and "new_password" in data:
    #     if not update__admin_login_password(admin_id, data["oldPassword"], data["newPassword"]):
    #         return jsonify({"error": "invalid password. Try again"}), 401

    if "first_name" in data:
        admin.first_name = data["first_name"]

    if "last_name" in data:
        admin.last_name = data["last_name"]

    if "contact" in data:
        admin.contact = data["contact"]

    db.session.commit()
    return make_response({"success": "Profile data updated successfully"}), 202


""" An endpoint to get  admin profile info """
@admin.route("/get/profile")
@cross_origin()
@jwt_required()
def get_admin_profile_info():
    admin_id = get_jwt_identity()
    admin = User.query.filter_by(id=admin_id).first()
    return jsonify({
        "first_name": admin.first_name,
        "last_name": admin.last_name,
        "image_id": admin.image_id,
        "contact": admin.contact,

    }), 200

""" A function to update user login password """
def update__admin_login_password(user_id: str, oldpassword: str, newpassword:str) -> bool:
    admin = User.query.filter_by(id=user_id).first()
    if check_password_hash(admin.password, oldpassword):
        news_pass = generate_password_hash(newpassword)
        admin.password = news_pass
        db.session.commit()
        return True

    
    return False



