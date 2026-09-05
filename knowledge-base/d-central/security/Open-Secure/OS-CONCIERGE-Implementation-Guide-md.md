---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 1e6c6a4b-769b-4e4a-939e-727f99cb7cbd
original_filename: OS-CONCIERGE_Implementation_Guide.md
created_at: 2026-03-04T20:34:59.474352+00:00
content_hash: 60f8c59528fd
topic: "opensecure-per-service-implementation-guides"
---

# OS-CONCIERGE Implementation Guide
## Visitor Management & Property Concierge System Deployment

**Document Type**: Implementation Guide  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Property Managers, IT Teams, Kiosk Integrators

---

## Executive Summary

**Deployment Timeline**: 1-2 days per property  
**Team Required**: 2 technicians (IT + Assembly)  
**Cost per Kiosk**: $1,500-$3,000  
**Scalability**: 1 to 100+ properties per cloud instance

### Phase Overview

| Phase | Duration | Team | Deliverable |
|-------|----------|------|-------------|
| Hardware Assembly | 2-3 hours | 1 Technician | Kiosk physically built |
| Network Setup | 1 hour | IT Specialist | Connected to network |
| Software Install | 2 hours | IT Specialist | OS + kiosk app running |
| Cloud Config | 2 hours | IT Specialist | Backend operational |
| Testing | 1 hour | Full team | Check-in flow working |
| Training | 1 hour | Property Staff | Staff trained on system |

---

## Pre-Deployment Planning

### Property Assessment

**Kiosk Placement Checklist:**
```
LOCATION REQUIREMENTS
☐ High-visibility area (main entrance/lobby)
☐ Accessible to visitors (ADA compliant)
☐ Protected from weather (if outdoor)
☐ Near power outlet (within 10 feet)
☐ Network connectivity available (Ethernet or WiFi)
☐ Adequate lighting (no glare on touchscreen)
☐ Space for visitor queue (6+ feet in front)
☐ Security camera coverage (recommended)

PHYSICAL REQUIREMENTS
☐ Floor space: 24" × 24" (floor stand)
☐ Wall space: 18" × 30" (wall mount)
☐ Clearance: 48" in front (ADA)
☐ Mounting surface: Solid (wall) or level (floor)
☐ Weight: 50-100 lbs (floor stand with ballast)

CONNECTIVITY
☐ Power: 120V AC outlet, 15A circuit
☐ Network: Ethernet (preferred) or WiFi
☐ Bandwidth: 10 Mbps minimum, 50 Mbps recommended
☐ Internet: Required for cloud sync

INTEGRATION POINTS
☐ Property management system (PMS) API available?
☐ Access control system integration needed?
☐ Existing badge printer?
☐ Calendar integration (Outlook/Google)?
☐ SMS/Email notification service?
```

### Hardware Selection Guide

**Kiosk Configurations:**
```
BASIC CONFIGURATION ($1,500)
├── Purpose: Simple check-in, low traffic
├── Touchscreen: 24" capacitive, 1080p
├── Computer: Intel NUC i5, 8GB RAM, 256GB SSD
├── Webcam: 1080p, 30fps
├── Scanner: 1D/2D barcode
├── Printer: Thermal badge printer
├── Mount: Floor stand (basic)
└── Use case: Small office (<50 visitors/day)

STANDARD CONFIGURATION ($2,200)
├── Purpose: Full-featured, medium traffic
├── Touchscreen: 27" capacitive, 1080p
├── Computer: Intel NUC i5, 16GB RAM, 512GB SSD
├── Webcam: 4K, 60fps
├── Scanner: 2D barcode + NFC reader
├── Printer: Thermal + label printer combo
├── Mount: Weighted floor stand
├── Accessories: Stylus, hand sanitizer dispenser
└── Use case: Corporate office (50-200 visitors/day)

PREMIUM CONFIGURATION ($3,000)
├── Purpose: High-end, high traffic, branded
├── Touchscreen: 32" 4K capacitive
├── Computer: Intel NUC i7, 16GB RAM, 1TB SSD
├── Webcam: 4K, 60fps, auto-focus
├── Scanner: 2D barcode + NFC + RFID
├── Printer: Dual (thermal badges + shipping labels)
├── Speakers: Stereo (greeting audio)
├── Mount: Custom branded enclosure
├── Accessories: Logo lighting, sanitizer, stylus
└── Use case: Luxury property (200+ visitors/day)

OUTDOOR CONFIGURATION ($4,500)
├── Purpose: Weatherproof, 24/7 operation
├── Touchscreen: 32" sunlight-readable, IP65
├── Computer: Fanless industrial PC
├── Webcam: Weatherproof, IR night vision
├── Scanner: Industrial 2D, weatherproof
├── Printer: Weatherproof thermal printer
├── Enclosure: NEMA 4X stainless steel
├── Heating/Cooling: Climate control system
├── Vandal resistance: Gorilla glass, reinforced
└── Use case: Parking gates, outdoor facilities
```

### Bill of Materials

