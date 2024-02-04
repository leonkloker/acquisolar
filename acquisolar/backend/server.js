const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Set storage engine
const storage = multer.diskStorage({
  destination: './uploads/',
  filename: function(req, file, cb){
    cb(null, file.originalname);
  }
});

// Initialize upload
const upload = multer({
  storage: storage,
  fileFilter: function(req, file, cb){
    checkFileType(file, cb);
  }
}).array('files'); // 'files' is the fieldname that will be used in the form

// Check File Type
function checkFileType(file, cb){
  // Allowed ext
  const filetypes = /pdf/;
  // Check ext
  const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
  // Check mime
  const mimetype = filetypes.test(file.mimetype);

  if(mimetype && extname){
    return cb(null,true);
  } else {
    cb('Error: PDFs Only!');
  }
}

// Ensure upload directory exists
const uploadDir = './uploads';
if (!fs.existsSync(uploadDir)){
  fs.mkdirSync(uploadDir);
}

const app = express();

// Public Folder
app.use(express.static('./public'));

app.post('/upload', (req, res) => {
  console.log(req);
  upload(req, res, (err) => {
    if(err){
      res.status(500).send(err);
    } else {
      if(req.files === undefined){
        res.status(400).send('Error: No File Selected!');
      } else {
        console.log('Uploaded files:', req.files);
        res.send('File(s) Uploaded!');
      }
    }
  });
});

app.use(express.static(path.join(__dirname, '..', 'frontend', 'build')));

app.get('*', function(req, res) {
    res.sendFile(path.join(__dirname, '..', 'frontend', 'build', 'index.html'));
});

const port = 3000;

app.listen(port, () => console.log(`Server started on port ${port}`));