import React from 'react';
import { Document, Page } from 'react-pdf';

const PDFViewer = ({ showSearch, currentPdf, numPages, searchQuery, handleSearchInputChange, handleSearchSubmit, onDocumentLoadSuccess }) => {
  return (
    <div style={styles.pdfViewer}>
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
      {showSearch && currentPdf && (
        <div style={styles.pdfContainer}>
          <Document
            file={currentPdf}
            onLoadSuccess={onDocumentLoadSuccess}
          >
            {Array.from(new Array(numPages), (el, index) => (
              <Page key={`page_${index + 1}`} pageNumber={index + 1} />
            ))}
          </Document>
        </div>
      )}
    </div>
  );
};

const styles = {
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
    pdfContainer: {
      maxHeight: '600px',
      overflowY: 'auto',
      marginLeft: '5%',
      marginRight: '10%',
    },
    pdfViewer: {
        flex: 1,
        flexDirection: 'column',
      }
  };

// Remember to pass onDocumentLoadSuccess function from the parent component or define it here if it's only used by PDFViewer
export default PDFViewer;