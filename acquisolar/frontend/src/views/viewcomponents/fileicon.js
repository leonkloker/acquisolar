import React, { useCallback, useState, useEffect } from 'react';
import fileIcon from '../../icons/pngegg.png';
import searchIcon from '../../icons/search.png';
import DarkenButton from './darkenbutton';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const ENDPOINT = 'http://localhost:3001';

const FileIcon = ({ file, onUpdateTitle, onShowPdf }) => {
    const navigate = useNavigate();
    const [contentToShow, setContentToShow] = useState(null);
    const [notes, setNotes] = useState(file.notes || "");
  
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
        setContentToShow(null);

        const data = {
            originalFilename: file.current_title,
            newFilename: file.Suggested_title,
        };

        axios.post(ENDPOINT + '/renameFile', data)
            .then((response) => {
                console.log('File rename successful', response);
            })
            .catch((error) => {
                console.error('Error renaming file', error);
            });
    };

    const handleSearch = () => {
        onShowPdf(file);
        navigate('/searchscreen', { state: { filename: file.current_title } });
    };

    const handleNotes = () => {
        // Function to send notes to the backend
        const data = {
            filename: file.current_title,
            notes: file.notes,
        };

        axios.post(ENDPOINT + '/updateNotes', data)
            .then((response) => {
                console.log('Notes update successful', response);
            })
            .catch((error) => {
                console.error('Error updating notes', error);
            });

        handleShowContent('notes')
    };

    const handleNoteChange = (event) => {
        setNotes(event.target.value);
    };

    const handleMove = () => {

    };
  
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
                <button style={styles.searchButton} onClick={handleSearch}>
                    <img src={searchIcon} alt="Search" style={styles.searchImage} />                    
                    Search...
                </button>

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
                                text="Cancel"
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
                    onClick={handleShowContent('move')}
                />
                <DarkenButton 
                    text="Notes"
                    onClick={handleShowContent('notes')}
                />
                {contentToShow === 'notes' && (
                    <div style={styles.contentBox}>
                        <textarea
                            value={notes || file.notes}
                            onChange={handleNoteChange}
                            style={{ width: '100%', height: '100px' }} // Adjust styling as needed
                        />
                        <div style={styles.buttonContainer}>
                            <DarkenButton 
                                text="Cancel"
                                onClick= {handleShowContent('notes')}
                            />
                            <DarkenButton
                                text="Confirm"
                                onClick={handleNotes}
                            />
                        </div>
                    </div>
                )}
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
        height: '32%', 
        maxHeight: '32%',
        borderRadius: '5px',
        backgroundColor: '#ffffff',
        margin: '10px',
        overflow: 'auto',
        padding: 5,
        boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)',
        position: 'relative'
    },
    image: {
        width: '70px', 
        height: '70px', 
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
    searchButton: {
        backgroundColor: '#FFFFFF',
        color: 'black',
        borderRadius: '10px',
        margin: '4px',
        padding: '2px',
        paddingLeft: '5px',
        paddingRight: '5px',
        width: '100%',
        borderWidth: 1,
        borderColor: '#979797',
        cursor: 'pointer',
    },
    searchImage: {
        width: '10px', 
        height: '10px', 
        objectFit: 'contain', 
        marginRight: 4,
    }

  };
  
  export default FileIcon;