import React from 'react';

// Header component
const Header = () => {
    return (

      <header style={styles.header}>
        <h1 style={styles.title}>ACQUISOLAR</h1>
        <div>
          <button style={styles.headerButton}>Upload</button>
          <button style={styles.headerButton}>View Files</button>
        </div>
        
      </header>

    );
  };


const styles = {
    header: {
        display: 'flex',
        justifyContent: 'space-between',
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
      },
      headerButton: {
        fontFamily: 'Helvetica Neue',
        border: 0,
        backgroundColor: "white",
        fontSize: '18px',
        margin: 10,
      },
  };

  export default Header;