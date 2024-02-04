import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

const Main = () => {
  const [files, setFiles] = useState([]);
  const [fileNames, setFileNames] = useState([]);

  const onDrop = useCallback((acceptedFiles) => {
    const filteredFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    setFiles((prevFiles) => [...prevFiles, ...filteredFiles]);
    setFileNames((prevFiles) => {
      const newFileNames = filteredFiles.map((file) => file.name);
      const existingFileNames = new Set(prevFiles);
      const uniqueNewFileNames = newFileNames.filter((fileName) => !existingFileNames.has(fileName));
      return [...prevFiles, ...uniqueNewFileNames];
    });
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    type:"file",
    accept: 'application/pdf',
    onDrop,
  });

  const uploadFilesToServer = async () => {
    const formData = new FormData();
    
    // Append each file to the form data
    files.forEach((file) => {
      formData.append('files', file);
    });

    console.log(formData);

    try {
      const response = await fetch('/upload', {
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
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>AcquiSolar</h1>
        <a href="/about" style={styles.aboutLink}>About Us</a>
      </header>
      <div style={styles.content}>
        <div {...getRootProps({ style: styles.dropzone })}>
          <input {...getInputProps()} />
          <p style={styles.uploadText}>Upload Files</p>
            <div style={styles.fileListContainer}>
            <p style={{ margin: 0 }}>Files:</p>
            <ul style={styles.fileList}>
              
              {fileNames.map((fileName, index) => (
                <li key={index} style={styles.fileName}>{fileName}</li>
              ))}
            </ul>
            </div> 
        </div>
        <button style={styles.analyzeButton} onClick={uploadFilesToServer}>Analyze</button>
      </div>
    </div>
  );
};



const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    height: '100vh',
    width: '100%',
    backgroundColor: '#9ACAC4',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start', // Align content to the top
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px',
    color: 'white',
    fontSize: '24px',
  },
  title: {
    margin: 0,
  },
  aboutLink: {
    color: 'white',
    textDecoration: 'none',
    backgroundColor: '#9ACAC4', // Match the header background color
    padding: '5px 10px', // Add some padding
    borderRadius: '5px', // Optional: add some rounding to match your design
  },
  content: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start', // Align dropzone to the left
    padding: '20px',
    width: '100%', // Make sure content takes the full width
  },
  dropzone: {
    padding: '20px',
    width: '300px',
    height: 'auto',
    borderRadius: '20px',
    backgroundColor: '#ffffff',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '10px',
  },
  uploadText: {
    color: '#000000',
    marginBottom: '20px',
    fontSize: '18px',
    fontWeight: 'bold',
  },
  fileListContainer: {
    width: '100%',
    backgroundColor: '#E6F0EF',
    borderRadius: '10px',
    padding: '10px',
    textAlign: 'left',
    maxHeight: '150px',
    overflowY: 'auto', // Allow scrolling for multiple files
  },
  fileList: {
    listStyleType: 'none',
    padding: 0,
    margin: 0,
  },
  fileName: {
    color: '#000000',
    fontSize: '16px',
    lineHeight: '24px',
    padding: '5px 0',
  },
  analyzeButton: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#FFF',
    border: 'none',
    borderRadius: '20px',
    cursor: 'pointer',
    color: 'black',
    alignSelf: 'flex-start', // Align the button to the left
  },
};

export default Main;