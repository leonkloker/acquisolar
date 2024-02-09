import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

// url of aws server and port 80
// change to '' for localhost
// const URL = 'http://54.90.226.66:80'
const URL = ''

const Main = () => {
  const [files, setFiles] = useState([]);
  const [fileNames, setFileNames] = useState([]);
  const [showSearch, setShowSearch] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearchInputChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = async () => {
    if (!searchQuery) {
      alert('Please enter a search query.');
      return;
    }
  
    try {
      const response = await fetch(URL + '/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchQuery }),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log(data);
      } else {
        console.error('Search failed', response);
      }
    } catch (error) {
      console.error('Error during search', error);
    }
  };

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

  const removeFile = (fileName, event) => {
    event.stopPropagation(); // Prevent the event from bubbling up to parent elements
  
    setFiles((prevFiles) => prevFiles.filter((file) => file.name !== fileName));
    setFileNames((prevFileNames) => prevFileNames.filter((name) => name !== fileName));
  };

  const { getRootProps, getInputProps } = useDropzone({
    accept: 'application/pdf',
    onDrop,
  });

  const uploadFilesToServer = async () => {
    if (files.length === 0) {
      alert('Please submit a file.');
      return;
    }
    
    setShowSearch(true); 
    const formData = new FormData();
    
    // Append each file to the form data
    files.forEach((file) => {
      formData.append('files', file);
    });

    console.log(formData);

    try {
      const response = await fetch(URL + '/upload', {
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

  {showSearch && (
  <div style={styles.searchContainer}>
    <input 
      type="text" 
      placeholder="Search..." 
      style={styles.searchInput} 
      value={searchQuery} 
      onChange={handleSearchInputChange} 
    />
    <button style={styles.searchButton} onClick={handleSearchSubmit}>Search</button>
  </div>
)}

  <div style={styles.mainContent}>
    <div {...getRootProps({ style: styles.dropzone })}>
      <input {...getInputProps()} />
      <div style={styles.uploadHeader}>
        <p style={styles.uploadText}>Upload Files</p>
        <button style={styles.addButton}>Add</button>
      </div>
      <div style={styles.fileListContainer}>
        <p style={styles.filesTitle}>Files:</p>
        <ul style={styles.fileList}>
          {fileNames.map((fileName, index) => (
            <li key={index} style={styles.fileName}>
              {fileName}
              <button 
                style={styles.removeButton} 
                onClick={(event) => removeFile(fileName, event)}
              >
                ✕
              </button>
            </li>
          ))}
        </ul>
      </div> 
    </div>
    {!showSearch && (
      <div style={styles.dragTextContainer}>
        <p style={styles.dragText}>Add your files in the box on the left and click Submit.</p>
      </div>
    )}
  </div>

  {!showSearch && (
    <button style={styles.analyzeButton} onClick={uploadFilesToServer}>Submit</button>
  )}
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
    justifyContent: 'flex-start',
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
    backgroundColor: '#9ACAC4', 
    padding: '5px 10px',
    borderRadius: '5px', 
  },
  filesTitle: {
    margin: '8px', 
  },
  content: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start', 
    padding: '20px',
    paddingTop: '10px',
    width: '100%',
  },
  dropzone: {
    padding: '20px',
    width: '300px',
    height: '400px',
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
    alignItems: 'flex-start',
    justifyContent: 'flex-start',
    marginBottom: '10px',
    fontSize: '18px',
    fontWeight: 'bold',
  },
  fileListContainer: {
    width: '100%',
    height: '100%',
    backgroundColor: '#E6F0EF',
    borderRadius: '10px',
    padding: '0px',
    textAlign: 'left',
    overflowY: 'auto', 
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
    margin: '8px',
  },
  analyzeButton: {
    padding: '10px 20px',
    marginLeft: '20px',
    fontSize: '16px',
    backgroundColor: '#FFF',
    border: 'none',
    borderRadius: '20px',
    cursor: 'pointer',
    color: 'black',
    alignSelf: 'flex-start', 
    fontWeight: 'bold',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  removeButton: {
    marginLeft: '10px',
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
    color: 'red',
    fontWeight: 'bold',
  },
  addButton: {
    marginLeft: '10px',
    padding: '5px 10px',
    fontSize: '16px',
    backgroundColor: '#FFF',
    border: '1px solid #000', 
    borderRadius: '5px',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  uploadHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    width: '100%', 
    padding: '0 20px', 
    marginBottom: '10px', 
  },
  mainContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px',
    paddingTop: '10px',
  },
  dragTextContainer: {
    marginLeft: '20px',
    fontSize: '24px', 
    marginRight: '15%',
    fontWeight: 'bold',
    color: '#FFF',
    maxWidth: '400px', 
    textAlign: 'left',
  },
  searchContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    
  },
  searchInput: {
    height: '40px',
    fontSize: '18px',
    padding: '0 15px',
    border: '2px solid #9ACAC4', 
    borderRadius: '20px', 
    marginRight: '10px', 
    outline: 'none', 
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', 
  },
  
  searchButton: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#FFF', 
    color: 'black', 
    border: 'none',
    borderRadius: '20px', 
    cursor: 'pointer',
    outline: 'none', 
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', 
    fontWeight: 'bold',
  },
  
};

export default Main;