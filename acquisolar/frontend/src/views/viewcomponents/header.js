import React from 'react';
import { useNavigate } from 'react-router-dom';

// Header component
const Header = () => {
  const navigate = useNavigate();

  const handleUploadClick = () => {
    console.log('Upload button clicked');
    navigate('/'); 
  };
  
  const handleFilesClick = () => {
    console.log('Files button clicked');
    navigate('/folders'); 
  };
  
  const handleSearchClick = () => {
    console.log('Search button clicked');
    navigate('/searchscreen'); 
  };

  return (

    <header style={styles.header}>
      <h1 style={styles.title}>ACQUISOLAR</h1>
      <div>
        <button style={styles.headerButton} onClick={handleUploadClick}>Upload</button>
        <button style={styles.headerButton} onClick={handleFilesClick}>Files</button>
        <button style={styles.headerButton} onClick={handleSearchClick}>Search</button>
      </div>
      
    </header>

  );
};

const styles = {
    header: {
        display: 'flex',
        justifyContent: 'left',
        alignItems: 'center',
        padding: '20px',
        color: 'black',
        fontSize: '16px',
        backgroundColor: '#FFFFFF',
        fontFamily: 'Helvetica Neue',
        borderBottom: '1px solid #DEE2E6',
      },
    title: {
        margin: 0,
        marginRight: 250
      },
      headerButton: {
        fontFamily: 'Helvetica Neue',
        border: 0,
        backgroundColor: "white",
        fontSize: '25px',
        margin: 10,
        marginRight: 40,
        cursor: 'pointer',
      },
  };

  export default Header;
