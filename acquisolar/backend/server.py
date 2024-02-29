from flask import Flask, request, send_from_directory, jsonify, stream_with_context, send_file
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import subprocess
import shutil

import classification
import searchengine
import Convert_directory

# Create the Flask app
app = Flask(__name__, static_folder = "../frontend/build", static_url_path='/')

# Enable cross-origin resource sharing
CORS(app)

# Configuration for file uploads
app.config['UPLOADED_FILES_DEST'] = 'documents'  # where files are stored
app.config['UPLOADED_FILES_INDEX'] = 'index_storage'  # where files are indexed
app.config['UPLOADED_FILES_ALLOW'] = ['pdf']  # allowed file types
app.config['STRUCTURED_DATA'] = 'structured_data'  # where structured data is stored

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

            # create directory for frontend
            Convert_directory.convert_directory_structure()
            

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

@app.route('/get-pdf/<filename>')
def get_pdf(filename):
    # Define the directory where your PDF files are stored
    pdf_directory = './structured_data/TESTSOLAR/Unclassified'
    filepath ='./structured_data/TESTSOLAR/Unclassified'
    
    # Construct the full file path
    filepath = os.path.join(pdf_directory, filename)
    
    # If validation passes, send the requested PDF file
    return send_file(filepath)

@app.route('/get-folders', methods=['GET'])
def get_folders():
    folder_structure = calculate_folders()
    print('test')
    return jsonify(folder_structure)


# return folder structure and corresponding metadata
def calculate_folders():
    f = open('./structured_data/global_directory_frontend.json', 'r')
    folders = json.load(f)
    f.close()
    return folders

def calculate_metadata():
    f = open('./structured_data/complete_file_metadata.json', 'r')
    metadata = json.load(f)
    f.close()
    return metadata


# Get the contents of a folder
@app.route('/get-folder-contents', methods=['POST'])
def get_folder_contents():
    folders = calculate_folders()
    metadata = calculate_metadata()
    data = request.json
    folder_name = data.get('folderName')
    print('HIII')
    if folder_name and folder_name in folders:
        print(metadata)
        return jsonify(metadata)
        #return jsonify({'status': 'success', 'data': folders_data[folder_name]})
    else:
        return jsonify({'status': 'error', 'message': 'Folder not found'}), 404


# Serve the frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def clean_environment():
    if os.path.exists(app.config['UPLOADED_FILES_DEST']):
        shutil.rmtree(app.config['UPLOADED_FILES_DEST'])
    if os.path.exists(app.config['STRUCTURED_DATA']):
        shutil.rmtree(app.config['STRUCTURED_DATA'])
    if os.path.exists(app.config['UPLOADED_FILES_INDEX']):
        shutil.rmtree(app.config['UPLOADED_FILES_INDEX'])
    if os.path.exists('classification_testing'):
        shutil.rmtree('classification_testing') 

if __name__ == '__main__':
    # Clean the environment
    clean_environment()

    # 3001 for localhost, 80 for remote on AWS
    port = 3001

    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
