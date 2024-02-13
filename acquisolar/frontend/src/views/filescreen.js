import React, { useCallback, useState } from 'react';
import folderIcon from '../icons/folder-icon.png';
import { useNavigate } from 'react-router-dom';

// Example dictionary of folders and files
const initialFolders = {
    'Documents': ['doc1.txt', 'doc2.txt', 'report.pdf'],
    'Photos': ['photo1.jpg', 'photo2.png'],
    'Music': ['song1.mp3', 'song2.wav', 'album1.zip'],
    /*'Documents2': ['doc1.txt', 'doc2.txt', 'report.pdf'],
    'Photos2': ['photo1.jpg', 'photo2.png'],
    'Music2': ['song1.mp3', 'song2.wav', 'album1.zip'],
    'Documents3': ['doc1.txt', 'doc2.txt', 'report.pdf'],
    'Photos3': ['photo1.jpg', 'photo2.png'],
    'Music3': ['song1.mp3', 'song2.wav', 'album1.zip'],
    'Documents4': ['doc1.txt', 'doc2.txt', 'report.pdf'],
    'Photos4': ['photo1.jpg', 'photo2.png'],
    'Music4': ['song1.mp3', 'song2.wav', 'album1.zip'],*/
  };

  const FileIcon = ({ name }) => (
    <div style={styles.fileIconContainer}>
      <div style={styles.fileContent}>
        <img src={folderIcon} alt="File" style={styles.image} />
        <p>{name}</p>
      </div>
    </div>
  );

  const File = () => {
    const [folders, setFolders] = useState(initialFolders);
    const [openFolder, setOpenFolder] = useState(null); // Tracks the currently open folder

    return (
        <div style={styles.container}>
            {/* Header */}
            <header style={styles.header}>
                <h1 style={styles.title}>AcquiSolar</h1>
                <a href="/about" style={styles.aboutLink}>About Us</a>
            </header>
            {/* If a folder is open, display the file icons */}
            {/*<FilesScreen files={folders[openFolder]} />*/}
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
    backgroundColor: '#7AA6B9', 
    padding: '5px 10px',
    borderRadius: '5px', 
  },
  content: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start', 
    padding: '20px',
    paddingTop: '10px',
    width: '100%',
  },
  mainContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px',
    paddingTop: '10px',
  },  
  image: {
    width: '30%', // Set a max-width that fits within the container
    objectFit: 'contain', // This ensures that the aspect ratio of the image is maintained
  },
  fileIconContainer: {
    width: '15%', // Set a fixed width or use percentages
    minWidth: '15%',
    height: '30%', // Set a fixed height or use percentages
    borderRadius: '15px',
    backgroundColor: '#ffffff',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'space-around', // This will distribute the spacing evenly
    overflow: 'hidden', // This ensures that the content doesn't spill out
    margin: '10px',
  },
  fileContent: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
};

export default File;