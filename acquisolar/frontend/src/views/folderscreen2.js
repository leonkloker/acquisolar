import React, { useCallback, useState, useEffect } from 'react';
import folderIcon from '../icons/folder-icon.png';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

// Example dictionary of folders and files
const initialFolders = {
    'Documents': ['doc1.txt', 'doc2.txt', 'report.pdf'],
    'Photos': ['photo1.jpg', 'photo2.png'],
    'Music': ['song1.mp3', 'song2.wav', 'album1.zip'],
  };

  // url of aws server and port 80
  // change to 'http://localhost:3001' for localhost
  // or http://54.90.226.66:80' for aws
  // Changed this variable name or causes issues with other parts of code
  const URLServer = 'http://localhost:3001'

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
    // Replace [] in useState with initialFolder for an example
    const [folders, setFolders] = useState([]);

    
    useEffect(() => {
      // Function to fetch folders data from the backend
      const fetchFolders = async () => {
          try {
              const response = await axios.get(URLServer + '/get-folders');
              setFolders(response.data);
          } catch (error) {
              console.error('Error fetching data: ', error);
          }
      };

      fetchFolders();
  }, []);

    const handleViewFolder = (folderName) => {
        navigate('/filescreen', { state: { folderName } });
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