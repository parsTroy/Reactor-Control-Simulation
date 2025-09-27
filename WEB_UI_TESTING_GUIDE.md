# Nuclear Reactor Control Simulation - Web UI Testing Guide

## 🚀 **How to Test the Web UI**

### **1. Access the Web Interface**
Open your browser and go to: **http://localhost:5001**

### **2. What You Should See**
- **Modern, professional interface** with real-time reactor monitoring
- **Fixed charts** that don't grow off-screen (Y-axis: 0.0 to 2.0)
- **Control panel** with start/stop/reset buttons
- **Real-time metrics** display
- **Interactive controls** for power setpoint and PID gains

---

## 📊 **All Available Metrics & Features**

### **Real-Time Monitoring**
✅ **Current Power Level** - Shows reactor power (0.0 to 2.0 range)
✅ **Simulation Time** - Tracks elapsed simulation time
✅ **SCRAM Status** - Shows if safety systems are active
✅ **Data Points Counter** - Number of data points collected

### **Interactive Controls**
✅ **Start/Stop/Reset Simulation** - Control simulation state
✅ **Power Setpoint Slider** - Adjust target power (0.5 to 1.5)
✅ **PID Controller Settings** - Adjust Kp, Ki, Kd gains in real-time
✅ **Test Scenarios** - Pre-built scenarios for testing

### **Data Visualization**
✅ **Power vs Time Chart** - Real-time power monitoring (FIXED Y-axis: 0-2)
✅ **Safety Status Chart** - SCRAM status over time (FIXED Y-axis: -0.1 to 1.1)
✅ **Setpoint Line** - Shows target power level
✅ **Overpower Threshold** - Shows safety limit (1.2)

### **Data Export & Analysis**
✅ **CSV Export** - Download simulation data
✅ **Plot Generation** - Create high-quality plots
✅ **Configuration Management** - Save/load settings

---

## 🧪 **Step-by-Step Testing Procedure**

### **Phase 1: Basic Functionality**
1. **Open Browser** → http://localhost:5001
2. **Verify Interface** → Should see clean, professional dashboard
3. **Check Charts** → Should show empty charts with fixed Y-axis (0-2)
4. **Test Controls** → Buttons should be responsive

### **Phase 2: Simulation Testing**
1. **Click "Start Simulation"** → Should see:
   - Power level starts at 1.0
   - Time counter starts incrementing
   - Charts begin plotting data
   - Status shows "RUNNING"

2. **Watch Real-Time Updates** → Should see:
   - Power values updating every second
   - Charts plotting smoothly
   - Y-axis staying fixed at 0-2 range
   - Data points counter increasing

### **Phase 3: Control Testing**
1. **Adjust Power Setpoint** → Move slider from 0.5 to 1.5
   - Should see setpoint line move on chart
   - Power should try to follow setpoint

2. **Modify PID Gains** → Change Kp, Ki, Kd values
   - Should see immediate effect on control behavior
   - Power response should change

3. **Test Scenarios** → Click scenario buttons:
   - **Normal Operation** → Steady 1.0 power
   - **Power Ramp** → Gradual increase to 1.2
   - **Emergency SCRAM** → Rapid increase triggering safety

### **Phase 4: Safety System Testing**
1. **Watch for SCRAM** → If power exceeds 1.2:
   - SCRAM status should turn red
   - Safety chart should show "1" (active)
   - Power should be controlled

2. **Test Reset** → Click "Reset" button:
   - All data should clear
   - Charts should return to empty state
   - Time should reset to 0

### **Phase 5: Data Export Testing**
1. **Generate Data** → Let simulation run for 30+ seconds
2. **Export CSV** → Click "Download CSV" button
   - Should download file with time, power, SCRAM data
3. **Generate Plot** → Click "Generate Plot" button
   - Should show modal with high-quality plot

---

## ✅ **Expected Results**

### **Chart Behavior (FIXED)**
- ✅ Y-axis stays at 0.0 to 2.0 (never grows off-screen)
- ✅ Data points plot smoothly within bounds
- ✅ Charts update every second (1Hz)
- ✅ No infinite scaling or jumping

### **Simulation Behavior**
- ✅ Power starts at 1.0 and stabilizes
- ✅ PID controller responds to setpoint changes
- ✅ Safety systems activate when needed
- ✅ Data accumulates over time

### **Performance**
- ✅ Smooth, responsive interface
- ✅ No excessive API calls (1Hz updates)
- ✅ Charts render quickly
- ✅ No memory leaks or crashes

---

## 🔧 **Troubleshooting**

### **If Charts Still Grow Off-Screen**
- Hard refresh browser (Ctrl+F5)
- Check browser console for errors
- Verify JavaScript is loading correctly

### **If Simulation Won't Start**
- Check browser console for errors
- Verify C++ module is built
- Check Flask server logs

### **If Data Looks Wrong**
- Check browser console for data validation warnings
- Verify simulation is actually running
- Check Flask server for errors

---

## 📈 **Key Metrics to Verify**

### **Power Range**
- Normal operation: 0.8 to 1.2
- Setpoint changes: Should follow smoothly
- Safety limits: Should not exceed 2.0

### **Time Progression**
- Should increment smoothly
- Should not jump or reset unexpectedly
- Should correlate with data points

### **Safety Systems**
- SCRAM should activate at power > 1.2
- Status should be clearly visible
- Reset should clear all data

### **Chart Stability**
- Y-axis should NEVER change from 0-2
- Data should plot within bounds
- Charts should not resize or jump

---

## 🎯 **Success Criteria**

✅ **Charts are fixed and stable** (no growing off-screen)
✅ **All controls work** (start, stop, reset, sliders)
✅ **Real-time data updates** (power, time, status)
✅ **Safety systems function** (SCRAM activation)
✅ **Data export works** (CSV download, plot generation)
✅ **Performance is smooth** (1Hz updates, no lag)
✅ **Interface is professional** (clean, responsive design)

---

**The web UI now provides a complete, professional interface for testing and monitoring the nuclear reactor simulation with all relevant metrics and controls!** 🚀
