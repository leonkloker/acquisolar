import React, { useCallback, useState, useEffect } from 'react';
import fileIcon from '../../icons/file-icon.png';
import DarkenButton from './darkenbutton';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

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
        <div style={styles.titleContainer}>
            {/* TITLE FILE HERE */}
            <p style={styles.titleText}>
                {file.current_title}
            </p>
        </div>

        <div style={styles.overviewContainer}>
            {/* Overview container */}
            <p style={styles.summaryText}>
                {file.Document_date}
            </p>

            <p style={styles.summaryText}>
                {file.number_of_pages}
            </p>
        </div>

        <div style={styles.contentContainer}>
            {/* content container */}

            <div style={styles.subContainer}>
                {/* Image and two buttons */}
                <img src={fileIcon} alt="File" style={styles.image} />
                <DarkenButton 
                    text="Search"

                />

                <DarkenButton 
                    text="Summary"
                />


            </div>

            <div style={styles.subContainer}>
                {/* Four buttons */}
                <DarkenButton 
                    text="Rename"
                />
                <DarkenButton 
                    text="Move"
                />
                <DarkenButton 
                    text="Tasks"
                />
                <DarkenButton 
                    text="Q&A"
                />                
            </div>

        </div>
    </div>

    );
  };

  const styles = {
    fileIconContainer: {
        display: 'flex',
        flexDirection: 'column',
        width: '15%', 
        height: '30%', 
        maxWidth: '15%',
        borderRadius: '5px',
        backgroundColor: '#ffffff',
        margin: '10px',
        overflow: 'auto',
        padding: 5,
        boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
    },
    image: {
        width: '50px', 
        height: '50px', 
        objectFit: 'contain', 
    },
    titleContainer: {
        alignItems: 'center',
        wordWrap: 'break-word', // Breaks the words to prevent overflow
        maxWidth: '100%',
        maxHeight: '20%', 
    },
    overviewContainer: {
        display: 'flex',
        justifyContent: 'space-between',
        marginLeft: 10,
        marginRight: 10,
        flexDirection: 'row',
    },
    contentContainer: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        margin: '3px',
    },
    subContainer: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    titleText: {
        fontWeight: 'bold',
    },
    summaryText: {

    },

    
  };
  
  export default FileIcon;