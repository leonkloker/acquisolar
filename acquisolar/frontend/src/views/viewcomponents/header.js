import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

// Header component
const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  const buttonStyle = (path) => ({
    ...styles.headerButton,
    backgroundColor: isActive(path) ? '#dddddd' : 'white',
    color: 'black',
  });

  const handleUploadClick = () => {
    console.log('Upload button clicked');
    navigate('/');
  };
  
  const handleFilesClick = () => {
    console.log('Files button clicked');
    navigate('/folders'); 
  };

  /*
  const handlePreferenceClick = () => {
    console.log('Preferences button clicked');
    navigate('/preferences');
  }*/
  
  const handleSearchClick = () => {
    console.log('Search button clicked');
    navigate('/searchscreen'); 
  };

  return (
    <header style={styles.header}>
      <h1 style={styles.title}>ACQUISOLAR</h1>
      <div>
        <button style={buttonStyle('/')} onClick={handleUploadClick}>Upload</button>
        <button style={buttonStyle('/folders')} onClick={handleFilesClick}>Files</button>
        <button style={buttonStyle('/searchscreen')} onClick={handleSearchClick}>Search</button>
        {/*<button style={buttonStyle('/preferences')} onClick={handlePreferenceClick()}>Preferences</button>*/}
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
        borderRadius: '5px',
        fontSize: '100%',
      },
  };

  export default Header;
