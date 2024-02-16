import React, { useCallback, useState, useEffect } from 'react';
import folderIcon from '../icons/folder-icon.png';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

// url of aws server and port 80
// change to 'http://localhost:3001' for localhost
// or http://54.90.226.66:80' for aws
// Changed this variable name or causes issues with other parts of code
const URLServer = 'http://localhost:3001'

// Example dictionary of folders and files
const initialFiles = [
  {
      "Document_date": "Oct-28, 2010",
      "Document_summary": "This document is an Interconnection Agreement between Kauai Island Utility Cooperative and Kapaa Solar LLC, outlining the terms and conditions for the interconnection of a Small Generating Facility. It covers responsibilities, costs, termination, disputes, insurance, confidentiality, and other miscellaneous provisions. The Agreement is detailed and comprehensive, ensuring compliance with laws and regulations for a smooth interconnection process.",
      "Suggested_title": "10-28-2010 Interconnection Agreement.pdf",
      "Suggested_title_v2": "Interconnection Agreement - 10-28-2010.pdf",
      "Suggested_title_v3": "Small Generating Facility Interconnection - Oct-28-2010.pdf",
      "Document_folder_path": "project_name/Unclassified",
      "number_of_pages": 46,
      "original_title": "2010-0179_IA_on_p3.pdf",
      "current_title": "2010-0179_IA_on_p3.pdf",
      "notes": "",
      "questions": "",
      "open_tasks": "",
      "id": 1
  },
  {
      "Document_date": "Jan-26, 2024",
      "Document_summary": "This document is a detailed resume of Leon Kloker's education, internships, research projects, publications, awards, and additional work. It showcases his expertise in computational and mathematical engineering, machine learning research, and various technical skills. The document provides a comprehensive overview of Leon Kloker's academic and professional background, highlighting his achievements and contributions in the field.",
      "Suggested_title": "Leon Kloker's Resume.pdf",
      "Suggested_title_v2": "MMM-DD-YYYY Kloker's Academic Profile.pdf",
      "Suggested_title_v3": "MMM-DD-YYYY Kloker's Expertise Overview.pdf",
      "Document_folder_path": "Unclassified",
      "number_of_pages": 1,
      "original_title": "Kloker_Leon_CV.pdf",
      "current_title": "Kloker_Leon_CV.pdf",
      "notes": "",
      "questions": "",
      "open_tasks": "",
      "id": 2
  },
  {
      "Document_date": "Oct-14, 2019",
      "Document_summary": "This document is a letter of intent between Haleakala Ranch Company and Clearway Renew LLC for the development of a 40 megawatt solar renewable energy project in Maui County, Hawaii. The letter outlines the negotiation of terms for an Agreement to Lease and Ground Lease, contingent on Developer's Project being selected as part of the 'Final Award Group' in the RFP.",
      "Suggested_title": "10-14-2019 Solar Project Intent.pdf",
      "Suggested_title_v2": "10-14-2019 Solar Energy Agreement.pdf",
      "Suggested_title_v3": "10-14-2019 Renewable Energy Project Proposal.pdf",
      "Document_folder_path": "Solar_Projects/Development",
      "number_of_pages": 9,
      "original_title": "HR_Clearway_LOI_Fully_Executed.pdf",
      "current_title": "HR_Clearway_LOI_Fully_Executed.pdf",
      "notes": "",
      "questions": "",
      "open_tasks": "",
      "id": 3
  }
]

