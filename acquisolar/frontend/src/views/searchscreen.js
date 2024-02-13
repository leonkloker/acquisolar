import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Document, Page, pdfjs } from 'react-pdf';
import FileList from './filelist';
import PDFViewer from './pdfviewer';
import { useNavigate } from 'react-router-dom';

// Need to implement

// Set the workerSrc for pdfjs
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

// url of aws server and port 80
// change to 'http://localhost:3001' for localhost
// or http://54.90.226.66:80' for aws
// Changed this variable name or causes issues with other parts of code
const URLServer = 'http://localhost:3001'

const Main = () => {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [fileNames, setFileNames] = useState([]);
  const [showSearch, setShowSearch] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPdf, setCurrentPdf] = useState(null);
  const [numPages, setNumPages] = useState(null); 
  const [instances, setInstances] = useState([]);
  const [currentInstance, setCurrentInstance] = useState(0);
  const [pageNumber, setPageNumber] = useState(1);

  const findInstancesOfSearchTerm = async () => {
    let instancesFound = [];
    if (!currentPdf) return;

    const pdfDocument = await pdfjs.getDocument(URL.createObjectURL(currentPdf)).promise;

    for (let i = 1; i <= numPages; i++) {
      const page = await pdfDocument.getPage(i);
      const textContent = await page.getTextContent();
      // Look for instances of the search term in the text content
      textContent.items.forEach((item) => {
        if (item.str.includes(searchQuery)) {
          instancesFound.push({ page: i, instance: item.str });
        }
      });
    }
    setInstances(instancesFound);
    if (instancesFound.length > 0) {
      setPageNumber(instancesFound[0].page); // Go to the first instance page
    }
  };

  const goToNextInstance = () => {
    if (instances.length === 0) return;
    const nextInstance = (currentInstance + 1) % instances.length;
    setCurrentInstance(nextInstance);
    setPageNumber(instances[nextInstance].page);
  };

  const goToPreviousInstance = () => {
    const nextInstance = (currentInstance - 1) % instances.length;
    setCurrentInstance(nextInstance);
    setPageNumber(instances[nextInstance].page);
  };

  
  const handleSearchInputChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = async () => {
    if (!searchQuery) {
      alert('Please enter a search query.');
      return;
    }
  
    try {
      const response = await fetch(URLServer + '/search', {
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
    findInstancesOfSearchTerm();
  };

  const onDrop = useCallback((acceptedFiles) => {
    // Prevents duplicates from being uploaded (based on filename atm)
    const filteredFiles = acceptedFiles.filter(file => file.type === 'application/pdf');
    setFiles((prevFiles) => [...prevFiles, ...filteredFiles]);

    // If there's no currently selected PDF, display the first one dropped
    if (filteredFiles.length && !currentPdf) {
      setCurrentPdf(filteredFiles[0]);
    }

    // Filenames that are displayed when file is uploaded
    setFileNames((prevFiles) => {
      const newFileNames = filteredFiles.map((file) => file.name);
      const existingFileNames = new Set(prevFiles);
      const uniqueNewFileNames = newFileNames.filter((fileName) => !existingFileNames.has(fileName));
      return [...prevFiles, ...uniqueNewFileNames];
    });
  }, [currentPdf]);

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

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
    
    setShowSearch(true); 
    const formData = new FormData();
    
    // Append each file to the form data
    files.forEach((file) => {
      formData.append('files', file);
    });

    console.log(formData);

    try {
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
    }
  };

  const handleNavigate = () => {
    // Programmatically navigate to the /folders route
    navigate('/folders');
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <h1 style={styles.title}>AcquiSolar</h1>
        <a href="/about" style={styles.aboutLink}>About Us</a>
      </header>

      {/* Main content area */}
      <div style={styles.mainContent}>
        {/* File upload area */}
        <div {...getRootProps({ style: styles.dropzone })}>
          <input {...getInputProps()} />
          <div style={styles.uploadHeader}>
            <p style={styles.uploadText}>Upload Files</p>
            <button style={styles.addButton}>Add</button>
          </div>
          <FileList fileNames={fileNames} removeFile={removeFile} />
        </div>

        {/* PDF viewer and search functionality */}
        <PDFViewer 
          showSearch={showSearch} 
          currentPdf={currentPdf} 
          numPages={numPages} 
          searchQuery={searchQuery} 
          handleSearchInputChange={handleSearchInputChange} 
          handleSearchSubmit={handleSearchSubmit} 
          onDocumentLoadSuccess = {onDocumentLoadSuccess}
          instances={instances}
          currentInstance={currentInstance}
          findInstancesOfSearchTerm={findInstancesOfSearchTerm}
          goToNextInstance={goToNextInstance}
          goToPreviousInstance={goToPreviousInstance}
          pageNumber={pageNumber}
        />

        {/* Instructions for users */}
        {!showSearch && (
          <div style={styles.dragTextContainer}>
            <p style={styles.dragText}>Add your files in the box on the left and click Submit.</p>
            {!showSearch && (
            <button style={styles.submitButton} onClick={uploadFilesToServer}>Submit</button>
            )}
          </div>
        )}
      </div>

      {/* Submit button */}
      <div style={styles.buttonContainer}>
      {showSearch && (
      <button onClick={handleNavigate} style={styles.submitButton} > Structure Folders</button>
      )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    height: '100vh',
    width: '100%',
    backgroundColor: '#7AA6B9',
    display: 'flex',
    flexDirection: 'column',
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
    backgroundColor: '#7AA6B9', 
    padding: '5px 10px',
    borderRadius: '5px', 
  },
  dropzone: {
    padding: '20px',
    width: '300px',
    height: '400px',
    borderRadius: '15px',
    backgroundColor: '#ffffff',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '2%',
    marginLeft: '5%',
    marginTop: '5%',
  },
  uploadText: {
    color: '#000000',
    alignItems: 'flex-start',
    justifyContent: 'flex-start',
    marginBottom: '10px',
    fontSize: '18px',
    fontWeight: 'bold',
  },
  submitButton: {
    padding: '10px 20px',
    marginLeft: '5%',
    fontSize: '16px',
    backgroundColor: '#FFF',
    border: 'none',
    borderRadius: '20px',
    cursor: 'pointer',
    color: 'black',
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
    backgroundColor: '#7AA6B9',
  },
  dragTextContainer: {
    marginLeft: '20px',
    fontSize: '170%', 
    marginRight: '10%',
    fontWeight: 'bold',
    color: '#FFF',
    maxWidth: '800%', 
    textAlign: 'left',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'column',
    alignSelf: 'flex-start',
  }
  
};

export default Main;