const express = require('express');
const multer = require('multer');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
app.use(cors());


app.use('/outputs', express.static(path.join(__dirname, 'outputs'))); 


if (!fs.existsSync('./uploads')) fs.mkdirSync('./uploads');
if (!fs.existsSync('./outputs')) fs.mkdirSync('./outputs');

const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'),
    filename: (req, file, cb) => cb(null, Date.now() + '-' + file.originalname)
});
const upload = multer({ storage });

app.post('/api/generate', upload.single('sketch'), (req, res) => {
    if (!req.file) return res.status(400).send('No file uploaded.');

    const jobId = Date.now();
    const inputPath = path.resolve(req.file.path);
    const outputPath = path.resolve(__dirname, 'outputs', `${jobId}.stl`);

    
    const pythonPath = "D:\\pythonenvironments\\SketchTo3D\\Scripts\\python.exe";
    const scriptPath = "D:\\python\\3D_Model_Gen\\ai_engine\\scripts\\master_pipeline.py";

    console.log(`🚀 Starting AI Engine for Job: ${jobId}`);

    const pythonProcess = spawn(pythonPath, [
        scriptPath,
        '--input', inputPath,
        '--output', outputPath,
        '--type', 'sketch',
        '--multiview', 'False'
    ]);

    
    pythonProcess.stdout.on('data', (data) => {
        console.log(`[Python]: ${data.toString()}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`[Python Error]: ${data.toString()}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`[System]: AI Process exited with code ${code}`);
    });

    res.json({ jobId, status: 'processing' });
});

app.get('/api/status/:id', (req, res) => {
    const filePath = path.join(__dirname, 'outputs', `${req.params.id}.stl`);
    if (fs.existsSync(filePath)) {
        res.json({ status: 'done', stlUrl: `http://localhost:5000/outputs/${req.params.id}.stl` });
    } else {
        res.json({ status: 'processing' });
    }
});

app.listen(5000, () => console.log('Server running on http://localhost:5000'));