```python
def calculate_concierge_bom(num_kiosks, config_type='standard'):
    """Calculate complete system cost"""
    
    # Hardware costs per kiosk
    hardware_configs = {
        'basic': {
            'touchscreen_24': 400,
            'nuc_i5_8gb': 500,
            'webcam_1080p': 80,
            'barcode_scanner': 120,
            'thermal_printer': 200,
            'floor_stand': 150,
            'cables': 50,
            'total': 1500
        },
        'standard': {
            'touchscreen_27': 600,
            'nuc_i5_16gb': 650,
            'webcam_4k': 150,
            'scanner_nfc': 180,
            'dual_printer': 350,
            'weighted_stand': 200,
            'accessories': 70,
            'total': 2200
        },
        'premium': {
            'touchscreen_32_4k': 900,
            'nuc_i7_16gb': 800,
            'webcam_4k_pro': 200,
            'scanner_rfid': 250,
            'dual_printer_pro': 450,
            'custom_enclosure': 600,
            'branding': 200,
            'accessories': 100,
            'total': 3500
        },
        'outdoor': {
            'touchscreen_sunlight': 1800,
            'industrial_pc': 1200,
            'weatherproof_camera': 300,
            'industrial_scanner': 400,
            'weatherproof_printer': 500,
            'nema_enclosure': 1000,
            'climate_control': 600,
            'installation': 500,
            'total': 6300
        }
    }
    
    # Cloud platform (monthly recurring per property)
    cloud_costs = {
        'small': {  # 1-5 kiosks
            'compute': 24,      # DigitalOcean 4GB
            'database': 9,      # MongoDB Atlas
            'storage': 3,       # S3 100GB
            'sms': 20,         # Twilio
            'email': 10,       # SendGrid
            'total': 66
        },
        'medium': {  # 6-25 kiosks
            'compute': 48,
            'database': 25,
            'storage': 10,
            'sms': 50,
            'email': 20,
            'total': 153
        },
        'large': {  # 26-100 kiosks
            'compute': 96,
            'database': 57,
            'storage': 25,
            'sms': 100,
            'email': 40,
            'total': 318
        }
    }
    
    # Calculate hardware total
    config = hardware_configs[config_type]
    hardware_total = config['total'] * num_kiosks
    
    # Select cloud tier
    if num_kiosks <= 5:
        cloud_tier = cloud_costs['small']
    elif num_kiosks <= 25:
        cloud_tier = cloud_costs['medium']
    else:
        cloud_tier = cloud_costs['large']
    
    # Installation labor (per kiosk)
    installation_labor = 300 * num_kiosks  # 4 hours @ $75/hr
    
    # Total costs
    total_hardware = hardware_total + installation_labor
    first_year_total = total_hardware + (cloud_tier['total'] * 12)
    
    return {
        'num_kiosks': num_kiosks,
        'config_type': config_type,
        'hardware_per_kiosk': config['total'],
        'hardware_total': hardware_total,
        'installation_labor': installation_labor,
        'cloud_monthly': cloud_tier['total'],
        'cloud_annual': cloud_tier['total'] * 12,
        'first_year_total': first_year_total,
        'ongoing_annual': cloud_tier['total'] * 12
    }

# Example calculations
print("Single kiosk (standard):")
print(calculate_concierge_bom(1, 'standard'))
# Hardware: $2,200 + Installation: $300 + Cloud: $66/mo
# First year: ~$3,300

print("\n5 properties (standard):")
print(calculate_concierge_bom(5, 'standard'))
# Hardware: $11,000 + Installation: $1,500 + Cloud: $66/mo
# First year: ~$13,300

print("\n25 properties (premium):")
print(calculate_concierge_bom(25, 'premium'))
# Hardware: $87,500 + Installation: $7,500 + Cloud: $153/mo
# First year: ~$96,800
```

---

## Phase 1: Hardware Assembly

### Day 1: Physical Setup (2-3 hours)

**1.1 Unbox and Inventory**

```
CHECKLIST
☐ Touchscreen monitor
☐ Intel NUC or PC
☐ Webcam
☐ Barcode scanner
☐ Badge printer
☐ Floor stand or wall mount
☐ Power cables (3-4 needed)
☐ HDMI cable
☐ USB cables (3-4 needed)
☐ Ethernet cable (if using wired)
☐ Mounting hardware (screws, anchors)
☐ Cable management sleeves
☐ Documentation

TOOLS NEEDED
☐ Phillips screwdriver
☐ Drill (if mounting to wall/floor)
☐ Level
☐ Measuring tape
☐ Cable ties
☐ Label maker
```

**1.2 Assemble Floor Stand**

```
FLOOR STAND ASSEMBLY
1. Unpack base and vertical column
2. Connect column to base
   ├── Align mounting holes
   ├── Insert bolts (usually M8 or M10)
   ├── Tighten with wrench
   └── Verify stability (should not wobble)

3. Add ballast weight (if included)
   ├── Typically lead weights in base
   ├── 20-40 lbs recommended
   └── Prevents tipping

4. Route cables through column
   ├── Power cable
   ├── Ethernet cable
   ├── USB cables
   └── Leave 12" service loop at top

5. Attach monitor bracket to column
   ├── Use VESA mount (75x75 or 100x100)
   ├── Height: 48-54" to center (ADA compliant)
   ├── Check with level
   └── Tighten securely

WALL MOUNT ALTERNATIVE
1. Locate studs (or use anchors)
2. Mark drill holes
3. Drill pilot holes
4. Install wall bracket
5. Attach monitor to bracket
6. Verify level and secure
```

