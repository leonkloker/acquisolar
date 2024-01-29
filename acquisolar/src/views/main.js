import React, { useCallback, useState } from 'react';

const Main = () => {
  const [fileName, setFileName] = useState('');
  const [pdfText, setPdfText] = useState('');  // State to store the extracted text

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('pdf', file);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setPdfText(data.text);  // Save the extracted text in state
    } catch (error) {
      console.error('Error:', error);
      setPdfText('');  // Reset the text on error
    }
  };

  const handleFileSelect = useCallback((event) => {
    event.preventDefault();
    const file = event.dataTransfer?.files[0] || event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setFileName(file.name);
      handleFileUpload(file);
    } else {
      console.log('Please upload a PDF file.');
    }
  }, []);

  const onDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <div>
      <div 
        className="drop-box"
        onDrop={handleFileSelect}
        onDragOver={onDragOver}
        style={{
          width: '800px',
          height: '500px',
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
          accept="application/pdf"
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            top: '0',
            left: '0',
            opacity: '0',
            cursor: 'pointer'
          }}
          onChange={handleFileSelect}
          onClick={(event) => event.stopPropagation()}
        />
        {fileName && <p>File name: {fileName}</p>}
        </div>
    {/* Text area container for extracted text */}
    {pdfText && (
      <div className="pdf-text-container" style={{ textAlign: 'center' }}>
        <h2>Extracted Text:</h2>
        <textarea 
          value={pdfText} 
          readOnly 
          style={{
            width: '100%', // Updated width to 80% of its container
            height: '300px',
            margin: '20px 0',
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            resize: 'none', // Optional: Prevents resizing the text area
          }}
        />
      </div>
    )}
  </div>
  );
};

export default Main;