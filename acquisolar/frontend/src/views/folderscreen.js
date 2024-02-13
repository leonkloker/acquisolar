// App.js
import React, { useState } from 'react';
import '../styles/folderscreen.css';
import '../icons/folder-icon.png';

// Example dictionary of folders and files
const initialFolders = {
  'Documents': ['doc1.txt', 'doc2.txt', 'report.pdf'],
  'Photos': ['photo1.jpg', 'photo2.png'],
  'Music': ['song1.mp3', 'song2.wav', 'album1.zip'],
};

const FolderIcon = ({ name, fileCount, onView }) => (
  <div className="folder-icon">
    <div className="folder-info">
      <img src="folder-icon.png" alt="Folder" />
      <p>{name}</p>
      <p>{fileCount} files</p>
    </div>
    <button onClick={onView}>Open</button>
  </div>
);

const Folder = () =>  {
  const [folders, setFolders] = useState([initialFolders]);

  const handleViewFolder = (folderName) => {
    // Logic to navigate to the folder's content view
    // For now, we'll just log the folder name to the console
    console.log(`Viewing contents of ${folderName}`);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Folder Viewer</h1>
        <div className="folder-grid">
          {Object.keys(folders).map((folderName) => (
            <FolderIcon
              key={folderName}
              name={folderName}
              fileCount={folders[folderName].length}
              onView={() => handleViewFolder(folderName)}
            />
          ))}
        </div>
      </header>
    </div>
  );
}

export default Folder;