from flask import Flask, request, send_from_directory, jsonify, stream_with_context
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import subprocess

import classification
import searchengine

# Create the Flask app
app = Flask(__name__, static_folder = "../frontend/build", static_url_path='/')

# Enable CORS only on AWS
CORS(app)

# Configuration for file uploads
app.config['UPLOADED_FILES_DEST'] = 'documents'  # where files are stored
app.config['UPLOADED_FILES_INDEX'] = 'index_storage'  # where files are indexed
app.config['UPLOADED_FILES_ALLOW'] = ['pdf']  # allowed file types
app.config['STRUCTURED_DATA'] = 'data_structured'  # where structured data is stored

# Configure file uploads
files = UploadSet('files', ['pdf'])
configure_uploads(app, files)

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
    os.makedirs(app.config['UPLOADED_FILES_DEST'])

# File upload endpoint
@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
        os.makedirs(app.config['UPLOADED_FILES_DEST'])
    
    if 'files' in request.files:
        filenames = []
        for file in request.files.getlist('files'):
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'pdf':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOADED_FILES_DEST'], filename))
                filenames.append(filename)
        if filenames:
            print('Uploaded files:', filenames)

            # Classify the uploaded files
            doc_dir = app.config['UPLOADED_FILES_DEST']
            output_dir = app.config['STRUCTURED_DATA']
            classification.main(doc_dir, output_dir)

            # Index the uploaded files
            index_dir = app.config['UPLOADED_FILES_INDEX']
            searchengine.index(output_dir, index_dir=index_dir)

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
    response_gen, sources = searchengine.query(search_query, app.config['UPLOADED_FILES_INDEX'])

    # Return the streaming response
    for word in response_gen:
        print(word, end='', flush=True)

    for source in sources:
        print(source)

    # return strings, document name
    return stream_with_context(response_gen)

# Serve the frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # 3001 for localhost, 80 for remote on AWS
    port = 3001
    app.run(host='0.0.0.0', port=port, debug=True)
