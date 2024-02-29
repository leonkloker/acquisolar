import React, { useCallback, useState, useEffect } from 'react';
import Header from './viewcomponents/header';
import PDFViewer from './viewcomponents/pdfviewer2';
import { useNavigate, useLocation } from 'react-router-dom';

const Search = () => {
    const location = useLocation();
    const [filename, SetFilename] = useState("")

    useEffect(() => {
        if (location.state && location.state.filename) {
          SetFilename(location.state.filename)
        }
    }, [location]);

  return (
    <div style={styles.container}>
        {/* Header */}
        <Header/>

        {/* Whole Content */}
        <div style={styles.content}>
            HIIIII {filename}
            <iframe src={`http://localhost:5000/get-pdf/${filename}`} width="100%" height="800px">
          This browser does not support PDFs. Please download the PDF to view it: <a href={`http://localhost:5000/get-pdf/${filename}`}>Download PDF</a>.
        </iframe>
            {/* Search Content */}
            <div style={styles.searchContainer}>
                <div style={styles.searchBar}>
                    <div style={styles.searchText}>

                    </div>
                    <button style={styles.searchButton}>

                    </button>
                </div>

                <div style={styles.searchResponse}>

                </div>
            </div>

            {/* PDF Viewer */}
            <div style={styles.pdfContainer}>
                <div style={styles.instanceContainer}>

                </div>
                <div style={styles.pdfContent}>

                </div>
            </div>
        </div>

    </div>
  );
};

const styles = {
    container: {
        fontFamily: 'Arial, sans-serif',
        height: '100vh',
        width: '100%',
        backgroundColor: '#FFFFFF',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
    },
    content: {
        display: 'flex',
        flexDirection: 'row',
        margin: 5,
        border: 5,
    }
};

export default Search;