**1.3 Mount Computer (NUC)**

```
NUC MOUNTING OPTIONS

Option 1: VESA Mount (Recommended)
├── Most NUCs support VESA 75x75mm
├── Mount to back of monitor
├── Keeps cables short and tidy
└── Hidden from view

Option 2: Behind Column
├── Mount NUC to back of stand column
├── Use velcro or mounting brackets
├── Good for cable management
└── Easy access for maintenance

Option 3: In Base Compartment
├── Some stands have lockable compartment
├── Extra security
├── Requires longer cables
└── Heat management considerations

MOUNTING PROCEDURE
1. Attach VESA bracket to NUC
2. Position on back of monitor
3. Align holes
4. Secure with M4 screws
5. Verify NUC doesn't block ventilation
```

**1.4 Connect Peripherals**

```
CONNECTION ORDER
1. Power
   ├── Monitor → Power strip
   ├── NUC → Power strip
   ├── Printer → Power strip
   └── Use surge protector/UPS

2. Video
   ├── NUC HDMI → Monitor HDMI
   └── Verify connection is secure

3. USB Peripherals
   ├── Webcam → NUC USB 3.0 (top of monitor)
   ├── Barcode scanner → NUC USB 3.0
   ├── Printer → NUC USB 2.0
   └── Label each cable

4. Network
   ├── Ethernet → NUC (preferred)
   └── Or configure WiFi during software setup

CABLE MANAGEMENT
1. Bundle cables with velcro ties (not zip ties)
2. Route through cable sleeves
3. Secure along stand column
4. Leave service loops (6-12")
5. Label all cables at both ends
6. Test all connections before securing permanently
```

**1.5 Position Kiosk**

```
PLACEMENT GUIDELINES
Height: 48-54" to touchscreen center (ADA)
Distance from wall: 6-12" (allow cable access)
Clearance in front: 48" minimum (ADA wheelchair)
Lighting: Avoid direct sunlight on screen
Power: Within 10 feet of outlet
Network: Within cable reach or WiFi coverage

ACCESSIBILITY (ADA Compliance)
├── Forward reach: Max 48" high
├── Side reach: Max 54" high
├── Operable parts: One-hand operation
├── Clear floor space: 30" × 48"
└── Approach: Straight on or parallel

FINAL POSITIONING
1. Place kiosk in desired location
2. Check with level (both directions)
3. Adjust feet/shims if needed
4. Mark floor (for repositioning after testing)
5. Connect power and network
6. Cable management for floor cables (rubber covers)
```

---

## Phase 2: Software Installation

### Day 1: Operating System Setup (2 hours)

**2.1 Install Ubuntu Desktop**

```bash
# Download Ubuntu 22.04 LTS Desktop
# Create bootable USB drive
# Boot NUC from USB

# Installation options:
# - Language: English
# - Keyboard: US
# - Installation type: Minimal installation
# - Erase disk and install Ubuntu
# - Timezone: Your timezone
# - User: kiosk / Password: (secure password)

# Wait for installation (~20 minutes)
# Reboot and remove USB drive
```

**2.2 Initial System Configuration**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y \
  openssh-server \
  vim \
  curl \
  wget \
  git \
  build-essential \
  net-tools \
  chromium-browser \
  unclutter \
  x11-xserver-utils \
  pulseaudio

# Enable SSH (for remote management)
sudo systemctl enable ssh
sudo systemctl start ssh

# Set static IP (if using Ethernet)
sudo nano /etc/netplan/01-netcfg.yaml
# Add:
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 10.0.40.50/24
      gateway4: 10.0.40.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]

sudo netplan apply

# Disable automatic updates (kiosk stability)
sudo systemctl disable apt-daily.timer
sudo systemctl disable apt-daily-upgrade.timer

# Disable screen blanking
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.desktop.screensaver lock-enabled false
```

**2.3 Configure Auto-Login**

```bash
# Edit GDM config for auto-login
sudo nano /etc/gdm3/custom.conf

# Uncomment and edit:
[daemon]
AutomaticLoginEnable = true
AutomaticLogin = kiosk

# Save and exit

# Verify auto-login on reboot
sudo reboot
```

**2.4 Install Kiosk Browser**

```bash
# Create kiosk startup script
mkdir -p /home/kiosk/bin
nano /home/kiosk/bin/start-kiosk.sh

# Add content:
#!/bin/bash

# Disable screen blanking
xset s off
xset -dpms
xset s noblank

# Hide mouse cursor
unclutter -idle 0.1 -root &

# Disable right-click
xdotool behave_screen_edge --delay 0 top exec --sync chromium-browser --app=https://concierge.company.com &

# Start Chromium in kiosk mode
chromium-browser \
  --kiosk \
  --app=https://concierge.company.com \
  --start-fullscreen \
  --noerrdialogs \
  --disable-infobars \
  --no-first-run \
  --disable-translate \
  --disable-features=TranslateUI \
  --disable-pinch \
  --overscroll-history-navigation=0 \
  --disable-session-crashed-bubble \
  --check-for-update-interval=604800 \
  --disk-cache-dir=/dev/null \
  --disk-cache-size=1 \
  --password-store=basic

