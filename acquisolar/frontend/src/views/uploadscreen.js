import Header from './viewcomponents/header';
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Document, Page, pdfjs } from 'react-pdf';
import FileList from './viewcomponents/filelist';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import uploadIcon from '../icons/upload.png';
import loadingIcon from '../icons/loadingIcon.svg';
import stylesLoad from '../styles/uploadscreen.css'

// Set the workerSrc for pdfjs
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

// url of aws server and port 80
// change to 'http://localhost:3001' for localhost
// or http://54.90.226.66:80' for aws
// Changed this variable name or causes issues with other parts of code
const URLServer = 'http://localhost:3001'


const Upload = () => {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [fileNames, setFileNames] = useState([]);
  const [isUploading, setIsUploading] = useState(false); // New state for tracking upload status
  const [hasUploaded, setHasUploaded] = useState(false)

  
    const onDrop = useCallback((acceptedFiles) => {
      // Prevents duplicates from being uploaded (based on filename atm)
      const filteredFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
      setFiles((prevFiles) => [...prevFiles, ...filteredFiles]);
  
  
      // Filenames that are displayed when file is uploaded
      setFileNames((prevFiles) => {
        const newFileNames = filteredFiles.map((file) => file.name);
        const existingFileNames = new Set(prevFiles);
        const uniqueNewFileNames = newFileNames.filter((fileName) => !existingFileNames.has(fileName));
        return [...prevFiles, ...uniqueNewFileNames];
      });
    },);
  
    const removeFile = (fileName, event) => {
      event.stopPropagation(); // Prevent the event from bubbling up to parent elements
    
      setFiles((prevFiles) => prevFiles.filter((file) => file.name !== fileName));
      setFileNames((prevFileNames) => prevFileNames.filter((name) => name !== fileName));
    };
  
    const { getRootProps, getInputProps } = useDropzone({
      // Only allows pdfs
      accept: 'application/pdf',
      onDrop,
    });
  
    const uploadFilesToServer = async () => {
      if (files.length === 0) {
        alert('Please submit a file.');
        return;
      }

      setIsUploading(true); // Start uploading

      const formData = new FormData();
      
      files.forEach((file) => {
        formData.append('files', file);
      });
  
      try {
        // Use axios or fetch here to upload the files
        // Example with fetch:
        const response = await fetch(URLServer + '/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          console.log('Files successfully uploaded');
        } else {
          console.error('Upload failed', response);
        }
      } catch (error) {
        console.error('Error uploading files', error);
      } finally {
        setHasUploaded(true);
        setIsUploading(false);
      }
    };

    const navigateFolders = () => {
      if(!isUploading && hasUploaded) {
        navigate('/folders'); 
      }
    }
  

  return (
    <div style={styles.container}>
      <Header/>

       {/* File upload area */}
       <div style={styles.content}>
       <div style={styles.uploadArea}>
        <div {...getRootProps({ style: styles.uploadBox })}>
            <input {...getInputProps()} />
            <div style={styles.uploadHeader}>
            <img src={uploadIcon} alt="Upload" style={styles.image} />   
            <p style={styles.uploadText}>Drag & Drop or <span style={{color: '#156CF7'}}>choose</span> file to upload</p>
            </div>
            </div>

            <div style={styles.buttonContainer}>
                <button style={styles.cancelButton}> Cancel </button>
                <button style={styles.submitButton} onClick={uploadFilesToServer}> Upload </button>
            </div>

        </div> 

      <div style={styles.halfBox}>
        <div style={styles.listContainer}>
          <FileList fileNames={fileNames} removeFile={removeFile} />
        </div>
        <button 
              style={(isUploading || !hasUploaded) ? { ...styles.navigateButton, backgroundColor: '#DEE2E6' } : styles.navigateButton}
              onClick={navigateFolders}
              disabled={isUploading}
            >
              {isUploading ? 'Uploading Files...' : 'See Folders'}
              
            </button>
        { isUploading  && (
            <img src={loadingIcon} className="rotating" alt="Loading" style={{ width: '30px', height: '30px', marginRight: '10px' }} />
          )}
      </div>
      </div>
    </div>
  );
};

const styles = {
    container: {
        display: 'flex',
        height: '100vh',
        width: '100%',
        backgroundColor: 'white',
        flexDirection: 'column',
    },
    halfBox: {
        display: 'flex',
        width: '50%',
        justifyContent: 'flex-start',
        alignItems: 'center',
        flexDirection: 'column',
    },
    uploadArea: {
        display: 'flex',
        width: '50%',
        flexDirection: 'column',
    },
    uploadBox: {
        display: 'flex',
        backgroundColor: 'white',
        height: '20%',
        borderRadius: 25,
        margin: '5%',
        border: '1px dashed darkgrey', 
        alignItems: 'center',
        justifyContent: 'center',
    },
    loadingBox: {
        backgroundColor: 'white',
        width: '50%',
    },
    uploadText: {
        fontWeight: 'bold',
    },
    content: {
        display: 'flex',
        width: '100%',
        height: '100%',
        justifyContent: 'space-between',
    },
    image: {
        width: '30px', 
        height: '30px', 
        objectFit: 'contain', 
        marginTop: 20,
    },
    buttonContainer: {
        display: 'flex',
        marginLeft: '5%',
        marignRight: '5%',
    },
    submitButton: {
        backgroundColor: '#156CF7', // Default background
        color: 'white',
        borderRadius: '10px',
        margin: '4px',
        width: '30%',
        border: 'none',
        cursor: 'pointer',
        fontWeight: 'bold',
        fontSize: '90%',
    },
    cancelButton: {
        backgroundColor: '#DEE2E6', // Default background
        color: 'black',
        borderRadius: '10px',
        margin: '4px',
        height: 50,
        width: '30%',
        border: 'none',
        cursor: 'pointer',
        fontWeight: 'bold',
        fontSize: '90%',
    },
    listContainer: {
        display: 'flex',
        width: '80%',
        height: '50%',
        margin: 20,
    },
    navigateButton: {
      display: 'flex',
      width: '80%',
      height: '10%',
      padding: 5,
      margin: 15,
      borderRadius: 15,
      fontSize: 18,
      border: 'none',
      cursor: 'pointer',
      fontWeight: 'bold',
      backgroundColor: '#156CF7',
      color: 'white',
      justifyContent: 'center',
      alignItems: 'center',
    },
    loadingBox: {
      display: 'flex',
      maxWidth: '20%',
      flex: '1',
      justifyContent: 'flex-end',
    }
};  

export default Upload;