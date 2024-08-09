from flask import Blueprint, render_template

upload_image = Blueprint('upload_image', __name__)

@upload_image.route('/')
def upload_image_page():
    return render_template('upload_image.html')

@upload_image.route('/upload', methods=['POST'])
def handle_upload():
    # Handle the upload logic here
    return "Upload successful!"
