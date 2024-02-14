// UI for the pdfviewer
import React from 'react';
import { useEffect } from 'react';
import { Document, Page } from 'react-pdf';

const PDFViewer = ({ showSearch, currentPdf, numPages, searchQuery, handleSearchInputChange, handleSearchSubmit, onDocumentLoadSuccess, 
    instances, currentInstance, findInstancesOfSearchTerm, goToNextInstance, pageNumber, goToPreviousInstance, onDocumentLoadError }) => {

        useEffect(() => {
            console.log(currentPdf);
          }, []);

return (
    <div style={styles.pdfViewer}>
        <div style={styles.searchHeader}>
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
            <div style={styles.instanceContainer}>
            {instances.length > 0 && (
                <>
                <span style={styles.instanceText}>
                    Instance ({currentInstance + 1}/{instances.length})
                </span>
                <button style={styles.searchButton} onClick={goToPreviousInstance}>
                    Previous
                </button>
                <button style={styles.searchButton} onClick={goToNextInstance}>
                    Next
                </button>
                </>
            )}
            </div>
        </div>

        {currentPdf && (
        <div style={styles.pdfContainer}>
        <Document
        file={currentPdf}
        onLoadSuccess={onDocumentLoadSuccess}
        onLoadError={onDocumentLoadError}
        >
        <Page pageNumber={pageNumber} />
        </Document>
        </div>
        )}


    </div>
    );
};

const styles = {
    searchHeader: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '10px', 
    },
    searchContainer: {
        display: 'flex',
        justifyContent: 'flex-start',
        alignItems: 'center',
    },
    instanceContainer: {
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'center',
    },
    searchInput: {
      height: '40px',
      fontSize: '18px',
      padding: '0 15px',
      border: '2px solid #7AA6B9',
      borderRadius: '20px',
      marginRight: '10px',
      outline: 'none',
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
      fontWeight: 'bold',
      margin: '4px'
    },
    pdfContainer: {
        maxWidth: '80%',
        maxHeight: '600px',
        overflowY: 'auto',
        marginLeft: '5%',
        marginRight: '10%',
    },
    pdfViewer: {
        flex: 1,
        flexDirection: 'column',
    },
    instanceText: {
        color: 'white', 
        fontWeight: 'bold',
        margin: '0 4px', 
    },
  };

export default PDFViewer;