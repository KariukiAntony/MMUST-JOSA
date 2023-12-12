from decouple import config
import cloudinary
import cloudinary.uploader
import logging
import tinify

tinify.key = config("TINIFY_API_KEY")
UPLOAD_DIRECTORY = config("UPLOAD_DIRECTORY")  

cloudinary.config( 
  cloud_name = config("cloudname"), 
  api_key =  config("api_key"), 
  api_secret = config("api_secret")
)


def send_image_to_cloudinary(filename):
    image_path = f"{UPLOAD_DIRECTORY}{filename}"
    response = cloudinary.uploader.upload(image_path,  public_id = "MMUSTJOSA")
    public_url = response['secure_url']
    return public_url


def compress_image_using_tinify(filename):
    image_path = f"{UPLOAD_DIRECTORY}{filename}"
    
    try:
        source = tinify.from_file(image_path)
        source.to_file(image_path)
        print("Image compressed successfully")
    
    except Exception as e:
        logging.error(f"An error has occured whole compressing the image: {str(e)}")
