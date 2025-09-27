# GitHub Pages Deployment Guide

## Overview

This guide explains how to deploy the Nuclear Reactor Control Simulation as a static demo on GitHub Pages. The demo showcases all the visual and interactive components without requiring a backend server.

## What's Included in the Demo

### Interactive Features
- **3D Reactor Visualization** - Interactive Three.js 3D model with mouse controls
- **Real-time Charts** - Power monitoring and safety status charts
- **Control Panel** - Start/stop/reset simulation controls
- **Test Scenarios** - Normal operation, power ramp, emergency SCRAM
- **Responsive Design** - Works on desktop and mobile devices

### Visual Demonstrations
- **Normal Operation**: Green power indicator, normal control rod position
- **Power Ramp**: Orange power indicator, increased control rod insertion  
- **Emergency SCRAM**: Red power indicator, full control rod insertion

## Quick Deployment

### Step 1: Run the Deployment Script
```bash
cd /Users/troyparsons/Developer/portfolio/aeronuclear/Reactor-Control-Simulation
./deploy-github-pages.sh
```

### Step 2: Copy Files to Repository Root
```bash
cp -r deploy/* ./
```

### Step 3: Enable GitHub Pages
1. Go to your GitHub repository
2. Click on "Settings" tab
3. Scroll down to "Pages" section
4. Under "Source", select "Deploy from a branch"
5. Choose "main" branch and "/ (root)" folder
6. Click "Save"

### Step 4: Commit and Push
```bash
git add .
git commit -m "Add GitHub Pages demo"
git push origin main
```

### Step 5: Access Your Demo
Visit: `https://yourusername.github.io/aeronuclear/`

## Manual Deployment

If you prefer to set up manually:

### 1. Create Required Files
- `index.html` - Main demo page
- `js/reactor3d.js` - 3D visualization engine
- `js/demo-simulation.js` - Simulated reactor behavior
- `.nojekyll` - Bypass Jekyll processing

### 2. Update Repository URL
Edit `index.html` and replace `yourusername` with your actual GitHub username:
```html
<a href="https://github.com/yourusername/aeronuclear" class="btn btn-primary">
```

### 3. Enable GitHub Pages
Follow the same steps as in the quick deployment section.

## File Structure

```
your-repository/
├── index.html              # Main demo page
├── js/
│   ├── reactor3d.js        # 3D visualization engine
│   └── demo-simulation.js  # Simulated reactor behavior
├── .nojekyll               # Bypass Jekyll processing
└── ... (other project files)
```

## Customization

### Modify Simulation Behavior
Edit `js/demo-simulation.js`:
- Adjust time step: `this.timeStep = 0.1`
- Change power variation: `variation = 0.05 * Math.sin(...)`
- Modify SCRAM behavior: `simulateScram()` function

### Update 3D Visualization
Edit `js/reactor3d.js`:
- Change colors and materials
- Adjust control rod movement
- Modify power indicator behavior

### Styling Changes
Edit `index.html`:
- Update Bootstrap classes
- Modify CSS styles
- Change layout structure

## Performance Optimization

### Charts
- Limited to 100 data points for smooth performance
- Disabled animations for better performance
- Fixed chart bounds to prevent scaling issues

### 3D Graphics
- Optimized for web browsers
- Uses requestAnimationFrame for smooth 60 FPS
- Minimal memory footprint

### General
- No external dependencies beyond CDN resources
- Responsive design for all screen sizes
- Static hosting compatible

## Troubleshooting

### Common Issues

**Demo not loading:**
- Check that all files are in the repository root
- Verify `.nojekyll` file exists
- Ensure GitHub Pages is enabled

**3D visualization not working:**
- Check browser console for JavaScript errors
- Verify Three.js CDN is loading
- Test in different browsers

**Charts not updating:**
- Check browser console for Chart.js errors
- Verify data is being generated correctly
- Test with different browsers

### Browser Compatibility
- Chrome/Chromium: Full support
- Firefox: Full support
- Safari: Full support
- Edge: Full support
- Mobile browsers: Responsive design

## Technical Details

### Technologies Used
- **Three.js** - 3D graphics and visualization
- **Chart.js** - Real-time data visualization
- **Bootstrap 5** - Responsive UI framework
- **Vanilla JavaScript** - No external dependencies

### Limitations
- Static simulation (no real physics)
- No persistent data storage
- No user authentication
- No real-time collaboration

### Advantages
- No server required
- Fast loading times
- Easy to deploy
- Professional appearance
- Mobile responsive

## Full Implementation

This demo showcases the visual and interactive components. The complete implementation includes:

- **C++ Nuclear Reactor Physics Engine**
- **Python Pybind11 Integration**
- **Flask WebSocket Server**
- **Real-time Data Streaming**
- **Advanced Safety Systems**
- **PID Control Algorithms**

## Support

For issues with the demo or full implementation:
1. Check the browser console for errors
2. Verify all files are properly deployed
3. Test in different browsers
4. Refer to the main repository documentation

## License

This project is open source. See the main repository for license details.
