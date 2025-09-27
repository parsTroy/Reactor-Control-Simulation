#!/bin/bash

# GitHub Pages Deployment Script
# This script prepares the project for GitHub Pages deployment

echo "Preparing Nuclear Reactor Control Simulation for GitHub Pages deployment..."

# Check if we're in the right directory
if [ ! -f "CMakeLists.txt" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Create deployment directory
echo "Creating deployment directory..."
rm -rf deploy
mkdir -p deploy

# Copy GitHub Pages files
echo "Copying GitHub Pages files..."
cp -r github-pages/* deploy/

# Update repository URL in index.html (replace with your actual GitHub username)
echo "Updating repository URL..."
sed -i.bak 's/yourusername/aeronuclear/g' deploy/index.html
rm deploy/index.html.bak

# Create .nojekyll file to bypass Jekyll processing
echo "Creating .nojekyll file..."
touch deploy/.nojekyll

# Create deployment instructions
echo "Creating deployment instructions..."
cat > deploy/DEPLOYMENT_INSTRUCTIONS.md << 'EOF'
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
EOF

echo "GitHub Pages deployment files created in 'deploy/' directory"
echo ""
echo "Next steps:"
echo "1. Copy the contents of 'deploy/' to your repository root"
echo "2. Enable GitHub Pages in your repository settings"
echo "3. Commit and push the changes"
echo "4. Visit your live demo at: https://yourusername.github.io/aeronuclear/"
echo ""
echo "Files created:"
echo "   - deploy/index.html (main demo page)"
echo "   - deploy/js/reactor3d.js (3D visualization)"
echo "   - deploy/js/demo-simulation.js (simulation logic)"
echo "   - deploy/.nojekyll (bypass Jekyll processing)"
echo "   - deploy/DEPLOYMENT_INSTRUCTIONS.md (deployment guide)"
echo ""
echo "Ready for GitHub Pages deployment!"
