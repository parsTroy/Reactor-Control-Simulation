# GitHub Pages Deployment Instructions

## Quick Deploy

1. **Copy these files to your repository root:**
   ```bash
   cp -r deploy/* ./
   ```

2. **Enable GitHub Pages:**
   - Go to repository Settings
   - Scroll to "Pages" section
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add GitHub Pages demo"
   git push origin main
   ```

4. **Access your demo:**
   - Visit: `https://yourusername.github.io/aeronuclear/`
   - Replace `yourusername` with your GitHub username

## What's Included

- Interactive 3D Reactor Visualization
- Real-time Power Monitoring Charts
- Safety System Status Display
- Emergency SCRAM Simulation
- Control Rod Animation
- Responsive Web Design
- No backend dependencies

## Customization

- Edit `index.html` for UI changes
- Modify `js/demo-simulation.js` for simulation behavior
- Update `js/reactor3d.js` for 3D visualization changes

## Performance

- Optimized for static hosting
- Minimal memory footprint
- 60 FPS animations
- Responsive design
