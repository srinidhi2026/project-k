from flask import Flask, render_template, redirect, url_for
from upload_handler import upload_image
from process_handler import process_image
from curve_completion_handler import curve_completion
from visualize_handler1 import visualize_data
from visualize_handler2 import visualize_csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'supersecretkey'

@app.route('/')
def landing():
    return render_template('landing.html')

# Register blueprints
app.register_blueprint(upload_image, url_prefix='/upload_image')
app.register_blueprint(process_image, url_prefix='/process_image')
app.register_blueprint(curve_completion, url_prefix='/curve_completion')
app.register_blueprint(visualize_data, url_prefix='/visualize_data')
app.register_blueprint(visualize_csv, url_prefix='/visualize_data')

if __name__ == '__main__':
    app.run(debug=True)