# Make executable
chmod +x /home/kiosk/bin/start-kiosk.sh
```

**2.5 Auto-Start Kiosk on Boot**

```bash
# Create autostart directory
mkdir -p /home/kiosk/.config/autostart

# Create desktop entry
nano /home/kiosk/.config/autostart/kiosk.desktop

# Add content:
[Desktop Entry]
Type=Application
Name=Concierge Kiosk
Exec=/home/kiosk/bin/start-kiosk.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Comment=Start concierge kiosk application

# Test auto-start
sudo reboot

# Kiosk should launch automatically after boot
# If not, check logs: journalctl -xe
```

**2.6 Configure Peripheral Drivers**

```bash
# Webcam test
sudo apt install -y cheese
cheese  # Verify webcam works

# Or use command line:
ffmpeg -f v4l2 -framerate 30 -video_size 1920x1080 -i /dev/video0 -frames:v 1 test.jpg

# Barcode scanner (should work as keyboard input)
# Test by scanning into text editor

# Printer setup (CUPS)
sudo apt install -y cups
sudo systemctl enable cups
sudo systemctl start cups

# Access CUPS web interface
# http://localhost:631

# Add printer:
# 1. Administration → Add Printer
# 2. Select USB printer
# 3. Choose driver (or PPD file if provided)
# 4. Set as default printer
# 5. Print test page

# Test printer from command line
echo "Test print" | lp
```

---

## Phase 3: Cloud Platform Deployment

### Day 1: Backend Setup (2 hours)

**3.1 Deploy Cloud Infrastructure**

```bash
# Deploy on DigitalOcean, AWS, or Azure
# This example uses DigitalOcean

# Create droplet via CLI or web UI
# - Distribution: Ubuntu 22.04 LTS
# - Plan: 4GB RAM / 2 vCPU ($24/mo)
# - Datacenter: Closest to property locations
# - Additional: Enable monitoring, backups

# SSH to droplet
ssh root@your-droplet-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
apt install -y docker-compose

# Create application directory
mkdir -p /opt/concierge
cd /opt/concierge
```

**3.2 Deploy Application Stack**

```yaml
# Create docker-compose.yml
cat > docker-compose.yml <<'EOF'
version: '3.8'

services:
  web:
    image: node:18
    container_name: concierge-web
    working_dir: /app
    volumes:
      - ./app:/app
      - ./uploads:/app/uploads
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
      - MONGODB_URI=mongodb://mongodb:27017/concierge
      - JWT_SECRET=${JWT_SECRET}
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
      - TWILIO_PHONE=${TWILIO_PHONE}
      - SENDGRID_API_KEY=${SENDGRID_API_KEY}
    command: npm start
    depends_on:
      - mongodb
      - redis
    restart: unless-stopped

  mongodb:
    image: mongo:6
    container_name: concierge-db
    volumes:
      - mongodb-data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD}
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: concierge-redis
    volumes:
      - redis-data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: concierge-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  mongodb-data:
  redis-data:
EOF
```

**3.3 Create Application Code**

```javascript
// Create app/server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const multer = require('multer');
const twilio = require('twilio');
const sgMail = require('@sendgrid/mail');

const app = express();
app.use(express.json());
app.use(cors());
app.use(express.static('public'));

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI);

// Visitor schema
const visitorSchema = new mongoose.Schema({
  firstName: { type: String, required: true },
  lastName: { type: String, required: true },
  email: { type: String, required: true },
  phone: String,
  company: String,
  host: {
    name: String,
    email: String,
    phone: String
  },
  property: {
    id: String,
    name: String
  },
  checkInTime: { type: Date, default: Date.now },
  checkOutTime: Date,
  photo: String,  // Base64 or URL
  signature: String,  // Base64
  badgeNumber: String,
  purpose: String,
  status: { 
    type: String, 
    enum: ['checked_in', 'checked_out', 'no_show'],
    default: 'checked_in'
  },
  preRegistered: { type: Boolean, default: false },
  qrCode: String
});

const Visitor = mongoose.model('Visitor', visitorSchema);

