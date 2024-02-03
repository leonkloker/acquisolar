// server.js
const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const pdfParse = require('pdf-parse');
const path = require('path');

const app = express();

// Middleware
app.use(cors()); // to handle Cross-Origin Resource Sharing (CORS)
app.use(fileUpload());

// Serve any static files
app.use(express.static(path.join(__dirname, '..', 'frontend', 'build')));

// Upload Endpoint
app.post('/upload', (req, res) => {
  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  let uploadedPdf = req.files.pdf; // PDF TO BE SENT FOR RAG

  pdfParse(uploadedPdf.data).then(result => {
    res.json({ text: result.text });
  }).catch(error => {
    res.status(500).send('Error parsing PDF');
  });
});

app.get('*', function(req, res) {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'build', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));