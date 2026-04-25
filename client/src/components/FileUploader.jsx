import React, { useState } from 'react';
import axios from 'axios';
import { Upload, CheckCircle, Loader2, AlertCircle, FileText } from 'lucide-react';

const FileUploader = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('idle');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setStatus('idle');
    };

    const startGeneration = async () => {
        if (!file) return;
        setStatus('uploading');
        const formData = new FormData();
        formData.append('sketch', file);

        try {
            const response = await axios.post('http://localhost:5000/api/generate', formData);
            setStatus('processing');
            pollStatus(response.data.jobId);
        } catch (err) {
            setStatus('error');
        }
    };

    const pollStatus = (id) => {
        const interval = setInterval(async () => {
            try {
                const res = await axios.get(`http://localhost:5000/api/status/${id}`);
                if (res.data.status === 'done') {
                    clearInterval(interval);
                    setStatus('success');
                    onUploadSuccess(res.data.stlUrl);
                }
            } catch (err) {
                clearInterval(interval);
                setStatus('error');
            }
        }, 3000);
    };

    return (
        <div style={styles.container}>
            <input type="file" onChange={handleFileChange} id="fileInput" hidden />
            <label htmlFor="fileInput" style={{...styles.dropZone, borderColor: file ? '#3399ff' : '#333'}}>
                {file ? <FileText size={40} color="#3399ff" /> : <Upload size={40} color="#444" />}
                <p style={styles.dropText}>{file ? file.name : "Drag your sketch here"}</p>
                <span style={styles.dropSubtext}>Supports PNG, JPG (Max 10MB)</span>
            </label>

            <button 
                onClick={startGeneration} 
                disabled={!file || status === 'processing' || status === 'uploading'}
                style={{
                    ...styles.button, 
                    opacity: (!file || status === 'processing') ? 0.5 : 1,
                    background: status === 'error' ? '#ff4444' : '#3399ff'
                }}
            >
                {status === 'processing' ? (
                    <><Loader2 className="spinner" size={18}/> generating in 10 minutes...</>
                ) : status === 'uploading' ? (
                    "Uploading..."
                ) : "Generate 3D Asset"}
            </button>

            {status !== 'idle' && (
                <div style={styles.statusArea}>
                    {status === 'processing' && <div className="progress-bar-container"><div className="progress-bar-fill"></div></div>}
                    {status === 'error' && <p style={{color: '#ff4444'}}><AlertCircle size={14}/> Pipeline Connection Failed</p>}
                </div>
            )}
        </div>
    );
};

const styles = {
    container: { display: 'flex', flexDirection: 'column', gap: '20px' },
    dropZone: { 
        border: '2px dashed', 
        padding: '50px 20px', 
        borderRadius: '20px', 
        cursor: 'pointer', 
        textAlign: 'center', 
        transition: 'all 0.3s ease',
        background: 'rgba(255,255,255,0.02)'
    },
    dropText: { fontSize: '16px', fontWeight: '600', margin: '15px 0 5px 0' },
    dropSubtext: { fontSize: '12px', color: '#555' },
    button: { 
        padding: '16px', 
        color: 'white', 
        border: 'none', 
        borderRadius: '14px', 
        cursor: 'pointer', 
        fontSize: '16px', 
        fontWeight: 'bold',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '10px',
        transition: 'all 0.2s ease'
    },
    statusArea: { textAlign: 'center', marginTop: '10px' }
};

export default FileUploader;