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

  const FolderIcon = ({ name, fileCount, onView }) => (
    <div style={styles.folderIconContainer} onDoubleClick={onView}>
      <div style={styles.folderContent}>
        <img src={folderIcon} alt="Folder" style={styles.image} />
        <p>{name}</p>
        <p>{fileCount} files</p>
      </div>
    </div>
  );

const Folder = () => {
    const navigate = useNavigate();
    const [folders, setFolders] = useState(initialFolders);

    const handleViewFolder = (folderName) => {
        // Logic to navigate to the folder's content view
        // For now, we'll just log the folder name to the console
        navigate('/filescreen');
        console.log(`Viewing contents of ${folderName}`);
    };
    return (
    <div style={styles.container}>
        {/* Header */}
        <header style={styles.header}>
            <h1 href="/" style={styles.title}>AcquiSolar</h1>
            <a href="/about" style={styles.aboutLink}>About Us</a>
        </header>

        <div style={styles.folderContainer}>
            {Object.keys(folders).map((folderName) => (
                <FolderIcon
                key={folderName}
                name={folderName}
                fileCount={folders[folderName].length}
                onView={() => handleViewFolder(folderName)}
                />
            ))}
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
  folderContainer: {
    display: 'flex',
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  folderIconContainer: {
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
  image: {
    width: '30%', // Set a max-width that fits within the container
    objectFit: 'contain', // This ensures that the aspect ratio of the image is maintained
  },
  openButton: {
    marginLeft: '10px',
    padding: '5px 10px',
    backgroundColor: '#FFF',
    border: '1px solid #000', 
    borderRadius: '5px',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
};

export default Folder;