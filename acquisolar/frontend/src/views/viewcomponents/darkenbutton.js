import React, { useState } from 'react';

const DarkenButton = ({ text, onClick }) => {
  const [isHovered, setIsHovered] = useState(false);

  // Styles
  const baseStyle = {
    backgroundColor: '#DEE2E6', // Default background
    color: 'black',
    borderRadius: '10px',
    margin: '4px',

    padding: '3px',
    paddingLeft: '5px',
    paddingRight: '5px',
    width: '100%',
    border: 'none',
    cursor: 'pointer',
  };

  const hoverStyle = {
    ...baseStyle,
    backgroundColor: '#979797', // Darker background on hover
  };

  return (
    <button
      style={isHovered ? hoverStyle : baseStyle}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={ onClick }
    >
      { text }
    </button>
  );
};

export default DarkenButton;