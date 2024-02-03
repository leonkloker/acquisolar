import React, { useCallback, useState } from 'react';
import "../App.css";

const Main = () => {
  const [fileName, setFileName] = useState('');
  const [pdfText, setPdfText] = useState(''); 

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('pdf', file);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setPdfText(data.text); 
    } catch (error) {
      console.error('Error:', error);
      setPdfText('');
    }
  };

  const handleFileSelect = useCallback((event) => {
    event.preventDefault(); // Prevents browser from opening file
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
<div className="container">
  <div className="drop-box" onDrop={handleFileSelect} onDragOver={onDragOver}>
    Drag and drop a file here or click to select a file
    <input
      type="file"
      accept="application/pdf"
      onChange={handleFileSelect}
      onClick={(event) => event.stopPropagation()}
    />
    {fileName && <p>File name: {fileName}</p>}
  </div>
  {/* Text area container for extracted text */}
  {pdfText && (
    <div className="pdf-text-container">
      <h2>Extracted Text:</h2>
      <textarea value={pdfText} readOnly />
    </div>
  )}
</div>
  );
};

export default Main;