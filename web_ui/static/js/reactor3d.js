// 3D Reactor Visualization using Three.js
// Real-time 3D representation of nuclear reactor

class Reactor3D {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.reactorCore = null;
        this.controlRods = [];
        this.powerIndicator = null;
        this.animationId = null;
        this.currentPower = 1.0;
        this.isScrammed = false;
        
        this.init();
    }
    
    init() {
        // Get container and canvas
        const container = document.getElementById('reactor3d-container');
        const canvas = document.getElementById('reactor3d-canvas');
        
        // Scene setup
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a1a);
        
        // Camera setup
        this.camera = new THREE.PerspectiveCamera(
            75, 
            container.clientWidth / container.clientHeight, 
            0.1, 
            1000
        );
        this.camera.position.set(5, 5, 5);
        
        // Renderer setup
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: canvas,
            antialias: true 
        });
        this.renderer.setSize(container.clientWidth, container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        
        // Controls setup
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.enableZoom = true;
        this.controls.enablePan = true;
        
        // Lighting
        this.setupLighting();
        
        // Create reactor components
        this.createReactorCore();
        this.createControlRods();
        this.createPowerIndicator();
        this.createEnvironment();
        
        // Start animation loop
        this.animate();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);
        
        // Point light for reactor glow
        const pointLight = new THREE.PointLight(0x00ff00, 1, 100);
        pointLight.position.set(0, 0, 0);
        this.scene.add(pointLight);
    }
    
    createReactorCore() {
        // Main reactor vessel
        const coreGeometry = new THREE.CylinderGeometry(1.5, 1.5, 3, 32);
        const coreMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x333333,
            transparent: true,
            opacity: 0.8
        });
        this.reactorCore = new THREE.Mesh(coreGeometry, coreMaterial);
        this.reactorCore.position.y = 0;
        this.reactorCore.castShadow = true;
        this.reactorCore.receiveShadow = true;
        this.scene.add(this.reactorCore);
        
        // Reactor core interior (fuel rods)
        const fuelGeometry = new THREE.CylinderGeometry(1.2, 1.2, 2.8, 16);
        const fuelMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x444444,
            transparent: true,
            opacity: 0.9
        });
        const fuelCore = new THREE.Mesh(fuelGeometry, fuelMaterial);
        fuelCore.position.y = 0;
        this.scene.add(fuelCore);
        
        // Add fuel rod details
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const radius = 0.8;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            
            const rodGeometry = new THREE.CylinderGeometry(0.05, 0.05, 2.5, 8);
            const rodMaterial = new THREE.MeshPhongMaterial({ color: 0x666666 });
            const fuelRod = new THREE.Mesh(rodGeometry, rodMaterial);
            fuelRod.position.set(x, 0, z);
            this.scene.add(fuelRod);
        }
    }
    
    createControlRods() {
        // Create control rods around the reactor
        for (let i = 0; i < 6; i++) {
            const angle = (i / 6) * Math.PI * 2;
            const radius = 2.2;
            const x = Math.cos(angle) * radius;
            const z = Math.sin(angle) * radius;
            
            const rodGeometry = new THREE.CylinderGeometry(0.1, 0.1, 2, 8);
            const rodMaterial = new THREE.MeshPhongMaterial({ color: 0x888888 });
            const controlRod = new THREE.Mesh(rodGeometry, rodMaterial);
            controlRod.position.set(x, 1, z);
            controlRod.userData = { index: i, originalY: 1 };
            this.controlRods.push(controlRod);
            this.scene.add(controlRod);
        }
    }
    
    createPowerIndicator() {
        // Power level indicator (glowing sphere inside reactor)
        const indicatorGeometry = new THREE.SphereGeometry(0.3, 16, 16);
        const indicatorMaterial = new THREE.MeshPhongMaterial({ 
            color: 0x00ff00,
            transparent: true,
            opacity: 0.8,
            emissive: 0x004400
        });
        this.powerIndicator = new THREE.Mesh(indicatorGeometry, indicatorMaterial);
        this.powerIndicator.position.y = 0;
        this.scene.add(this.powerIndicator);
    }
    
    createEnvironment() {
        // Floor
        const floorGeometry = new THREE.PlaneGeometry(20, 20);
        const floorMaterial = new THREE.MeshPhongMaterial({ color: 0x222222 });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.position.y = -2;
        floor.receiveShadow = true;
        this.scene.add(floor);
        
        // Walls (optional)
        const wallGeometry = new THREE.PlaneGeometry(20, 10);
        const wallMaterial = new THREE.MeshPhongMaterial({ color: 0x333333 });
        
        // Back wall
        const backWall = new THREE.Mesh(wallGeometry, wallMaterial);
        backWall.position.set(0, 3, -10);
        this.scene.add(backWall);
        
        // Side walls
        const leftWall = new THREE.Mesh(wallGeometry, wallMaterial);
        leftWall.position.set(-10, 3, 0);
        leftWall.rotation.y = Math.PI / 2;
        this.scene.add(leftWall);
        
        const rightWall = new THREE.Mesh(wallGeometry, wallMaterial);
        rightWall.position.set(10, 3, 0);
        rightWall.rotation.y = -Math.PI / 2;
        this.scene.add(rightWall);
    }
    
    updatePower(power, scramStatus) {
        console.log('Reactor3D.updatePower called with:', { power, scramStatus });
        this.currentPower = power;
        this.isScrammed = scramStatus;
        
        // Update power indicator color and intensity
        if (this.powerIndicator) {
            if (scramStatus) {
                // SCRAM - red color
                this.powerIndicator.material.color.setHex(0xff0000);
                this.powerIndicator.material.emissive.setHex(0x440000);
            } else if (power > 1.05) {  // Lowered threshold for more sensitivity
                // High power - orange color
                this.powerIndicator.material.color.setHex(0xff8800);
                this.powerIndicator.material.emissive.setHex(0x442200);
            } else if (power > 0.95) {  // Narrower normal range
                // Normal power - green color
                this.powerIndicator.material.color.setHex(0x00ff00);
                this.powerIndicator.material.emissive.setHex(0x004400);
            } else {
                // Low power - blue color
                this.powerIndicator.material.color.setHex(0x0088ff);
                this.powerIndicator.material.emissive.setHex(0x002244);
            }
            
            // Scale based on power level
            const scale = 0.5 + (power * 0.5);
            this.powerIndicator.scale.setScalar(scale);
        }
        
                // Update control rod positions based on power
                this.controlRods.forEach((rod, index) => {
                    if (scramStatus) {
                        // SCRAM - rods fully inserted
                        rod.position.y = rod.userData.originalY - 1.5;
                    } else {
                        // Normal operation - rods partially inserted based on power
                        // More dramatic movement for visibility
                        const insertion = (1.0 - power) * 2.0;  // Increased from 1.5 to 2.0
                        rod.position.y = rod.userData.originalY - insertion;
                    }
                });
        
        // Update reactor core glow
        if (this.reactorCore) {
            const intensity = scramStatus ? 0.1 : power * 0.5;
            this.reactorCore.material.emissive.setHex(0x000000);
            this.reactorCore.material.emissive.setHex(
                scramStatus ? 0x220000 : 
                power > 1.1 ? 0x221100 : 
                power > 0.9 ? 0x002200 : 0x000022
            );
        }
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        // Update controls
        this.controls.update();
        
        // Rotate reactor core slowly
        if (this.reactorCore) {
            this.reactorCore.rotation.y += 0.005;
        }
        
        // Animate power indicator
        if (this.powerIndicator) {
            this.powerIndicator.rotation.x += 0.01;
            this.powerIndicator.rotation.y += 0.01;
        }
        
        // Render
        this.renderer.render(this.scene, this.camera);
    }
    
    onWindowResize() {
        const container = document.getElementById('reactor3d-container');
        const width = container.clientWidth;
        const height = container.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
    
    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// Global 3D reactor instance
let reactor3D = null;

// Initialize 3D reactor when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for the container to be ready
    setTimeout(() => {
        try {
            reactor3D = new Reactor3D();
            console.log('3D Reactor visualization initialized');
            
            // Test the 3D reactor with initial values
            if (reactor3D) {
                reactor3D.updatePower(1.0, false);
                console.log('3D Reactor test update sent');
            }
        } catch (error) {
            console.error('Error initializing 3D reactor:', error);
        }
    }, 500);
});

// Function to update 3D reactor from main app
function updateReactor3D(power, scramStatus) {
    // Only log occasionally to reduce console spam
    if (Math.random() < 0.05) {
        console.log('updateReactor3D called with:', { power, scramStatus, reactor3D: !!reactor3D });
    }
    if (reactor3D) {
        reactor3D.updatePower(power, scramStatus);
        if (Math.random() < 0.05) {
            console.log('3D Reactor updated successfully');
        }
    } else {
        console.warn('3D Reactor not initialized yet');
    }
}
