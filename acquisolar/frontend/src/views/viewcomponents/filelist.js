// UI for the filelist in the dropbox
import React from 'react';

const FileList = ({ fileNames, removeFile }) => {
  return (
    <div style={styles.fileListContainer}>
      <p style={styles.filesTitle}>Files to Upload:</p>
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
  );
};

const styles = {
    filesTitle: {
        margin: '5px', 
        fontWeight: 'bold',
        fontSize: 18,
      },
    fileListContainer: {
      width: '100%',
      height: '100%',
      backgroundColor: 'white',
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
      backgroundColor: '#F6F7F9',
      borderRadius: 15,
      padding: 5,
      boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
    },
    removeButton: {
      marginLeft: '10px',
      backgroundColor: 'transparent',
      border: 'none',
      cursor: 'pointer',
      color: 'red',
      fontWeight: 'bold',
      fontSize: '100%',
    },
  };

export default FileList;