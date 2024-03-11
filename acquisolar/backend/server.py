from flask import Flask, request, send_from_directory, jsonify, stream_with_context, send_file, Response
from flask_cors import CORS, cross_origin
import json
import os
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import subprocess
import shutil

import classification
import searchengine
import Convert_directory
import Metadata_changes

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

    # Return the streaming response
    def generate():
        for word in response_gen:
            yield word
        for source in sources:
            yield source

    # return strings, document name
    return response_gen

@app.route('/renameFile', methods=['POST'])
@cross_origin()
def renameFile():
    # Ensure there is JSON data and extract it
    if not request.json:
        return jsonify({'error': 'Missing request data'}), 400

    data = request.get_json()
    originalFilename = data.get('originalFilename')
    newFilename = data.get('newFilename')

    if not originalFilename or not newFilename:
        return jsonify({'error': 'Missing filenames in the request'}), 400


    try:
        Metadata_changes.rename_file(originalFilename, newFilename)
        return jsonify({'message': 'File renamed successfully'}), 200
    except:
        return jsonify({'error': 'Original file not found'}), 404


@app.route('/get-pdf/<filename>')
def get_pdf(filename):
    json_file_path = 'structured_data/global_directory.json'
    
    # Load the JSON content
    with open(json_file_path, 'r') as file:
        directories = json.load(file)

    # Function to find a directory or file by ID
    def find_by_id(d_id):
        return next((item for item in directories if item["id"] == d_id), None)
    
    # Function to construct the path for a given file
    def construct_path(file_item):
        path = []
        current_item = file_item
        while current_item["parent_id"] is not None:
            current_item = find_by_id(current_item["parent_id"])
            path.insert(0, current_item["name"])
        return "/".join(path)

    # Find the file in the directory structure
    file_item = next((item for item in directories if item["name"] == filename), None)
    
    # If file is not found, return an error
    if not file_item:
        return jsonify(error="File not found"), 404

    # Construct and return the path
    path = construct_path(file_item)
    path = os.path.join('./structured_data', construct_path(file_item), filename)

    print('hi' + path)
    
# Check if file exists
    if not os.path.isfile(path):
        return jsonify(error="File does not exist on server"), 404

    # Send the file
    return send_file(path)

@app.route('/get-folders', methods=['GET'])
def get_folders():
    folder_structure = calculate_folders()
    print('test')
    return jsonify(folder_structure)


# return folder structure and corresponding metadata
def calculate_folders():

    with open('./structured_data/global_directory.json', 'r') as file:
        data = json.load(file)
    
    folders = {}
    
    directory_entries = [item for item in data if item['type'] == 'directory' and item['parent_id'] == 1]
    
    for directory in directory_entries:
        files = [item['name'] for item in data if item['type'] == 'file' and item['parent_id'] == directory['id']]
        
        folders[directory['name']] = files
    
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
    clean_environment()

    # 3001 for localhost, 80 for remote on AWS
    port = 3001

    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