// Check-in endpoint
app.post('/api/visitors/check-in', async (req, res) => {
  try {
    const visitorData = req.body;
    
    // Create visitor record
    const visitor = new Visitor(visitorData);
    await visitor.save();
    
    // Send SMS to host
    if (visitor.host.phone) {
      const twilioClient = twilio(
        process.env.TWILIO_ACCOUNT_SID,
        process.env.TWILIO_AUTH_TOKEN
      );
      
      await twilioClient.messages.create({
        body: `${visitor.firstName} ${visitor.lastName} from ${visitor.company || 'N/A'} has checked in at ${visitor.property.name}`,
        from: process.env.TWILIO_PHONE,
        to: visitor.host.phone
      });
    }
    
    // Send email confirmation to visitor
    if (visitor.email) {
      sgMail.setApiKey(process.env.SENDGRID_API_KEY);
      
      await sgMail.send({
        to: visitor.email,
        from: 'noreply@company.com',
        subject: 'Check-in Confirmation',
        html: `
          <h2>Welcome to ${visitor.property.name}</h2>
          <p>You checked in at ${visitor.checkInTime.toLocaleString()}</p>
          <p>Your host has been notified.</p>
          <p>Badge Number: ${visitor.badgeNumber}</p>
        `
      });
    }
    
    res.json({ 
      success: true, 
      visitor: visitor,
      message: 'Check-in successful'
    });
    
  } catch (error) {
    console.error('Check-in error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
});

// Check-out endpoint
app.post('/api/visitors/check-out', async (req, res) => {
  try {
    const { visitorId } = req.body;
    
    const visitor = await Visitor.findByIdAndUpdate(
      visitorId,
      { 
        checkOutTime: new Date(),
        status: 'checked_out'
      },
      { new: true }
    );
    
    res.json({ success: true, visitor });
    
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get visitors (for dashboard)
app.get('/api/visitors', async (req, res) => {
  try {
    const { propertyId, date, status } = req.query;
    
    let query = {};
    if (propertyId) query['property.id'] = propertyId;
    if (status) query.status = status;
    if (date) {
      const startOfDay = new Date(date);
      startOfDay.setHours(0, 0, 0, 0);
      const endOfDay = new Date(date);
      endOfDay.setHours(23, 59, 59, 999);
      query.checkInTime = { $gte: startOfDay, $lte: endOfDay };
    }
    
    const visitors = await Visitor.find(query)
      .sort({ checkInTime: -1 })
      .limit(100);
    
    res.json({ success: true, visitors });
    
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Pre-registration endpoint
app.post('/api/visitors/pre-register', async (req, res) => {
  try {
    const visitorData = {
      ...req.body,
      preRegistered: true,
      qrCode: generateQRCode(req.body)
    };
    
    const visitor = new Visitor(visitorData);
    await visitor.save();
    
    // Email QR code to visitor
    // ...
    
    res.json({ success: true, visitor });
    
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Concierge API running on port ${PORT}`);
});
```

**3.4 Deploy and Start Services**

```bash
# Create .env file
cat > .env <<EOF
JWT_SECRET=$(openssl rand -base64 32)
MONGO_PASSWORD=$(openssl rand -base64 32)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE=+1234567890
SENDGRID_API_KEY=your_sendgrid_key
EOF

# Install dependencies
cd app
npm init -y
npm install express mongoose cors multer twilio @sendgrid/mail jsonwebtoken bcryptjs

# Start services
cd /opt/concierge
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web

# Access application
# http://your-droplet-ip:3000
```

---

## Phase 4: Frontend Development

### Kiosk User Interface

**4.1 Create React Frontend**

```jsx
// src/App.jsx - Main kiosk interface
import React, { useState, useRef } from 'react';
import Webcam from 'react-webcam';
import SignatureCanvas from 'react-signature-canvas';
import './App.css';

function App() {
  const [step, setStep] = useState('welcome');  // welcome, info, photo, sign, badge
  const [visitor, setVisitor] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    company: '',
    host: '',
    purpose: ''
  });
  const [photo, setPhoto] = useState(null);
  const [signature, setSignature] = useState(null);
  
  const webcamRef = useRef(null);
  const signatureRef = useRef(null);

  // Welcome screen
  if (step === 'welcome') {
    return (
      <div className="screen welcome-screen">
        <h1>Welcome to Acme Corporation</h1>
        <p>Please check in for your visit</p>
        
        <button 
          className="btn-primary" 
          onClick={() => setStep('info')}
        >
          Check In
        </button>
        
        <button 
          className="btn-secondary"
          onClick={() => setStep('qr-scan')}
        >
          Pre-Registered? Scan QR Code
        </button>
      </div>
    );
  }

  // Information entry screen
  if (step === 'info') {
    return (
      <div className="screen info-screen">
        <h2>Visitor Information</h2>
        
        <form onSubmit={(e) => {
          e.preventDefault();
          setStep('photo');
        }}>
          <div className="form-group">
            <label>First Name *</label>
            <input
              type="text"
              required
              value={visitor.firstName}
              onChange={(e) => setVisitor({...visitor, firstName: e.target.value})}
              autoFocus
            />
          </div>
          
          <div className="form-group">
            <label>Last Name *</label>
            <input
              type="text"
              required
              value={visitor.lastName}
              onChange={(e) => setVisitor({...visitor, lastName: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Email *</label>
            <input
              type="email"
              required
              value={visitor.email}
              onChange={(e) => setVisitor({...visitor, email: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Phone</label>
            <input
              type="tel"
              value={visitor.phone}
              onChange={(e) => setVisitor({...visitor, phone: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Company</label>
            <input
              type="text"
              value={visitor.company}
              onChange={(e) => setVisitor({...visitor, company: e.target.value})}
            />
          </div>
          
          <div className="form-group">
            <label>Who are you visiting? *</label>
            <select
              required
              value={visitor.host}
              onChange={(e) => setVisitor({...visitor, host: e.target.value})}
            >
              <option value="">Select...</option>
              <option value="john.doe@company.com">John Doe - CEO</option>
              <option value="jane.smith@company.com">Jane Smith - CTO</option>
              <option value="bob.johnson@company.com">Bob Johnson - Sales</option>
            </select>
          </div>
          
          <div className="form-actions">
            <button 
              type="button" 
              className="btn-secondary"
              onClick={() => setStep('welcome')}
            >
              Back
            </button>
            <button type="submit" className="btn-primary">
              Next
            </button>
          </div>
        </form>
      </div>
    );
  }

  // Photo capture screen
  if (step === 'photo') {
    return (
      <div className="screen photo-screen">
        <h2>Take Your Photo</h2>
        <p>Please look at the camera</p>
        
        <Webcam
          ref={webcamRef}
          audio={false}
          screenshotFormat="image/jpeg"
          className="webcam-preview"
          videoConstraints={{
            width: 1280,
            height: 720,
            facingMode: 'user'
          }}
        />
        
        {photo && (
          <div className="photo-preview">
            <img src={photo} alt="Visitor" />
            <button onClick={() => setPhoto(null)}>Retake</button>
          </div>
        )}
        
        <div className="form-actions">
          <button 
            className="btn-secondary"
            onClick={() => setStep('info')}
          >
            Back
          </button>
          
          {!photo ? (
            <button 
              className="btn-primary"
              onClick={() => {
                const imageSrc = webcamRef.current.getScreenshot();
                setPhoto(imageSrc);
              }}
            >
              Capture Photo
            </button>
          ) : (
            <button 
              className="btn-primary"
              onClick={() => setStep('sign')}
            >
              Next
            </button>
          )}
        </div>
      </div>
    );
  }

  // Signature screen
  if (step === 'sign') {
    return (
      <div className="screen signature-screen">
        <h2>Sign Below</h2>
        <p>I agree to the visitor policies and procedures</p>
        
        <SignatureCanvas
          ref={signatureRef}
          canvasProps={{
            width: 600,
            height: 300,
            className: 'signature-canvas'
          }}
        />
        
        <div className="form-actions">
          <button 
            className="btn-secondary"
            onClick={() => signatureRef.current.clear()}
          >
            Clear
          </button>
          
          <button 
            className="btn-secondary"
            onClick={() => setStep('photo')}
          >
            Back
          </button>
          
          <button 
            className="btn-primary"
            onClick={async () => {
              const signatureData = signatureRef.current.toDataURL();
              
              // Submit check-in
              const response = await fetch('http://api.company.com/api/visitors/check-in', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  ...visitor,
                  photo: photo,
                  signature: signatureData,
                  property: {
                    id: 'PROP_001',
                    name: 'Acme Corporation HQ'
                  }
                })
              });
              
              const data = await response.json();
              
              if (data.success) {
                setStep('badge');
                // Trigger badge print
                printBadge(data.visitor);
              }
            }}
          >
            Submit
          </button>
        </div>
      </div>
    );
  }

  // Badge printing / completion screen
  if (step === 'badge') {
    setTimeout(() => {
      setStep('welcome');
      setVisitor({});
      setPhoto(null);
      setSignature(null);
    }, 10000);  // Return to welcome after 10 seconds
    
    return (
      <div className="screen success-screen">
        <div className="success-icon">✓</div>
        <h2>Welcome, {visitor.firstName}!</h2>
        <p>Your host has been notified</p>
        <p className="badge-instruction">
          Please take your visitor badge from the printer
        </p>
        <div className="badge-preview">
          <img src={photo} alt="Visitor" />
          <h3>{visitor.firstName} {visitor.lastName}</h3>
          <p>{visitor.company}</p>
          <p>Visiting: {visitor.host}</p>
          <p className="date">{new Date().toLocaleDateString()}</p>
        </div>
      </div>
    );
  }
}

export default App;
```

**4.2 Badge Printing**

```javascript
// Badge printing service
function printBadge(visitor) {
  // Generate badge content (HTML/Canvas)
  const badge = generateBadgeHTML(visitor);
  
  // Send to printer via CUPS or direct USB
  // Option 1: Use node-printer
  const printer = require('printer');
  printer.printDirect({
    data: badge,
    printer: 'DYMO_LabelWriter_450',  // Printer name
    type: 'RAW',
    success: (jobID) => {
      console.log(`Badge printed: ${jobID}`);
    },
    error: (err) => {
      console.error('Print error:', err);
    }
  });
  
  // Option 2: Print via browser (if printer supports IPP)
  window.print();
}

function generateBadgeHTML(visitor) {
  return `
    <div style="width: 4in; height: 3in; border: 2px solid #000; padding: 20px;">
      <div style="text-align: center;">
        <img src="${visitor.photo}" style="width: 1.5in; height: 1.5in; border-radius: 50%;" />
        <h2>${visitor.firstName} ${visitor.lastName}</h2>
        <p>${visitor.company}</p>
        <p>Visiting: ${visitor.host}</p>
        <p>${new Date().toLocaleDateString()}</p>
        <img src="${visitor.qrCode}" style="width: 1in; height: 1in;" />
      </div>
    </div>
  `;
}
```

---

## Phase 5: Testing & Validation

### Day 2: System Testing

**5.1 Kiosk Functionality Test**

```bash
#!/bin/bash
# Kiosk test script

echo "OS-CONCIERGE Kiosk Testing"
echo "==========================="

# Test 1: Network connectivity
echo "Test 1: Network Connectivity"
ping -c 3 google.com &> /dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ Internet: Connected"
else
    echo "  ❌ Internet: No connection"
fi

# Test 2: API connectivity
echo ""
echo "Test 2: API Connectivity"
response=$(curl -s -o /dev/null -w "%{http_code}" http://api.company.com/api/health)
if [ "$response" = "200" ]; then
    echo "  ✅ API: Reachable"
else
    echo "  ❌ API: Not reachable ($response)"
fi

# Test 3: Webcam
echo ""
echo "Test 3: Webcam"
if [ -e /dev/video0 ]; then
    echo "  ✅ Webcam: Detected"
    # Capture test image
    ffmpeg -f v4l2 -i /dev/video0 -frames:v 1 /tmp/webcam_test.jpg &> /dev/null
    if [ -f /tmp/webcam_test.jpg ]; then
        echo "  ✅ Webcam: Image captured"
    else
        echo "  ❌ Webcam: Capture failed"
    fi
else
    echo "  ❌ Webcam: Not detected"
fi

# Test 4: Printer
echo ""
echo "Test 4: Badge Printer"
lpstat -p | grep -q "printer"
if [ $? -eq 0 ]; then
    echo "  ✅ Printer: Detected"
    # Print test page
    echo "Test Badge" | lp
    echo "  ℹ️  Check if test page printed"
else
    echo "  ❌ Printer: Not detected"
fi

# Test 5: Barcode scanner
echo ""
echo "Test 5: Barcode Scanner"
echo "  ℹ️  Scan a barcode to test (30 second timeout)"
read -t 30 -p "  Scan: " barcode
if [ ! -z "$barcode" ]; then
    echo "  ✅ Scanner: Working (scanned: $barcode)"
else
    echo "  ⚠️  Scanner: No input received"
fi

# Test 6: Touchscreen
echo ""
echo "Test 6: Touchscreen"
echo "  ℹ️  Touch the screen to test"
xinput list | grep -i touch
if [ $? -eq 0 ]; then
    echo "  ✅ Touchscreen: Detected"
else
    echo "  ⚠️  Touchscreen: Not detected (may be mouse only)"
fi

echo ""
echo "Testing complete!"
```

**5.2 Check-In Flow Test**

```javascript
// Automated check-in test
async function testCheckInFlow() {
  console.log('Testing check-in flow...\n');
  
  // Test visitor data
  const testVisitor = {
    firstName: 'John',
    lastName: 'Test',
    email: 'john.test@example.com',
    phone: '+15551234567',
    company: 'Test Corp',
    host: 'jane.smith@company.com',
    purpose: 'Meeting',
    photo: 'data:image/jpeg;base64,...',  // Base64 photo
    signature: 'data:image/png;base64,...',  // Base64 signature
    property: {
      id: 'PROP_001',
      name: 'Test Property'
    }
  };
  
  // Step 1: Submit check-in
  console.log('Step 1: Submitting check-in...');
  const response = await fetch('http://api.company.com/api/visitors/check-in', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(testVisitor)
  });
  
  const data = await response.json();
  
  if (data.success) {
    console.log('✅ Check-in successful');
    console.log(`  Visitor ID: ${data.visitor._id}`);
    console.log(`  Badge Number: ${data.visitor.badgeNumber}`);
  } else {
    console.log('❌ Check-in failed:', data.error);
    return;
  }
  
  // Step 2: Verify visitor in database
  console.log('\nStep 2: Verifying database record...');
  const verifyResponse = await fetch(
    `http://api.company.com/api/visitors?email=${testVisitor.email}`
  );
  const verifyData = await verifyResponse.json();
  
  if (verifyData.visitors.length > 0) {
    console.log('✅ Visitor record found in database');
  } else {
    console.log('❌ Visitor record not found');
  }
  
  // Step 3: Check notification sent
  console.log('\nStep 3: Check notifications...');
  console.log('  ℹ️  Manually verify SMS and email were received');
  
  // Step 4: Test check-out
  console.log('\nStep 4: Testing check-out...');
  const checkoutResponse = await fetch('http://api.company.com/api/visitors/check-out', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ visitorId: data.visitor._id })
  });
  
  const checkoutData = await checkoutResponse.json();
  
  if (checkoutData.success) {
    console.log('✅ Check-out successful');
  } else {
    console.log('❌ Check-out failed');
  }
  
  console.log('\n✅ Check-in flow test complete!');
}

testCheckInFlow();
```

**5.3 Load Testing**

```python
# Simulate multiple concurrent check-ins
import asyncio
import aiohttp
import time

async def check_in(session, visitor_num):
    """Simulate a visitor check-in"""
    visitor = {
        'firstName': f'Test{visitor_num}',
        'lastName': 'Visitor',
        'email': f'test{visitor_num}@example.com',
        'phone': '+15551234567',
        'company': 'Test Corp',
        'host': 'jane.smith@company.com',
        'property': {'id': 'PROP_001', 'name': 'Test Property'}
    }
    
    start_time = time.time()
    
    async with session.post(
        'http://api.company.com/api/visitors/check-in',
        json=visitor
    ) as response:
        data = await response.json()
        duration = time.time() - start_time
        
        if data['success']:
            print(f"✅ Visitor {visitor_num}: {duration:.2f}s")
        else:
            print(f"❌ Visitor {visitor_num}: Failed")
        
        return duration

async def load_test(num_visitors):
    """Run load test with N concurrent check-ins"""
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            check_in(session, i) 
            for i in range(num_visitors)
        ]
        
        start = time.time()
        durations = await asyncio.gather(*tasks)
        total_time = time.time() - start
        
        print(f"\nLoad Test Results:")
        print(f"  Total visitors: {num_visitors}")
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Average: {sum(durations)/len(durations):.2f}s")
        print(f"  Min: {min(durations):.2f}s")
        print(f"  Max: {max(durations):.2f}s")
        print(f"  Throughput: {num_visitors/total_time:.1f} check-ins/sec")

# Run test
asyncio.run(load_test(50))  # Simulate 50 concurrent check-ins
```

---

## Phase 6: Go-Live

### Day 2: Production Cutover

**6.1 Pre-Go-Live Checklist**

```
TECHNICAL VALIDATION
☐ Kiosk boots to welcome screen automatically
☐ Touchscreen responsive
☐ Webcam captures clear photos
☐ Barcode scanner reads QR codes
☐ Badge printer prints correctly
☐ Network connectivity stable
☐ API endpoints responding (<500ms)
☐ Database backups configured

USER EXPERIENCE
☐ Check-in flow tested end-to-end
☐ Badge quality acceptable
☐ SMS notifications sending
☐ Email confirmations sending
☐ Pre-registration working
☐ Staff dashboard accessible

PHYSICAL SETUP
☐ Kiosk positioned correctly (ADA compliant)
☐ Adequate lighting (no glare)
☐ Signage installed ("Check in here")
☐ Instructions posted (if needed)
☐ Badge stock loaded
☐ Cable management clean
☐ Power backup (UPS) working

DOCUMENTATION
☐ Admin credentials secured
☐ Staff training completed
☐ Support procedures documented
☐ Emergency contacts posted
☐ User manual available
☐ Troubleshooting guide ready
```

**6.2 Go-Live Script**

```bash
#!/bin/bash
# OS-CONCIERGE Go-Live

echo "OS-CONCIERGE System Go-Live"
echo "============================"

# Step 1: Final health check
echo "Step 1: System Health Check"
./scripts/health-check.sh
echo ""

# Step 2: Verify cloud services
echo "Step 2: Cloud Services Status"
curl -s http://api.company.com/api/health | jq '.'

# Step 3: Test check-in flow
echo ""
echo "Step 3: Test Check-In"
echo "  Please complete a test check-in at the kiosk"
read -p "  Press Enter when complete..."

# Step 4: Verify test visitor
echo "Step 4: Verify Test Visitor"
curl -s "http://api.company.com/api/visitors?propertyId=PROP_001" | jq '.visitors | length'

# Step 5: Enable production mode
echo ""
echo "Step 5: Enable Production Mode"
echo "  System is now live for actual visitors"

echo ""
echo "✅ GO-LIVE COMPLETE!"
echo ""
echo "System Information:"
echo "  - Kiosk URL: https://concierge.company.com"
echo "  - Admin Dashboard: https://concierge.company.com/admin"
echo "  - Support: support@company.com"
echo ""
echo "Monitor for first 2 hours"
```

---

## Post-Deployment

### Maintenance Schedule

**Daily:**
```
☐ Check badge printer stock
☐ Clean touchscreen
☐ Verify kiosk is operational
☐ Review visitor log for issues
```

**Weekly:**
```
☐ Restart kiosk (off-hours)
☐ Update visitor directory/hosts
☐ Review analytics (peak times, etc.)
☐ Clean webcam lens
```

**Monthly:**
```
☐ Software updates (test in staging first)
☐ Clean hardware (dust, fingerprints)
☐ Verify backup procedures
☐ Review and optimize workflow
☐ User feedback collection
```

---

## Troubleshooting Guide

### Common Issues

**Issue 1: Kiosk Not Booting to Application**
```
Symptoms: Kiosk shows desktop instead of app
Resolution:
1. Check autostart: ls ~/.config/autostart/
2. Verify script: cat ~/bin/start-kiosk.sh
3. Check logs: journalctl -xe | grep kiosk
4. Restart: sudo reboot
```

**Issue 2: Badge Not Printing**
```
Symptoms: Check-in completes but no badge prints
Resolution:
1. Check printer: lpstat -p
2. Verify connection: lsusb
3. Check queue: lpq
4. Test print: echo "Test" | lp
5. Reload CUPS: sudo systemctl restart cups
```

**Issue 3: Webcam Image Dark/Blurry**
```
Symptoms: Poor photo quality
Resolution:
1. Clean lens with microfiber cloth
2. Adjust lighting (add light source)
3. Check camera settings: v4l2-ctl --list-ctrls
4. Adjust exposure: v4l2-ctl --set-ctrl=exposure_absolute=200
```

**Issue 4: Touchscreen Not Responding**
```
Symptoms: Touch not registering
Resolution:
1. Check connection: lsusb | grep -i touch
2. Calibrate: xinput_calibrator
3. Restart X server: sudo systemctl restart gdm3
4. Check for physical damage
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Typical Deployment**: 1-2 days per property  
**System Scalability**: 1 to 100+ properties per cloud instance
