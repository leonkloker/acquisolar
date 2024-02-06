from flask import Flask, request, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import sys 

# add the path to the sys path
sys.path.append('..')

# import custom modules
import src.searchengine as searchengine

# Create the application instance
app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Needed for session management and flashing messages

# Configuration
UPLOAD_FOLDER = '../data/orig'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024  # Limit uploads to 128MB per file

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file's extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# endpoint to upload files
@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle the file upload and save files to the UPLOAD_FOLDER."""
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)

    files = request.files.getlist('files[]')

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    flash('File(s) successfully uploaded')
    return redirect(url_for('upload_form'))

# sample endpoint
@app.route('/', methods=['GET'])
def api():
    return jsonify({'message': 'Welcome to AcquiSolar'})

# endpoint to query the search engine
@app.route('/query', methods=['POST'])
def query():
    query_text = request.json['query']
    response = searchengine.query(query_text)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
