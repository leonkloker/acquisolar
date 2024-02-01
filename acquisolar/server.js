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

// Upload Endpoint
app.post('/upload', (req, res) => {
  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  let uploadedPdf = req.files.pdf;

  pdfParse(uploadedPdf.data).then(result => {
    res.json({ text: result.text });
  }).catch(error => {
    res.status(500).send('Error parsing PDF');
  });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname+'/build/index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));