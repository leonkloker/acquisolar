import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { Document, Page, pdfjs } from 'react-pdf';
import FileList from './viewcomponents/filelist';
import PDFViewer from './viewcomponents/pdfviewer2';
import { useNavigate, useLocation } from 'react-router-dom';
import QueryResult from './viewcomponents/queryresult';
import axios from 'axios';

// Set the workerSrc for pdfjs
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

// url of aws server and port 80
// change to 'http://localhost:3001' for localhost
// or http://54.90.226.66:80' for aws
// Changed this variable name or causes issues with other parts of code
const URLServer = 'http://localhost:3001'

const Search = () => {
const location = useLocation();
  const navigate = useNavigate();
  const [showSearch, setShowSearch] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPdf, setCurrentPdf] = useState(null);
  const [blobUrl, setBlobUrl] = useState('');
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

  useEffect(() => {
    if (location.state && location.state.file) {
      const newBlobUrl = URL.createObjectURL(location.state.file);
      setBlobUrl(newBlobUrl);
      setCurrentPdf(location.state.file); // Save the File object if needed
    }

    // Clean up the blob URL when the component unmounts
    return () => {
      if (blobUrl) {
        URL.revokeObjectURL(blobUrl);
      }
    };
  }, [location]);
  
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

  const onDocumentLoadSuccess = ({ numPages }) => {
    console.log("Document is loaded with " + numPages + " pages");
    setNumPages(numPages);
  };

  const onDocumentLoadError = (error) => {
    console.error('Error while loading document!', error);
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

      {/* Submit button */}
      <button onClick={handleNavigate} style={styles.submitButton} >Folders</button>
        <div style={styles.mainContent}>
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
          onDocumentLoadError={onDocumentLoadError}
        />
      </div>
      <div style={styles.queryContainer}>
      <QueryResult/>
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
  mainContent: {
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
  submitButton: {
    padding: '10px 20px',
    width: '10%',
    margin: '2%',
    fontSize: '16px',
    backgroundColor: '#FFF',
    border: 'none',
    borderRadius: '20px',
    cursor: 'pointer',
    color: 'black',
    fontWeight: 'bold',
  },
  mainContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#7AA6B9',
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'column',
    alignSelf: 'flex-start',
  },
  queryContainer: {
    display: 'flex',

  }
  
};

export default Search;