const FileIcon = ({ file, onUpdateTitle }) => {
  const [showOptions, setShowOptions] = useState(false);
  const [contentToShow, setContentToShow] = useState(null);

  const handleToggleOptions = () => {
    setShowOptions(!showOptions);
    // Reset the content to show whenever we toggle the options
    setContentToShow(null);
  };

  const handleShowContent = (content) => {
    setContentToShow(content);
  };

  const handleConfirmTitle = () => {
    onUpdateTitle(file.id, file.Suggested_title);
    setShowOptions(false);
  };

  return (
    <div style={styles.fileIconContainer}>
      <img src={folderIcon} alt="File" style={styles.image} />
      <div style={styles.titleContainer}>
        <p style={styles.fileName}>
          {file.current_title}
        </p>
        <button style={styles.optionButton} onClick={handleToggleOptions}>?</button>
      </div>
      {showOptions && (
        <div style={styles.tooltip}>
          <button style={styles.closeButton} onClick={handleToggleOptions}>X</button>
          {contentToShow === null && (
            <>
              <button style={styles.optionButton} onClick={() => handleShowContent('summary')}>See Summary</button>
              <button style={styles.optionButton} onClick={() => handleShowContent('title')}>Suggest Title</button>
            </>
          )}
          {contentToShow === 'summary' && (
            <div style={styles.contentBox}>
              <p>{file.Document_summary}</p>
            </div>
          )}
          {contentToShow === 'title' && (
            <div style={styles.contentBox}>
              <p>Suggested title:</p>
              <p>{file.Suggested_title}</p>
              <button style={styles.confirmButton} onClick={handleConfirmTitle}>Confirm</button>
            </div>
          )}
        </div>
      )}
      <p style={styles.fileName}>{file.Document_date}</p>
    </div>
  );
};


  const FileIcon2 = ({ name, date }) => (
    <div style={styles.fileIconContainer}>
        <div>
        <img src={folderIcon} alt="File" style={styles.image} />
        <p style={styles.fileName}>{name}</p>
        </div>
        <p style={styles.fileName}>{date}</p> 
    </div>
  );

  const File = () => {
    const location = useLocation();
    const { folderName } = location.state || {};
    const [files, setFiles] = useState([]);
    const [openFolder, setOpenFolder] = useState(null); // Tracks the currently open folder

    const updateTitle = (id, newTitle) => {
      setFiles(files.map(file => 
        file.id === id ? { ...file, current_title: newTitle } : file
      ));
    };
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
      console.log(files[0]["original_title"])
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
            {files.map((file) => (
            <FileIcon
              file={file}
              onUpdateTitle={updateTitle}
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
  image: {
    width: '30px', 
    height: '30px', 
    objectFit: 'contain', 
  },
  fileIconContainer: {
    width: '15%', 
    minWidth: '15%',
    height: '30%', 
    borderRadius: '15px',
    backgroundColor: '#ffffff',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'space-around', 
    overflow: 'hidden', 
    margin: '10px',
  },
  folderContainer: {
    display: 'flex',
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  fileName: {
    textAlign: 'center',
    wordWrap: 'break-word', 
    maxWidth: '90%', 
    marginLeft: '15%', 
    marginRight: '15%',
  },
  closeButton: {
    position: 'absolute',
    top: '5px',
    right: '5px',
    borderRadius: '20px',
    backgroundColor: '#BCD5E0',
    // Style as needed
  },
  confirmButton: {
    position: 'absolute',
    bottom: '5px',
    right: '5px',
    borderRadius: '20px',
    backgroundColor: '#BCD5E0'
    // Style as needed
  },
  tooltip: {
    position: 'absolute',
    backgroundColor: 'white',
    padding: '10px',
    border: '1px solid #ccc',
    zIndex: 100, // Ensure the tooltip appears above other elements
    borderRadius: '15px',
    backgroundColor: '#ffffff',

    // Adjust the position as needed
  },
  toggleButton: {
    marginLeft: '5px',
    cursor: 'pointer',
    backgroundColor: '#BCD5E0',
    border: 'none',
    // Style the button to look like a small square or whatever you prefer
  },
  summaryBox: {
    marginTop: '10px',
    padding: '5px',
    border: '1px solid #ccc',
    backgroundColor: '#f9f9f9',
    borderRadius: '4px',
    maxHeight: '100px', // Control the size of the summary box
    overflowY: 'auto', // Add scroll if the content is too long
    fontSize: '12px', // Adjust the font size as needed
  },
  optionButton: {
    margin: '5px',
    marginRight: '14px',
    cursor: 'pointer',
    backgroundColor: '#BCD5E0',
    border: 'none',
    padding: '3px',
    borderRadius: '15px',
    // Style the button to look like a small square or whatever you prefer
  },
};

export default File;