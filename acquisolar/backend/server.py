from flask import Flask, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import subprocess

import searchengine

app = Flask(__name__, static_folder="../frontend/build", static_url_path='/')

# Configuration for file uploads
app.config['UPLOADED_FILES_DEST'] = 'documents'  # where files are stored
app.config['UPLOADED_FILES_INDEX'] = 'index_storage'  # where files are indexed
app.config['UPLOADED_FILES_ALLOW'] = ['pdf']  # allowed file types

files = UploadSet('files', ['pdf'])
configure_uploads(app, files)
#patch_request_class(app)  # to limit upload size; default is 16MB

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
    os.makedirs(app.config['UPLOADED_FILES_DEST'])

def call_python(file):
    try:
        result = subprocess.run(['python3', file], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e.stderr}")
        return None

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

@app.route('/search', methods=['POST'])
def search():
    search_query = request.json.get('query', '')
    print('Received search query:', search_query)
    
    # Search the index
    response = searchengine.query(search_query, app.config['UPLOADED_FILES_INDEX'])

    return jsonify(response=str(response))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = 3000
    app.run(port=port, debug=True)