import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import STLViewer from './components/STLViewer';

const App = () => {
    const [stlUrl, setStlUrl] = useState(null);
    const [viewMode, setViewMode] = useState('upload');

    const handleUploadSuccess = (url) => {
        setStlUrl(url);
        setViewMode('viewer');
    };

    const handleReset = () => {
        setStlUrl(null);
        setViewMode('upload');
    };

    return (
        <div style={styles.appContainer}>
            <div style={styles.glow} /> {/* Background ambient glow */}
            
            <nav style={styles.nav}>
                <div style={styles.logo}>
                    <span style={styles.logoIcon}>✦</span>
                    <span style={styles.logoText}>SketchTo3D</span>
                </div>
                
            </nav>

            <main style={styles.main}>
                {viewMode === 'upload' ? (
                    <section style={styles.heroSection}>
                        <h1 style={styles.heroTitle}>Transform Sketches <br/>into <span style={styles.gradientText}>3D Realities</span></h1>
                        <p style={styles.heroSubtitle}>Upload a 2D sketch and let our neural engine reconstruct into STL assets in minutes.</p>
                        <div style={styles.card}>
                            <FileUploader onUploadSuccess={handleUploadSuccess} />
                        </div>
                    </section>
                ) : (
                    <div style={styles.viewerWrapper}>
                        <div style={styles.toolbar}>
                            <button onClick={handleReset} style={styles.backButton}>
                                ↺ New Generation
                            </button>
                            <a href={stlUrl} download="generation.stl" style={styles.downloadButton}>
                                Export STL
                            </a>
                        </div>
                        <div style={styles.viewerCard}>
                            <STLViewer stlUrl={stlUrl} />
                        </div>
                    </div>
                )}
            </main>

            <footer style={styles.footer}>
                Powered by Zero123++ & TripoSR Architecture
            </footer>
        </div>
    );
};

const styles = {
    appContainer: {
        minHeight: '100vh',
        backgroundColor: '#050505',
        color: '#e0e0e0',
        fontFamily: "'Inter', sans-serif",
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        overflowX: 'hidden'
    },
    glow: {
        position: 'absolute',
        top: '-10%',
        left: '50%',
        width: '80%',
        height: '40%',
        background: 'radial-gradient(circle, rgba(51, 153, 255, 0.1) 0%, transparent 70%)',
        transform: 'translateX(-50%)',
        pointerEvents: 'none'
    },
    nav: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '20px 60px',
        borderBottom: '1px solid rgba(255,255,255,0.05)'
    },
    logo: { display: 'flex', alignItems: 'center', gap: '10px' },
    logoIcon: { fontSize: '24px', color: '#3399ff' },
    logoText: { fontSize: '18px', fontWeight: '800', letterSpacing: '-0.5px' },
    badge: { fontSize: '10px', background: '#1a1a1a', padding: '4px 10px', borderRadius: '100px', color: '#666' },
    main: { flex: 1, display: 'flex', justifyContent: 'center', padding: '40px 20px' },
    heroSection: { textAlign: 'center', maxWidth: '800px', display: 'flex', flexDirection: 'column', alignItems: 'center' },
    heroTitle: { fontSize: '4rem', fontWeight: '900', lineHeight: '1.1', margin: '0 0 20px 0', letterSpacing: '-2px' },
    gradientText: { background: 'linear-gradient(90deg, #3399ff, #00ffcc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' },
    heroSubtitle: { fontSize: '1.1rem', color: '#888', marginBottom: '40px', maxWidth: '500px', lineHeight: '1.6' },
    card: {
        backgroundColor: 'rgba(20, 20, 20, 0.6)',
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: '24px',
        padding: '30px',
        width: '100%',
        maxWidth: '500px'
    },
    viewerWrapper: { width: '100%', maxWidth: '1000px', animation: 'fadeIn 0.5s ease' },
    viewerCard: {
        backgroundColor: '#000',
        borderRadius: '24px',
        overflow: 'hidden',
        border: '1px solid rgba(255,255,255,0.1)',
        boxShadow: '0 40px 100px rgba(0,0,0,0.8)'
    },
    toolbar: { display: 'flex', justifyContent: 'space-between', marginBottom: '20px', alignItems: 'center' },
    backButton: { background: 'none', border: 'none', color: '#888', cursor: 'pointer', fontWeight: '600' },
    downloadButton: { backgroundColor: '#3399ff', color: 'white', padding: '12px 24px', borderRadius: '12px', textDecoration: 'none', fontWeight: 'bold', fontSize: '0.9rem' },
    footer: { padding: '40px', textAlign: 'center', color: '#333', fontSize: '12px', letterSpacing: '1px', textTransform: 'uppercase' }
};

export default App;