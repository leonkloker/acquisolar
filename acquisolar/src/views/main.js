import React, { useCallback, useState } from 'react';

const Main = () => {
    const [fileName, setFileName] = useState('');

    const onDrop = useCallback((event) => {
      event.preventDefault();
      if (event.dataTransfer.files && event.dataTransfer.files[0]) {
        const file = event.dataTransfer.files[0];
        setFileName(file.name);
      }
    }, []);
  
    const onChange = (event) => {
      if (event.target.files && event.target.files[0]) {
        const file = event.target.files[0];
        setFileName(file.name);
      }
    };
  
    const onDragOver = (event) => {
      event.preventDefault();
    };

  return (
    <div 
    className="drop-box"
    onDrop={onDrop}
    onDragOver={onDragOver}
    style={{
      width: '300px',
      height: '200px',
      borderWidth: '2px',
      borderColor: '#666',
      borderStyle: 'dashed',
      borderRadius: '5px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'column',
      fontSize: '16px',
      color: '#666',
      marginBottom: '20px',
      position: 'relative',
    }}
  >
    Drag and drop a file here or click to select a file
    <input
      type="file"
      style={{
        position: 'absolute',
        width: '100%',
        height: '100%',
        top: '0',
        left: '0',
        opacity: '0',
        cursor: 'pointer'
      }}
      onChange={onChange}
      onClick={(event) => event.stopPropagation()} // Prevent input from capturing clicks outside the drop-box
    />
              {fileName && <p>File name: {fileName}</p>}
  </div>
  );
};

export default Main;