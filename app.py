from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
import main
from main import process_image_model
from PIL import Image

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload and processed folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('show_image', filename=filename))
    return "File type not allowed"

@app.route('/uploads/<filename>')
def show_image(filename):
    return render_template('display_image.html', filename=filename, folder='uploads')

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

@app.route('/process', methods=['POST'])
def process_image():
    filename = request.form['filename']
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)

    # Placeholder for processing function
    process_placeholder(input_path, processed_path)

    return redirect(url_for('show_processed_image', filename=filename))

def process_placeholder(input_path, output_path):
    # Example function: simply copy the input file to processed folder
    process_img, text, score = process_image_model(input_path)
    for r in process_img:
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])
        im.show()
        im.save(output_path)
    return text, score

@app.route('/processed/<filename>')
def show_processed_image(filename):
    return render_template('display_image.html', filename=filename, folder='processed')

if __name__ == '__main__':
    app.run(debug=True)
