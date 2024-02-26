import React from 'react';

// Header component
const Header = () => {
    return (
      <header style={styles.header}>
        <h1 style={styles.title}>AcquiSolar</h1>
        <a href="/about" style={styles.aboutLink}>About Us</a>
      </header>
    );
  };


const styles = {
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
  };

  export default Header;