from decouple import config

UPLOAD_DIRECTORY = config("UPLOAD_DIRECTORY")

import cloudinary
import cloudinary.uploader
          
cloudinary.config( 
  cloud_name = "dqfjiip8v", 
  api_key = "826449421191762", 
  api_secret = "oNHvF0SzT4eTB1F6vdefIHH3gAg" 
)


def send_image_to_cloudinary(filename):
    image_path = f"{UPLOAD_DIRECTORY}{filename}"
    response = cloudinary.uploader.upload(image_path,  public_id = "MMUSTJOSA")
    public_url = response['secure_url']
    return public_url
