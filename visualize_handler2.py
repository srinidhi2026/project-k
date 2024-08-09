from flask import Blueprint, render_template, request, redirect, url_for, send_file
import os
import numpy as np
import matplotlib.pyplot as plt

visualize_csv = Blueprint('visualize_csv', __name__)

@visualize_csv.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        # Save the uploaded CSV file
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)

        # Process the CSV file
        path_XYs = read_csv(file_path)
        plot_path = plot_transformed(path_XYs, file.filename)

        # Redirect to a route that opens the image in a new tab
        return redirect(url_for('visualize_csv.display_image', filename=os.path.basename(plot_path)))

    # For GET requests, just render the file upload form
    return render_template('visualize_data.html')

@visualize_csv.route('/display_image/<filename>')
def display_image(filename):
    file_path = os.path.join('static/uploads', filename)
    return send_file(file_path, as_attachment=False)

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

def plot_transformed(paths_XYs, filename):
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

    # Save the plot image
    plot_path = os.path.join('static/uploads', 'plot_' + filename.split('.')[0] + '.png')
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path
