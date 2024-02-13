import React, { useCallback, useState, useEffect } from 'react';
import folderIcon from '../icons/folder-icon.png';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

// Example dictionary of folders and files
const initialFiles = ['doc1.txt', 'doc2.txt', 'report.pdf'];

   // url of aws server and port 80
  // change to 'http://localhost:3001' for localhost
  // or http://54.90.226.66:80' for aws
  // Changed this variable name or causes issues with other parts of code
  const URLServer = 'http://localhost:3001'

  const FileIcon = ({ name }) => (
    <div style={styles.fileIconContainer}>
      <div style={styles.fileContent}>
        <img src={folderIcon} alt="File" style={styles.image} />
        <p>{name}</p>
      </div>
    </div>
  );


  const File = () => {
    const location = useLocation();
    const { folderName } = location.state || {};
    const [folders, setFolders] = useState([]);
    const [files, setFiles] = useState([]);
    const [openFolder, setOpenFolder] = useState(null); // Tracks the currently open folder

    
    useEffect(() => {
        const fetchFolderContents = async (folderName) => {
          try {
              const response = await axios.post(URLServer + '/get-folder-contents', { folderName });
              setFiles(response.data); // Update state with folder contents
          } catch (error) {
              console.error('Error fetching folder contents:', error);
              setFiles([]); // Reset or handle error
          }
      };
      fetchFolderContents(folderName);
      }, []);

    return (
        <div style={styles.container}>
            {/* Header */}
            <header style={styles.header}>
                <h1 style={styles.title}>AcquiSolar</h1>
                <a href="/about" style={styles.aboutLink}>About Us</a>
            </header>
            {/* If a folder is open, display the file icons */}
            {/*<FilesScreen files={folders[openFolder]} />*/}
            <div style={styles.folderContainer}>
            {Object.keys(files).map((fileIndex) => (
                <FileIcon
                key={fileIndex}
                name={files[fileIndex]}
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
  folderContainer: {
    display: 'flex',
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
};

export default File;