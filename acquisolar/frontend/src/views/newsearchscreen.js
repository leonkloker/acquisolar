import React, { useCallback, useState, useEffect } from 'react';
import Header from './viewcomponents/header';
import PDFViewer from './viewcomponents/pdfviewer2';
import { useNavigate, useLocation } from 'react-router-dom';
import QueryResult from './viewcomponents/queryresult';

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
            {/* Search Content */}
            <div style={styles.searchContainer}>
                <div style={styles.searchBar}>
                <input
                    type="text"
                    placeholder="Search..."
                    style={styles.searchInput}
                />
                <button style={styles.searchButton}>Search</button>
                </div>
                <QueryResult/>
            </div>

            {/* PDF Viewer */}
            <div style={styles.pdfContainer}>
                    <iframe src={`http://localhost:3001/get-pdf/${filename}`} width="100%" height="600px">
                    This browser does not support PDFs. Please download the PDF to view it: <a href={`http://localhost:3001/get-pdf/${filename}`}>Download PDF</a>.
                    </iframe>
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
    },
    content: {
        display: 'flex',
        flexDirection: 'row',
    },
    pdfContainer: {
        display: 'flex',
        width: '65%',
        justifyContent: 'center',
        backgroundColor: 'white',
        marginTop: 20,
        margin: 15,
    },
    searchContainer: {
        display: 'flex',
        width: '35%',
        backgroundColor: 'white',
        flexDirection: 'column',
        justifyContent: 'flex-start',
    },
    searchText: {
        color: 'grey',
    },
    searchBar: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'flex-start',
        alignItems: 'center',
    },
    searchButton: {
        padding: '10px 20px',
        fontSize: '16px',
        backgroundColor: '#156CF7',
        color: 'white',
        border: 'none',
        borderRadius: '15px',
        cursor: 'pointer',
        outline: 'none',
        margin: '4px'
      },
    searchInput: {
        height: '40px',
        marginLeft: "3%",
        fontSize: '18px',
        padding: '0 15px',
        backgroundColor: '#F3F3F3',
        border: 0,
        borderRadius: '15px',
        marginRight: '10px',
        outline: 'none',
    },

};

export default Search;