import React, { useCallback, useState, useEffect } from 'react';
import folderIcon from '../icons/folder-icon.png';
import { Document, Page, pdfjs } from 'react-pdf';
import { useNavigate, useLocation } from 'react-router-dom';
import PDFViewer from './viewcomponents/pdfviewer2';
import axios from 'axios';
import FileIcon from './viewcomponents/fileicon';

// Set the workerSrc for pdfjs
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

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

  const File = () => {
    const location = useLocation();
    const { folderName } = location.state || {};
    const [files, setFiles] = useState(initialFiles);
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

    useEffect(() => {
        const fetchFolderContents = async (folderName) => {
          try {
              const response = await axios.post(URLServer + '/get-folder-contents', { folderName });
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
            <header style={styles.header}>
                <h1 style={styles.title}>ACQUISOLAR</h1>
            </header>


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
    flexDirection: 'column',
    alignItems: 'flex-start', 
    padding: '20px',
    paddingTop: '10px',
    width: '100%',
  },
  folderContainer: {
    display: 'flex',
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },

};

export default File;