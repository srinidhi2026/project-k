import os
import cv2
import numpy as np
from flask import Blueprint, request, render_template, flash, redirect
from werkzeug.utils import secure_filename

# Blueprint setup
process_image = Blueprint('process_image', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@process_image.route('/', methods=['GET', 'POST'])
def process():
    """Handle image upload and processing."""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Load and process the image
            img = cv2.imread(filepath)
            process_type = request.form['process_type']
            processed_image_path = None

            if process_type == 'flip_horizontal':
                # Apply horizontal flipping
                processed_image = cv2.flip(img, 1)
                processed_image_path = os.path.join(UPLOAD_FOLDER, 'horizontal_flip_' + filename)
                cv2.imwrite(processed_image_path, processed_image)
                
            elif process_type == 'flip_vertical':
                # Apply vertical flipping
                processed_image = cv2.flip(img, 0)
                processed_image_path = os.path.join(UPLOAD_FOLDER, 'vertical_flip_' + filename)
                cv2.imwrite(processed_image_path, processed_image)

            elif process_type == 'symmetry':
                # Check symmetry
                vertical_symmetry = check_symmetry(img, axis='vertical')
                horizontal_symmetry = check_symmetry(img, axis='horizontal')
                return render_template('process_image.html', 
                                       vertical_symmetry=vertical_symmetry, 
                                       horizontal_symmetry=horizontal_symmetry)

            return render_template('process_image.html', processed_image=processed_image_path)

    return render_template('process_image.html')

def check_symmetry(image, axis='vertical'):
    """Check image symmetry along the specified axis."""
    h, w = image.shape[:2]
    
    if axis == 'vertical':
        if w % 2 != 0:
            w -= 1
        left = image[:, :w // 2]
        right = image[:, w // 2:w]
        right_flipped = np.fliplr(right)

        return np.allclose(left, right_flipped, atol=5)
    
    elif axis == 'horizontal':
        if h % 2 != 0:
            h -= 1
        top = image[:h // 2, :]
        bottom = image[h // 2:h, :]
        bottom_flipped = np.flipud(bottom)

        return np.allclose(top, bottom_flipped, atol=5)
