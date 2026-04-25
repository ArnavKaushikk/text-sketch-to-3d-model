import React, { useEffect, useRef } from 'react';
import { 
    Engine, 
    Scene, 
    ArcRotateCamera, 
    Vector3, 
    HemisphericLight, 
    DirectionalLight,
    SceneLoader, 
    PBRMaterial, 
    Color3,
    EnvironmentHelper
} from '@babylonjs/core';
import "@babylonjs/loaders/STL";

const STLViewer = ({ stlUrl }) => {
    const canvasRef = useRef(null);

    useEffect(() => {
        if (!canvasRef.current || !stlUrl) return;

        const engine = new Engine(canvasRef.current, true, { preserveDrawingBuffer: true, stencil: true });
        const scene = new Scene(engine);
        
        
        scene.clearColor = new Color3(0.1, 0.1, 0.12);

        const camera = new ArcRotateCamera(
            "camera", 
            Math.PI / 2, 
            Math.PI / 3, 
            10, 
            Vector3.Zero(), 
            scene
        );
        camera.attachControl(canvasRef.current, true);
        camera.wheelPrecision = 50; 

        
        
        const light = new HemisphericLight("hemiLight", new Vector3(0, 1, 0), scene);
        light.intensity = 0.5;
        light.groundColor = new Color3(0.1, 0.1, 0.1);

        
        const dirLight = new DirectionalLight("dirLight", new Vector3(-1, -2, -1), scene);
        dirLight.position = new Vector3(10, 20, 10);
        dirLight.intensity = 1.5;

        
        const envHelper = scene.createDefaultEnvironment({
            createGround: true,
            groundSize: 100,
            groundColor: new Color3(0.2, 0.2, 0.2),
            createSkybox: false,
        });

        SceneLoader.ImportMesh(
            "", 
            "", 
            stlUrl, 
            scene, 
            (meshes) => {
                const mesh = meshes[0];
                
                
                scene.createDefaultCameraOrLight(true, true, true);
                scene.activeCamera.alpha += Math.PI; 

                
                const pbr = new PBRMaterial("pbr", scene);
                pbr.albedoColor = new Color3(0.1, 0.4, 0.9); 
                pbr.metallic = 0.8;    
                pbr.roughness = 0.2;   
                pbr.useAlphaFromAlbedoTexture = true;
                
                mesh.material = pbr;

                
                scene.registerBeforeRender(() => {
                    mesh.rotation.y += 0.005;
                });
            },
            null,
            (scene, message) => console.error("Babylon Error:", message)
        );

        engine.runRenderLoop(() => scene.render());
        const handleResize = () => engine.resize();
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            engine.dispose();
        };
    }, [stlUrl]);

    return (
        <div style={{ width: '100%', height: '500px', position: 'relative' }}>
            <canvas 
                ref={canvasRef} 
                style={{ width: '100%', height: '100%', outline: 'none', borderRadius: '12px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }} 
            />
            <div style={styles.overlay}>3D Real-time Preview</div>
        </div>
    );
};

const styles = {
    overlay: {
        position: 'absolute',
        top: '15px',
        right: '25px',
        color: 'white',
        backgroundColor: 'rgba(255,255,255,0.1)',
        backdropFilter: 'blur(5px)',
        border: '1px solid rgba(255,255,255,0.2)',
        padding: '6px 15px',
        borderRadius: '20px',
        fontSize: '11px',
        fontWeight: 'bold',
        textTransform: 'uppercase',
        letterSpacing: '1px'
    }
};

export default STLViewer;