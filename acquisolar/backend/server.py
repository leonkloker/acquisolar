from flask import Flask, request, send_from_directory, jsonify, stream_with_context, send_file, Response
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
app.config['PREFERENCES'] = 'preferences' # where preferences are stored 

# Configure file uploads
files = UploadSet('files', ['pdf'])
configure_uploads(app, files)

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
    os.makedirs(app.config['UPLOADED_FILES_DEST'])

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

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
            preferences_dir = app.config['PREFERENCES']
            project_name = "project"
            copy_or_move = "move"
            classification.main(doc_dir, output_dir, preferences_dir, project_name, copy_or_move)
            

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

    ### FILENAME THAT CORRESPONDS TO WHAT FILE THE USER IS SEARCHING IN
    filename = request.json.get('file', '')
    print(filename)

    print('Received search query:', search_query)
    
    # Search the index and return a streaming response
    response_gen, sources = searchengine.query(search_query, app.config['UPLOADED_FILES_INDEX'])

    print(sources)

    # return strings, document name
    return response_gen


@app.route('/get-pdf/<filename>')
def get_pdf(filename):
    base_directory = app.config['STRUCTURED_DATA']
    json_file_path = os.path.join(base_directory, '/complete_file_metadata.json')
    
    # Load the JSON content
    with open(json_file_path, 'r') as file:
        documents = json.load(file)

    # Initialize document_folder_path as None
    document_folder_path = None

    # Loop through the documents to find a match
    for document in documents:
        if document["original_title"] == filename:
            document_folder_path = document["Document_folder_path"]
            break

    # Construct the full file path if document_folder_path is found
    if document_folder_path:
        pdf_directory = os.path.join(base_directory, document_folder_path)
        filepath = os.path.join(pdf_directory, filename)

        # If validation passes, send the requested PDF file
        return send_file(filepath)
    else:
        return "File not found", 404

@app.route('/get-folders', methods=['GET'])
def get_folders():
    folder_structure = calculate_folders()
    print('test')
    return jsonify(folder_structure)


# return folder structure and corresponding metadata
def calculate_folders():
    f = open(os.path.join(app.config['STRUCTURED_DATA'], 'global_directory_frontend.json'), 'r')
    folders = json.load(f)
    f.close()
    return folders

def calculate_metadata():
    f = open(os.path.join(app.config['STRUCTURED_DATA'], 'complete_file_metadata.json', 'r'))
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

    if folder_name and folder_name in folders:
        # Filter metadata for files in the correct folder
        filtered_metadata = [item for item in metadata if folder_name in item["Document_folder_path"].split('/')]
        if filtered_metadata:
            return jsonify(filtered_metadata)
        else:
            return jsonify({'status': 'error', 'message': 'No files found in the specified folder'}), 404
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
    # clean_environment()

    # 3001 for localhost, 80 for remote on AWS
    port = 3001

    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
