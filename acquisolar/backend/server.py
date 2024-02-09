from flask import Flask, request, send_from_directory, jsonify, stream_with_context
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import subprocess

import searchengine

# Create the Flask app
app = Flask(__name__, static_folder="../frontend/build", static_url_path='/')

# Enable CORS only on AWS
#CORS(app)

# Configuration for file uploads
app.config['UPLOADED_FILES_DEST'] = 'documents'  # where files are stored
app.config['UPLOADED_FILES_INDEX'] = 'index_storage'  # where files are indexed
app.config['UPLOADED_FILES_ALLOW'] = ['pdf']  # allowed file types

# Configure file uploads
files = UploadSet('files', ['pdf'])
configure_uploads(app, files)

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
    os.makedirs(app.config['UPLOADED_FILES_DEST'])

# File upload endpoint
@app.route('/upload', methods=['POST'])
def upload():
    if 'files' in request.files:
        filenames = []
        for file in request.files.getlist('files'):
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'pdf':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOADED_FILES_DEST'], filename))
                filenames.append(filename)
        if filenames:
            print('Uploaded files:', filenames)

            # Index the uploaded files
            doc_dir = app.config['UPLOADED_FILES_DEST']
            index_dir = app.config['UPLOADED_FILES_INDEX']
            searchengine.index(doc_dir, index_dir=index_dir)

            return jsonify(message="File(s) uploaded successfully!", filenames=filenames)
        else:
            return jsonify(error="No valid PDF files selected!"), 400
    return jsonify(error="No files part in request!"), 400

# Search endpoint
@app.route('/search', methods=['POST'])
def search():
    search_query = request.json.get('query', '')
    print('Received search query:', search_query)
    
    # Search the index and return a streaming response
    response = searchengine.query(search_query, app.config['UPLOADED_FILES_INDEX'])

    # Return the streaming response
    for word in response:
        print(word, end='', flush=True)
    return stream_with_context(response)

# Serve the frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # 3000 for localhost, 80 for remote on AWS
    port = 3000
    app.run(host='0.0.0.0', port=port, debug=True)
