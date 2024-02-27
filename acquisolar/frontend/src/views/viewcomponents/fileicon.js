import React, { useCallback, useState, useEffect } from 'react';
import fileIcon from '../../icons/file-icon.png';
import DarkenButton from './darkenbutton';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const FileIcon = ({ file, onUpdateTitle, onShowPdf }) => {
    const [contentToShow, setContentToShow] = useState(null);
  
    const handleShowContent = (content) => {
        return () => {
            if (!contentToShow) {
                setContentToShow(content);
            } else {
                setContentToShow(null);
            }
        };
    };
  
    const handleConfirmTitle = () => {
        onUpdateTitle(file.id, file.Suggested_title);
        setContentToShow(null)
    };

    const handleSearch = () => {
        onShowPdf(file);
    }
  
    return (
    <div style={styles.fileIconContainer}>
        <div style={styles.titleContainer}>
            {/* Title */}
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
                {file.number_of_pages} page(s)
            </p>
        </div>

        <div style={styles.contentContainer}>
            {/* content container */}

            <div style={styles.subContainer}>
                {/* Image and two buttons */}
                <img src={fileIcon} alt="File" style={styles.image} />
                <DarkenButton 
                    text="Search"
                    onClick={handleSearch}
                />

                <DarkenButton 
                    text="Summary"
                    onClick={handleShowContent('summary')}
                />
                {contentToShow === 'summary' && (
                    <div style={styles.contentBox}>
                        <p>{file.Document_summary}</p>
                        <DarkenButton 
                                text="Close Summary"
                                onClick= {handleShowContent('summary')}
                        />
                    </div>
                )}

            </div>

            <div style={styles.subContainer}>
                {/* Four buttons */}
                <DarkenButton 
                    text="Rename"
                    onClick={handleShowContent('title')}
                />
                {contentToShow === 'title' && (
                    <div style={styles.contentBox}>
                        <p>Rename file: {file.Suggested_title}</p>

                        <div style={styles.buttonContainer}>
                            <DarkenButton 
                                text="X"
                                onClick= {handleShowContent('title')}
                            />
                            <DarkenButton
                                text="Confirm"
                                onClick={handleConfirmTitle}
                            />
                        </div>
                    </div>
                )}
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
        width: '18%', 
        height: '30%', 
        maxHeight: '30%',
        borderRadius: '5px',
        backgroundColor: '#ffffff',
        margin: '10px',
        overflow: 'auto',
        padding: 5,
        boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
        position: 'relative'
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
        justifyContent: 'space-evenly',

    },
    subContainer: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    buttonContainer: {
        display: 'flex',
        flexDirection: 'row',
    },
    contentBox: {
        position: 'absolute',
        zIndex: 1000, 
        backgroundColor: 'white', 
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', 
        borderRadius: '4px',
        padding: '20px', 
        maxWidth: '90%', 
        maxHeight: '90%', 
        overflow: 'auto',
        top: 0, 
        right: 0, 
        bottom: 0,
        left: 0, 

    },
    titleText: {
        fontWeight: 'bold',
    },
    summaryText: {
        color: '#9499A1',
        fontSize: 14,
    },

  };
  
  export default FileIcon;