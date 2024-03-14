import React, { useCallback, useState, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import FileIcon from './viewcomponents/fileicon';
import Header from './viewcomponents/header';
import backButton from './../icons/backbutton.png';

// Set the workerSrc for pdfjs
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

// url of aws server and port 80
// change to 'http://localhost:3001' for localhost
// or http://54.90.226.66:80' for aws
// Changed this variable name or causes issues with other parts of code
const URLServer = 'http://localhost:3001'

const File = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { folderName } = location.state || {};
  const [files, setFiles] = useState([]);
  const [openFolder, setOpenFolder] = useState(null); // Tracks the currently open folder
  const [showPdf, setShowPdf] = useState(false);
  const [selectedPdf, setSelectedPdf] = useState(null);
  const [test, setTest] = useState("");

  const updateTitle = (id, newTitle) => {
    setFiles(files.map(file => 
      file.id === id ? { ...file, current_title: newTitle } : file
    ));
  };

  const onShowPdf = (file) => {
    setShowPdf(true);
    setSelectedPdf(file);
  }
  const handleBack = () => {
    navigate('/folders');
  }

  useEffect(() => {
    console.log(folderName);
      const fetchFolderContents = async (folderName) => {
        try {
            const response = await axios.post(URLServer + '/get-folder-contents', { folderName });
            console.log(response.data)
            setFiles(response.data); // Update state with folder contents
        } catch (error) {
            console.error('Error fetching folder contents:', error);
        }
    };
    fetchFolderContents(folderName);
    }, []);

  return (
      <div style={styles.container}>
          {/* Header */}
          <Header/>

          <img src={backButton} alt="Backbutton" style={styles.imageIcon} onClick={handleBack}/>

          <div style={styles.folderContainer}>
              {files.map((file) => (
                  <FileIcon
                  file={file}
                  onUpdateTitle={updateTitle}
                  onShowPdf={onShowPdf}
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
    backgroundColor: '#FFFFFF',
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
  folderContainer: {
    display: 'flex',
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  imageIcon: {
    width: '40px', 
    height: '40px', 
    objectFit: 'contain', 
  },

};

export default File;