# Nuclear Reactor Control Simulation - GitHub Pages Demo

This is a **static demonstration** of the Nuclear Reactor Control Simulation project, designed to run on GitHub Pages.

## Live Demo

Visit the live demo at: `https://yourusername.github.io/aeronuclear/`

## What This Demo Shows

### Interactive Features:
- **3D Reactor Visualization** - Interactive Three.js 3D model
- **Real-time Charts** - Power monitoring and safety status
- **Control Panel** - Start/stop/reset simulation
- **Test Scenarios** - Normal operation, power ramp, emergency SCRAM
- **Responsive Design** - Works on desktop and mobile

### Visual Demonstrations:
- **Normal Operation**: Green power indicator, normal control rod position
- **Power Ramp**: Orange power indicator, increased control rod insertion
- **Emergency SCRAM**: Red power indicator, full control rod insertion

## Technologies Used

### **Frontend:**
- **Three.js** - 3D graphics and visualization
- **Chart.js** - Real-time data visualization
- **Bootstrap 5** - Responsive UI framework
- **Vanilla JavaScript** - No external dependencies

### **Backend (Full Version):**
- **C++** - High-performance reactor physics engine
- **Python** - Pybind11 integration and web server
- **Flask-SocketIO** - Real-time WebSocket communication
- **CMake** - Cross-platform build system

## File Structure

```
github-pages/
├── index.html              # Main demo page
├── js/
│   ├── reactor3d.js        # 3D visualization engine
│   └── demo-simulation.js  # Simulated reactor behavior
└── README.md               # This file
```

## Deployment Instructions

### **1. Enable GitHub Pages**
1. Go to your repository settings
2. Scroll to "Pages" section
3. Select "Deploy from a branch"
4. Choose "main" branch and "/ (root)" folder
5. Click "Save"

### **2. Move Files to Root**
```bash
# Copy the github-pages folder contents to repository root
cp -r github-pages/* ./
```

### **3. Update Repository URL**
Edit `index.html` and update the GitHub repository URL:
```html
<a href="https://github.com/yourusername/aeronuclear" class="btn btn-primary">
```

### **4. Commit and Push**
```bash
git add .
git commit -m "Add GitHub Pages demo"
git push origin main
```

## Demo Features

### 3D Reactor Visualization
- Interactive 3D model with mouse controls
- Real-time power level indicators
- Dynamic control rod positioning
- Visual SCRAM emergency state

### Real-time Monitoring
- Power level charts with setpoint and threshold lines
- Safety system status display
- Time progression tracking
- Responsive chart updates

### Control Interface
- Start/stop/reset simulation controls
- Power setpoint adjustment slider
- Test scenario buttons
- Real-time status indicators

## Customization

### **Modify Simulation Behavior**
Edit `js/demo-simulation.js`:
- Adjust time step: `this.timeStep = 0.1`
- Change power variation: `variation = 0.05 * Math.sin(...)`
- Modify SCRAM behavior: `simulateScram()` function

### **Update 3D Visualization**
Edit `js/reactor3d.js`:
- Change colors and materials
- Adjust control rod movement
- Modify power indicator behavior

### **Styling Changes**
Edit `index.html`:
- Update Bootstrap classes
- Modify CSS styles
- Change layout structure

## Performance Notes

- **Charts**: Limited to 100 data points for smooth performance
- **3D Graphics**: Optimized for web browsers
- **Animation**: 60 FPS with requestAnimationFrame
- **Memory**: Minimal memory footprint

## Full Implementation

This demo showcases the visual and interactive components. The complete implementation includes:

- **C++ Nuclear Reactor Physics Engine**
- **Python Pybind11 Integration**
- **Flask WebSocket Server**
- **Real-time Data Streaming**
- **Advanced Safety Systems**
- **PID Control Algorithms**

## 📝 **License**

This project is open source. See the main repository for license details.

## 🤝 **Contributing**

Contributions are welcome! Please see the main repository for contribution guidelines.

---

**Note**: This is a static demonstration. For the full interactive simulation with real-time C++ physics, please refer to the main repository.
