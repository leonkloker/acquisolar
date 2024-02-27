import React, { useCallback, useState, useEffect } from 'react';


const Search = () => {

  return (
    <div style={styles.container}>
        {/* Header */}
        <header style={styles.header}>
            <h1 style={styles.title}>ACQUISOLAR</h1>
        </header>

        {/* Whole Content */}
        <div style={styles.content}>

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
        backgroundColor: '#F9F9F9',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
    },
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '20px',
        color: 'black',
        fontSize: '24px',
    },
    title: {
        margin: 0,
    },
    content: {
        display: 'flex',
        flexDirection: 'row',
        margin: 5,
        border: 5,
    }
};

export default Search;