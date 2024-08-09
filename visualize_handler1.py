from flask import Blueprint, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

visualize_data = Blueprint('visualize_data', __name__)

@visualize_data.route('/')
def visualize_image_page():
    return render_template('visualize_data.html')

@visualize_data.route('/upload', methods=['POST'])
def upload_image():
    data_type = request.form['data_type']
    
    if data_type == 'image':
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        # Save the uploaded image
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)

        # Load and process the image
        image = cv2.imread(file_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Normalization logic
        b, g, r = cv2.split(image_rgb)
        min_value = 0
        max_value = 1
        norm_type = cv2.NORM_MINMAX

        b_normalized = cv2.normalize(b.astype("float"), None, min_value, max_value, norm_type)
        g_normalized = cv2.normalize(g.astype("float"), None, min_value, max_value, norm_type)
        r_normalized = cv2.normalize(r.astype("float"), None, min_value, max_value, norm_type)

        normalized_image = cv2.merge((b_normalized, g_normalized, r_normalized))

        # Save the normalized image
        normalized_image_path = os.path.join('static/uploads', 'normalized_' + file.filename)
        plt.figure(figsize=(15, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(image_rgb)
        plt.title("Original Image")
        plt.subplot(1, 2, 2)
        plt.imshow(normalized_image)
        plt.title("Normalized Image")
        plt.savefig(normalized_image_path)
        plt.close()

        return render_template('visualize_result.html', original=file.filename, normalized='normalized_' + file.filename)
    
    elif data_type == 'csv':
        # Handle CSV file processing and visualization
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        # Save the uploaded CSV file
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)

        # Process the CSV file (as described in your code)
        path_XYs = read_csv(file_path)
        
        # Generate the plot
        plot_transformed(path_XYs)

        # Save the plot image
        plot_image_path = os.path.join('static/uploads', 'plot_' + file.filename.replace('.csv', '.png'))
        plt.savefig(plot_image_path)
        plt.close()

        return render_template('visualize_result.html', original=file.filename, normalized='plot_' + file.filename.replace('.csv', '.png'))
    
    else:
        return "Invalid data type", 400

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def plot_transformed(paths_XYs):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            # Flip sidewise (mirror horizontally)
            XY_flipped = XY.copy()
            XY_flipped[:, 0] = -XY_flipped[:, 0]
            
            # Rotate 180 degrees
            XY_rotated = -XY_flipped
            
            ax.plot(XY_rotated[:, 0], XY_rotated[:, 1], c=c, linewidth=2)
    
    ax.set_aspect('equal')
    plt.show()
