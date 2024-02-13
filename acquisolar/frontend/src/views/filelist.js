// UI for the filelist in the dropbox
import React from 'react';

const FileList = ({ fileNames, removeFile }) => {
  return (
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
  );
};

const styles = {
    filesTitle: {
        margin: '8px', 
      },
    fileListContainer: {
      width: '100%',
      height: '100%',
      backgroundColor: '#BCD5E0',
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
    removeButton: {
      marginLeft: '10px',
      backgroundColor: 'transparent',
      border: 'none',
      cursor: 'pointer',
      color: 'red',
      fontWeight: 'bold',
    },
  };

export default FileList;