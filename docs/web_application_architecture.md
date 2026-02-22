# 🏥 MRI Super-Resolution Web Application - Technical Architecture Document

**Project:** Final Year Project - MRI SR Pipeline Web Interface  
**Version:** 1.0  
**Date:** February 22, 2026  
**Status:** Planning & Design Phase

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Technology Stack Recommendations](#technology-stack-recommendations)
4. [Feature Implementation Guide](#feature-implementation-guide)
5. [Data Flow & API Design](#data-flow--api-design)
6. [3D Visualization Strategy](#3d-visualization-strategy)
7. [Security & Privacy Considerations](#security--privacy-considerations)
8. [Deployment Architecture](#deployment-architecture)
9. [Development Roadmap](#development-roadmap)
10. [Cost & Resource Estimation](#cost--resource-estimation)

---

## 1. Executive Summary

### 1.1 Project Goals

Build a platform that enables:
1. **Preprocessing Service**: Upload raw MRI scans → receive preprocessed HR/LR pairs
2. **Super-Resolution Inference**: Process LR images through trained model → generate HR predictions
3. **3D Medical Visualization**: Interactive comparison of LR vs HR images (3D Slicer-like interface)

### 1.2 Key Requirements

- **File Format**: NIfTI (.nii.gz) input/output
- **Processing**: Long-running tasks (5-30 minutes per scan)
- **Visualization**: 3D rendering with medical imaging tools
- **Security**: HIPAA-aware design (anonymization, secure storage)
- **Scalability**: Handle multiple concurrent users
- **Model Serving**: GPU-accelerated inference

---

## 2. Web vs Desktop Application: Critical Decision Analysis

### 2.1 Comparison Overview

| Aspect | Web Application | Desktop Application (3D Slicer Style) |
|--------|----------------|--------------------------------------|
| **Development Time** | 14-16 weeks | 20-24 weeks |
| **Deployment** | Single deployment, instant updates | Install on each machine, manual updates |
| **Access** | Anywhere (browser) | Local machine only |
| **Performance** | Good (WebGL) | Excellent (native OpenGL/Vulkan) |
| **3D Visualization** | Limited by browser | Full-featured medical imaging |
| **Collaboration** | Easy (share links) | Difficult (file transfer) |
| **GPU Utilization** | Server-side only | Both local + server |
| **Initial Setup** | None (just URL) | Complex installation |
| **Cost** | Server hosting (~$60-600/month) | Free (one-time dev) |
| **Maintenance** | Centralized, easier | Distributed, harder |
| **FYP Showcase** | Impressive, modern | More traditional |

### 2.2 Detailed Analysis

#### **A. Web Application Approach**

**Architecture:**
```
User Browser (Thin Client)
    ↓ Upload files via web interface
Cloud/Server (Heavy Backend)
    ↓ Processing + GPU inference
Browser (3D Viewer - NiiVue/WebGL)
```

**Advantages:**
- ✅ **No Installation Required**: Users just need a browser
- ✅ **Instant Updates**: Fix bugs once, all users benefit immediately
- ✅ **Cross-Platform**: Works on Windows, Mac, Linux, even tablets
- ✅ **Centralized Management**: Single server to maintain
- ✅ **Easy Collaboration**: Share results via URL
- ✅ **Modern & Impressive**: Great for FYP demonstrations
- ✅ **Scalable**: Add more servers as users grow
- ✅ **Remote Access**: Work from anywhere
- ✅ **Controlled Environment**: You manage dependencies
- ✅ **Usage Analytics**: Track how features are used

**Disadvantages:**
- ⚠️ **Ongoing Hosting Costs**: Need server 24/7 (~$60-600/month)
- ⚠️ **Internet Dependency**: Requires stable connection
- ⚠️ **Limited 3D Performance**: WebGL not as fast as native
- ⚠️ **File Upload Size**: Large files slow to upload
- ⚠️ **Browser Limitations**: Memory limits, security restrictions
- ⚠️ **Privacy Concerns**: Medical data sent to server
- ⚠️ **Learning Curve**: Need to learn web technologies

**Best For:**
- Multi-user scenarios (hospital departments, research groups)
- Remote collaboration
- Demonstrating SaaS (Software as a Service) model
- When you want modern, impressive demo for FYP
- If you plan to commercialize later

---

#### **B. Desktop Application Approach (3D Slicer Style)**

**Architecture:**
```
Local Desktop Application
    ↓ Process locally OR
    ↓ Send to remote server for GPU tasks
    ↓ Visualize locally (full GPU power)
```

**Advantages:**
- ✅ **Superior Performance**: Native code, full GPU access
- ✅ **Offline Capable**: Work without internet (for local processing)
- ✅ **Advanced Visualization**: Professional medical imaging tools
- ✅ **No Data Privacy Issues**: Data stays on user's machine
- ✅ **No Hosting Costs**: One-time development cost
- ✅ **Large File Handling**: No upload limits
- ✅ **Existing Ecosystem**: Can integrate with 3D Slicer/ITK-SNAP
- ✅ **Professional Credibility**: Medical community trusts desktop tools
- ✅ **Rich Features**: Complex annotations, measurements, DICOM support

**Disadvantages:**
- ⚠️ **Complex Installation**: Users must install dependencies (Python, CUDA, etc.)
- ⚠️ **Platform-Specific**: Need different builds for Windows/Mac/Linux
- ⚠️ **Update Difficulty**: Must manually update each installation
- ⚠️ **Hardware Requirements**: Users need powerful local machine
- ⚠️ **No Collaboration**: Hard to share results
- ⚠️ **Longer Development**: UI frameworks (Qt/wxPython) are complex
- ⚠️ **Distribution Challenges**: Large install packages (>1GB)
- ⚠️ **Support Burden**: Different issues on different machines

**Best For:**
- Single-user clinical workstations
- Research labs with powerful local machines
- When data privacy is paramount (cannot send to cloud)
- If you want to integrate with existing medical imaging software
- Academic environments (like hospitals using 3D Slicer)

---

### 2.3 Hybrid Approach (Best of Both Worlds)

**Recommended Architecture:**
```
Desktop App (Viewer + Local Processing)
    ↕ REST API
Cloud Backend (Heavy GPU Tasks + Model Serving)
```

**How It Works:**
1. Users install lightweight desktop app (Electron or Python GUI)
2. Light tasks (viewing, annotations) happen locally
3. Heavy tasks (preprocessing, GPU inference) sent to cloud
4. Desktop app provides professional 3D visualization
5. Backend handles model inference and scalability

**Advantages:**
- ✅ Best visualization (desktop) + best scalability (cloud)
- ✅ Offline viewing of downloaded results
- ✅ Cloud handles expensive GPU processing
- ✅ Easy updates for backend logic

**Disadvantages:**
- ⚠️ Most complex to develop (both desktop + web backend)
- ⚠️ Still requires installation

---

### 2.4 Technology Comparison for Each Approach

#### **Web Application Stack**

**Frontend:**
- React + TypeScript
- NiiVue (medical imaging viewer)
- Three.js (3D rendering)
- TailwindCSS

**Backend:**
- FastAPI (Python)
- Celery (task queue)
- PostgreSQL + Redis

**Pros:** Modern, maintainable, extensive community support  
**Cons:** Learning curve if unfamiliar with web dev

---

#### **Desktop Application Stack**

**Option 1: Python + Qt (Most Professional)**
```python
Stack:
├── PyQt6 / PySide6      (GUI framework)
├── VTK                  (3D visualization - medical grade)
├── SimpleITK / ANTsPy   (Image processing - already using)
├── PyTorch              (Model inference)
└── Your existing pipeline
```

**Pros:**
- Same language as your pipeline
- VTK is industry standard for medical imaging
- 3D Slicer is built with this stack
- Excellent 3D rendering

**Cons:**
- Qt has learning curve
- Large deployment size
- GUI design is tedious

---

**Option 2: Electron + React (Modern Desktop)**
```javascript
Stack:
├── Electron             (Cross-platform desktop)
├── React + TypeScript   (UI - same as web)
├── NiiVue               (3D viewer)
└── Python Backend (subprocess)
    └── Your pipeline + PyTorch
```

**Pros:**
- Web technologies in desktop wrapper
- Same React code as web version
- Easy to build cross-platform
- Modern look and feel

**Cons:**
- Large memory footprint
- Not truly native performance
- Python subprocess communication complexity

---

**Option 3: 3D Slicer Extension (Integrate with Existing Tool)**
```python
Stack:
├── 3D Slicer            (Already installed in medical institutions)
├── Custom Python Module (Your SR pipeline)
└── SlicerExtension API
```

**Pros:**
- No visualization code needed (use Slicer's)
- Medical users already have it
- Professional credibility
- Fastest development time

**Cons:**
- Users must have 3D Slicer installed
- Limited UI customization
- Tied to Slicer's release cycle

---

### 2.5 Decision Matrix for Your FYP

#### **Score Each Factor (1-10, higher is better):**

| Factor | Weight | Web App | Desktop App | Hybrid | 3D Slicer Plugin |
|--------|--------|---------|-------------|--------|------------------|
| **Development Time** | 25% | 9 | 5 | 4 | 10 |
| **FYP Demo Impact** | 20% | 10 | 7 | 9 | 6 |
| **Ease of Use** | 15% | 10 | 6 | 7 | 9 |
| **3D Viz Quality** | 15% | 6 | 10 | 10 | 10 |
| **Scalability** | 10% | 10 | 3 | 8 | 5 |
| **Cost (Development + Hosting)** | 10% | 7 | 9 | 5 | 10 |
| **Future Commercialization** | 5% | 10 | 6 | 8 | 4 |
| **Weighted Score** | **100%** | **8.8** | **6.6** | **7.1** | **8.4** |

---

### 2.6 Recommendations by Scenario

#### **Scenario 1: You want to impress with modern tech & finish on time**
**→ Choose Web Application**
- Most impressive for FYP presentation
- Easier to demonstrate (just share URL)
- 16-week development timeline is achievable
- Can use university free hosting/credits

#### **Scenario 2: You're targeting clinical deployment**
**→ Choose 3D Slicer Extension**
- Hospitals already use 3D Slicer
- Professional credibility
- Fastest development (6-8 weeks)
- Focus on algorithm, not UI

#### **Scenario 3: You have strong desktop development skills**
**→ Choose Desktop Application (PyQt + VTK)**
- Best visualization quality
- Good for research lab deployment
- No hosting costs
- More traditional but solid

#### **Scenario 4: You have a larger team (3-4 people)**
**→ Choose Hybrid Approach**
- Desktop for visualization
- Web backend for processing
- Best of both worlds
- Distribute work across team

#### **Scenario 5: Limited time, limited web experience**
**→ Choose 3D Slicer Extension**
- Minimal UI work
- Focus on your SR algorithm
- Quick integration
- Well-documented API

---

### 2.7 My Strong Recommendation for Your FYP

**🎯 Go with Web Application** for these reasons:

1. **Timeline**: You can finish in 16 weeks with 2 developers
2. **Modern**: FYP evaluators will be impressed by web-based AI service
3. **Demonstrable**: Easy to show during presentation (no installation)
4. **Portfolio**: Great for resume/GitHub showcase
5. **Skills**: Learn modern full-stack development (valuable for career)
6. **Scalable**: Can add features incrementally
7. **University Support**: Most universities offer free cloud credits

**When to Reconsider:**
- ❌ If you have NO web development experience and < 12 weeks left
- ❌ If visualization quality is THE main evaluation criterion
- ❌ If you cannot get free hosting (cost constraint)

**In those cases, choose 3D Slicer Extension instead.**

---

### 2.8 Implementation Strategy (Web Application)

**Phase 1 - Core Backend (Weeks 1-6):**
- Set up FastAPI + Celery
- Integrate your existing preprocessing pipeline
- Implement file upload and job management
- Get basic end-to-end working

**Phase 2 - Basic Frontend (Weeks 7-10):**
- React app with upload form
- Job status tracking
- Simple file viewer (just download links)

**Phase 3 - 3D Visualization (Weeks 11-14):**
- Integrate NiiVue library
- Multi-planar views
- LR vs HR comparison
- Basic measurement tools

**Phase 4 - Polish (Weeks 15-16):**
- UI improvements
- Bug fixes
- Documentation
- Deployment

**Buffer:** Weeks 17-18 for unexpected issues

---

### 2.9 Quick Start Decision Tree

```
START: Do you have < 10 weeks remaining?
├── YES → Choose 3D Slicer Extension (fastest)
└── NO
    └── Do you want modern web-based demo?
        ├── YES → Choose Web Application
        └── NO
            └── Is visualization quality most important?
                ├── YES → Choose Desktop App (PyQt + VTK)
                └── NO → Choose 3D Slicer Extension
```

---

## 3. Quick Guide: 3D Slicer Extension Development (Alternative Path)

If you decide to go with a 3D Slicer extension instead of a web application, here's how to proceed:

### 3.1 What is 3D Slicer?

3D Slicer is an **open-source medical imaging platform** used in hospitals and research institutions worldwide. It's built with:
- **VTK** for 3D visualization
- **ITK** for image processing
- **Qt** for user interface
- **Python** for scripting

### 3.2 Why Build a Slicer Extension?

**Advantages:**
- Users already have professional medical imaging software
- Zero visualization code needed (Slicer handles all 3D rendering)
- Can package your ML model as a Slicer module
- Direct DICOM support
- Fast development (2-4 weeks for basic extension)

**Your Extension Would:**
```
User loads MRI in 3D Slicer
    ↓
Your Extension adds menu: "MRI Super-Resolution"
    ↓
User clicks: "Preprocess" or "Run Super-Resolution"
    ↓
Your Python code runs (using existing pipeline)
    ↓
Result displayed in Slicer's viewer
```

### 3.3 Quick Start Code Example

```python
# MRISuperResolution/MRISuperResolution.py
import os
import slicer
from slicer.ScriptedLoadableModule import *
import SimpleITK as sitk
import torch

class MRISuperResolution(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "MRI Super-Resolution"
        self.parent.categories = ["Filtering"]
        self.parent.dependencies = []
        self.parent.contributors = ["Your Name"]
        self.parent.helpText = """
        This module performs super-resolution on MRI scans.
        """

class MRISuperResolutionWidget(ScriptedLoadableModuleWidget):
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        
        # UI Elements
        preprocessButton = qt.QPushButton("Preprocess MRI")
        preprocessButton.toolTip = "Run preprocessing pipeline"
        preprocessButton.connect('clicked(bool)', self.onPreprocessButton)
        self.layout.addWidget(preprocessButton)
        
        inferenceButton = qt.QPushButton("Run Super-Resolution")
        inferenceButton.toolTip = "Apply SR model"
        inferenceButton.connect('clicked(bool)', self.onInferenceButton)
        self.layout.addWidget(inferenceButton)
        
        # Input/Output selectors
        self.inputSelector = slicer.qMRMLNodeComboBox()
        self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputSelector.selectNodeUponCreation = True
        self.inputSelector.addEnabled = False
        self.inputSelector.removeEnabled = False
        self.inputSelector.noneEnabled = False
        self.inputSelector.setMRMLScene(slicer.mrmlScene)
        self.layout.addWidget(self.inputSelector)
    
    def onPreprocessButton(self):
        """Run preprocessing on selected volume."""
        inputVolume = self.inputSelector.currentNode()
        if not inputVolume:
            slicer.util.errorDisplay("Please select an input volume")
            return
        
        # Get numpy array from Slicer volume
        inputArray = slicer.util.arrayFromVolume(inputVolume)
        
        # Run your existing pipeline
        from src.pipeline import MRIPreprocessingPipeline
        
        # Process...
        # (Your existing code here)
        
        # Create new volume in Slicer
        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        outputVolume.SetName(inputVolume.GetName() + "_preprocessed")
        slicer.util.updateVolumeFromArray(outputVolume, processedArray)
        
        # Copy image geometry
        outputVolume.SetOrigin(inputVolume.GetOrigin())
        outputVolume.SetSpacing(inputVolume.GetSpacing())
        
        slicer.util.setSliceViewerLayers(background=outputVolume)
    
    def onInferenceButton(self):
        """Run super-resolution model."""
        inputVolume = self.inputSelector.currentNode()
        
        # Load model (do this once at startup in real code)
        model = torch.load('model.pth')
        model.eval()
        
        # Run inference
        inputArray = slicer.util.arrayFromVolume(inputVolume)
        inputTensor = torch.from_numpy(inputArray).float().unsqueeze(0).unsqueeze(0)
        
        with torch.no_grad():
            outputTensor = model(inputTensor)
        
        outputArray = outputTensor.squeeze().numpy()
        
        # Display in Slicer
        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        outputVolume.SetName(inputVolume.GetName() + "_SR")
        slicer.util.updateVolumeFromArray(outputVolume, outputArray)
        outputVolume.SetOrigin(inputVolume.GetOrigin())
        outputVolume.SetSpacing(inputVolume.GetSpacing())
```

### 3.4 File Structure for Slicer Extension

```
MRISuperResolution/
├── MRISuperResolution.py          # Main module
├── MRISuperResolution.png         # Icon
├── CMakeLists.txt                 # Build configuration
├── Resources/
│   └── Icons/
│       └── MRISuperResolution.png
├── Testing/
│   └── Python/
│       └── test_MRISuperResolution.py
├── models/
│   └── best_model.pth             # Your trained model
└── src/                           # Your existing pipeline
    ├── pipeline.py
    ├── degradation.py
    └── ...
```

### 3.5 Development Steps

**Week 1: Setup**
```bash
# Install 3D Slicer
# Download from: https://download.slicer.org/

# Create extension
cd ~/
git clone https://github.com/Slicer/ExtensionTemplate.git MRISuperResolution
cd MRISuperResolution

# Copy your pipeline code
cp -r /path/to/your/pipeline/src ./
```

**Week 2: Core Integration**
- Integrate preprocessing pipeline
- Add UI buttons and selectors
- Handle volume conversions (Slicer ↔ NumPy)

**Week 3: Model Integration**
- Load PyTorch model
- Run inference
- Display results

**Week 4: Testing & Polish**
- Test with various MRI scans
- Add progress bars
- Error handling
- Documentation

### 3.6 Distribution

**Option 1: Extension Manager (Recommended)**
- Upload to Slicer Extension Index
- Users install with one click from Slicer
- Automatic updates

**Option 2: Manual Installation**
- Share as .zip file
- Users extract to Slicer modules folder
- Simple for small user base

### 3.7 Comparison Time Investment

| Approach | Setup | Development | Total |
|----------|-------|-------------|-------|
| Web App | 2 weeks | 12 weeks | 14-16 weeks |
| Desktop App | 3 weeks | 15 weeks | 18-20 weeks |
| **Slicer Extension** | **1 week** | **3 weeks** | **4-6 weeks** |

### 3.8 When to Choose Slicer Extension

✅ **Choose this if:**
- You have limited time (< 10 weeks)
- Your users are radiologists/researchers (already use Slicer)
- You want to focus on the algorithm, not UI
- You need professional medical imaging features (DICOM, MPR, measurements)
- You're working with a medical institution

❌ **Avoid if:**
- You want to learn web/modern development
- Target users are non-technical
- You want something unique for your portfolio
- You plan to commercialize as standalone product

---

## 4. System Architecture (Web Application)

### 4.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         WEB FRONTEND                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Upload UI    │  │ Job Status   │  │ 3D Viewer            │  │
│  │ - File Drop  │  │ - Progress   │  │ - Multi-planar View  │  │
│  │ - Validation │  │ - Queue Mgmt │  │ - Volume Rendering   │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕ REST API / WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API SERVER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ File Handler │  │ Task Queue   │  │ Authentication       │  │
│  │ - Upload     │  │ - Celery     │  │ - JWT Tokens         │  │
│  │ - Download   │  │ - Redis      │  │ - User Management    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                     PROCESSING WORKERS                           │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐│
│  │ Preprocessing Worker     │  │ Model Inference Worker       ││
│  │ - ANTsPy Pipeline        │  │ - PyTorch/ONNX              ││
│  │ - HD-BET                 │  │ - GPU Acceleration          ││
│  │ - CPU/GPU Compute        │  │ - Batch Processing          ││
│  └──────────────────────────┘  └──────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ PostgreSQL   │  │ File Storage │  │ Redis Cache          │  │
│  │ - Metadata   │  │ - MinIO/S3   │  │ - Task Status        │  │
│  │ - Job Status │  │ - NIfTI Files│  │ - Session Data       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Architectural Patterns

**Pattern Choice: Microservices-Lite**
- **API Gateway**: Single entry point (FastAPI)
- **Task Queue**: Async processing (Celery)
- **Worker Separation**: Preprocessing vs Inference isolated
- **Message Broker**: Redis for task coordination

**Why Not Full Microservices?**
- FYP scope: balance between modern architecture and maintainability
- Small team: avoid operational complexity
- Cost: single deployment easier to host

---

## 5. Technology Stack Recommendations

### 5.1 Frontend Stack

#### **Option A: React + Three.js (Recommended for FYP)**

```javascript
Tech Stack:
├── React 18             (UI framework)
├── TypeScript           (Type safety)
├── Vite                 (Build tool - faster than CRA)
├── TailwindCSS          (Styling)
├── React Query          (API state management)
├── Zustand              (Global state)
└── Medical Visualization:
    ├── @niivue/niivue   (NIfTI viewer - built for web)
    ├── Three.js         (3D rendering engine)
    └── @react-three/fiber (React + Three.js integration)
```

**Pros:**
- ✅ Large ecosystem and community support
- ✅ Excellent tooling and developer experience
- ✅ NiiVue library specifically built for medical imaging
- ✅ Easy to find tutorials and resolve issues

**Cons:**
- ⚠️ Requires learning curve for 3D visualization
- ⚠️ Bundle size can get large (optimize with code splitting)

#### **Option B: Vue 3 + Three.js**

```javascript
Tech Stack:
├── Vue 3 + Composition API
├── Vite
├── TailwindCSS
├── Pinia (state management)
└── Medical Visualization:
    ├── NiiVue
    └── TresJS (Vue + Three.js)
```

**Pros:**
- ✅ Simpler learning curve than React
- ✅ Better performance in some cases
- ✅ More intuitive for beginners

**Cons:**
- ⚠️ Smaller ecosystem for medical imaging
- ⚠️ Fewer medical imaging examples

#### **🎯 Recommendation: React + NiiVue + React Three Fiber**

### 5.2 Backend Stack

#### **Option A: FastAPI + Celery (Recommended)**

```python
Tech Stack:
├── FastAPI              (API framework)
├── Celery               (Distributed task queue)
├── Redis                (Message broker + cache)
├── PostgreSQL           (Relational database)
├── SQLAlchemy           (ORM)
├── Pydantic             (Data validation)
├── python-multipart     (File upload handling)
├── PyJWT                (Authentication)
└── Your Existing Pipeline:
    ├── ANTsPy
    ├── HD-BET
    ├── MONAI
    └── PyTorch
```

**Pros:**
- ✅ Same language as your ML pipeline (Python)
- ✅ Fast performance (async/await support)
- ✅ Automatic API documentation (Swagger)
- ✅ Easy integration with existing preprocessing code
- ✅ Excellent type hints with Pydantic

**Cons:**
- ⚠️ Celery can be complex to set up initially

#### **Option B: Flask + Celery**

**Pros:**
- ✅ Simpler, more minimalist
- ✅ Easier to learn

**Cons:**
- ⚠️ No async support
- ⚠️ Manual API documentation
- ⚠️ Slower than FastAPI

#### **🎯 Recommendation: FastAPI + Celery + Redis**

### 5.3 Model Serving

#### **Option A: Integrate with FastAPI (Simple)**
```python
# Load model once at startup
model = torch.load('model.pth')

@app.post("/inference")
async def infer(file: UploadFile):
    # Direct inference
    result = model(data)
    return result
```

**Pros:**
- ✅ Simple deployment
- ✅ Low latency

**Cons:**
- ⚠️ Ties up API server during inference
- ⚠️ Hard to scale independently

#### **Option B: Separate Model Server (Recommended for Production)**

```python
Tech Stack:
├── TorchServe          (PyTorch model serving)
├── ONNX Runtime        (Cross-platform inference)
└── FastAPI Worker      (Celery task calls model server)
```

**Pros:**
- ✅ Independent scaling
- ✅ GPU resource isolation
- ✅ Model versioning support

**Cons:**
- ⚠️ More complex architecture

#### **🎯 Recommendation for FYP: Start with Option A, refactor to Option B if needed**

### 5.4 Storage Solutions

```
Storage Requirements:
├── Raw MRI Files:      ~100-500 MB each
├── Preprocessed HR:    ~50-200 MB each
├── Preprocessed LR:    ~20-100 MB each
├── Model Output:       ~50-200 MB each
└── Intermediate Files: ~500 MB per job
```

#### **Options:**

| Solution | Pros | Cons | Cost |
|----------|------|------|------|
| **Local Filesystem** | Simple, fast | Not scalable | Free |
| **MinIO (Self-hosted S3)** | S3-compatible, scalable | Needs setup | Free |
| **AWS S3** | Managed, reliable | Ongoing cost | ~$0.023/GB |
| **Azure Blob Storage** | Good for universities | Requires account | Similar to S3 |

#### **🎯 Recommendation: MinIO for development, AWS S3 for production**

### 5.5 Database

```sql
Database Requirements:
├── User accounts
├── Job metadata (status, timestamps, errors)
├── File references (paths, URLs)
└── Processing logs
```

**PostgreSQL** is recommended:
- ✅ JSONB support for flexible metadata
- ✅ Strong ACID guarantees
- ✅ Excellent Python support (psycopg3)
- ✅ Free and open source

**Alternative: MongoDB** (if you prefer NoSQL)

---

## 6. Feature Implementation Guide

### 6.1 Feature 1: Upload & Preprocessing

#### **4.1.1 Frontend Implementation**

```typescript
// components/UploadForm.tsx
import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';

const UploadForm = () => {
  const [files, setFiles] = useState<File[]>([]);
  
  const uploadMutation = useMutation({
    mutationFn: async (files: File[]) => {
      const formData = new FormData();
      files.forEach(file => formData.append('files', file));
      
      const response = await fetch('/api/preprocess/upload', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      return response.json();
    },
    onSuccess: (data) => {
      // Data contains job_id
      // Redirect to status page
      navigate(`/jobs/${data.job_id}`);
    }
  });
  
  return (
    <div className="upload-container">
      <Dropzone
        accept={{'.nii.gz': [], '.nii': []}}
        onDrop={setFiles}
        maxSize={1024 * 1024 * 1024} // 1GB
      />
      <button onClick={() => uploadMutation.mutate(files)}>
        Upload & Process
      </button>
    </div>
  );
};
```

#### **6.1.2 Backend Implementation**

```python
# app/api/routes/preprocess.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from celery import group
from typing import List
import uuid

router = APIRouter(prefix="/preprocess", tags=["preprocessing"])

@router.post("/upload")
async def upload_and_preprocess(
    files: List[UploadFile] = File(...),
    user_id: str = Depends(get_current_user)
):
    """
    Upload one or more MRI files and trigger preprocessing.
    Returns job_id for status tracking.
    """
    # 1. Validate files
    for file in files:
        if not file.filename.endswith(('.nii.gz', '.nii')):
            raise HTTPException(400, "Only NIfTI files allowed")
    
    # 2. Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # 3. Save files to storage
    file_paths = []
    for file in files:
        file_path = await save_to_storage(file, job_id)
        file_paths.append(file_path)
    
    # 4. Create job record in database
    job = await db_create_job(
        job_id=job_id,
        user_id=user_id,
        status="pending",
        input_files=file_paths
    )
    
    # 5. Trigger Celery task
    task = preprocess_pipeline_task.apply_async(
        args=[job_id, file_paths],
        task_id=job_id
    )
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Preprocessing started",
        "estimated_time": len(files) * 15  # 15 min per file
    }

# app/tasks/preprocess_tasks.py
from celery import shared_task
from src.pipeline import MRIPreprocessingPipeline

@shared_task(bind=True, max_retries=3)
def preprocess_pipeline_task(self, job_id: str, file_paths: List[str]):
    """
    Execute the preprocessing pipeline for uploaded files.
    """
    try:
        # 1. Update job status
        update_job_status(job_id, "processing", progress=0)
        
        # 2. Initialize pipeline
        pipeline = MRIPreprocessingPipeline("configs/config.yaml")
        
        # 3. Process each file
        for i, file_path in enumerate(file_paths):
            try:
                # Run preprocessing
                pipeline.process_subject(file_path)
                
                # Update progress
                progress = ((i + 1) / len(file_paths)) * 100
                update_job_status(job_id, "processing", progress=progress)
                
            except Exception as e:
                # Log error but continue with other files
                log_file_error(job_id, file_path, str(e))
        
        # 4. Mark as complete
        output_files = get_output_files(job_id)
        update_job_status(
            job_id, 
            "completed", 
            progress=100,
            output_files=output_files
        )
        
        return {"status": "success", "output_files": output_files}
        
    except Exception as e:
        # 5. Handle failure
        update_job_status(job_id, "failed", error=str(e))
        raise self.retry(exc=e, countdown=60)  # Retry after 1 min
```

#### **6.1.3 Job Status Tracking**

```typescript
// components/JobStatus.tsx
const JobStatus = ({ jobId }: { jobId: string }) => {
  const { data, isLoading } = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => fetch(`/api/jobs/${jobId}`).then(r => r.json()),
    refetchInterval: (data) => {
      // Poll every 5 seconds while processing
      return data?.status === 'processing' ? 5000 : false;
    }
  });
  
  if (isLoading) return <Spinner />;
  
  return (
    <div>
      <h2>Job Status: {data.status}</h2>
      <ProgressBar value={data.progress} />
      
      {data.status === 'completed' && (
        <div>
          <h3>Output Files:</h3>
          <FileList files={data.output_files} />
          <button onClick={() => downloadAll(data.output_files)}>
            Download All
          </button>
        </div>
      )}
      
      {data.status === 'failed' && (
        <ErrorMessage error={data.error} />
      )}
    </div>
  );
};
```

#### **6.1.4 WebSocket Alternative (Real-time Updates)**

```python
# app/api/websocket.py
from fastapi import WebSocket

@app.websocket("/ws/jobs/{job_id}")
async def job_status_websocket(websocket: WebSocket, job_id: str):
    await websocket.accept()
    
    # Subscribe to Redis pub/sub for job updates
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"job:{job_id}")
    
    try:
        while True:
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                # Forward update to WebSocket client
                await websocket.send_json(json.loads(message['data']))
    except WebSocketDisconnect:
        pubsub.unsubscribe(f"job:{job_id}")
```

### 6.2 Feature 2: Model Inference

#### **6.2.1 Model Loading Strategy**

```python
# app/models/model_loader.py
import torch
from monai.networks.nets import SwinUNETR

class ModelManager:
    def __init__(self):
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def load_model(self, checkpoint_path: str):
        """Load model once at startup."""
        self.model = SwinUNETR(
            img_size=(96, 96, 96),
            in_channels=1,
            out_channels=1,
            feature_size=48
        )
        
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()
        self.model.to(self.device)
        
        print(f"Model loaded on {self.device}")
    
    @torch.no_grad()
    def infer(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """Run inference on input tensor."""
        input_tensor = input_tensor.to(self.device)
        output = self.model(input_tensor)
        return output.cpu()

# Initialize globally
model_manager = ModelManager()

# Load at startup
@app.on_event("startup")
async def load_ml_model():
    model_manager.load_model("checkpoints/best_model.pth")
```

#### **6.2.2 Inference API**

```python
# app/api/routes/inference.py
@router.post("/infer")
async def run_inference(
    lr_file_id: str,
    user_id: str = Depends(get_current_user)
):
    """
    Run super-resolution inference on a preprocessed LR file.
    """
    # 1. Verify file belongs to user
    file_record = await get_file_record(lr_file_id, user_id)
    if not file_record:
        raise HTTPException(404, "File not found")
    
    # 2. Generate inference job ID
    inference_job_id = str(uuid.uuid4())
    
    # 3. Trigger Celery task
    task = inference_task.apply_async(
        args=[inference_job_id, file_record.path],
        task_id=inference_job_id
    )
    
    return {
        "job_id": inference_job_id,
        "status": "pending"
    }

# app/tasks/inference_tasks.py
@shared_task(bind=True)
def inference_task(self, job_id: str, lr_file_path: str):
    """Execute model inference."""
    try:
        update_job_status(job_id, "processing", progress=0)
        
        # 1. Load LR image
        lr_image = ants.image_read(lr_file_path)
        lr_array = lr_image.numpy()
        
        # 2. Preprocess for model (normalize, add batch/channel dims)
        lr_tensor = torch.from_numpy(lr_array).float().unsqueeze(0).unsqueeze(0)
        
        # 3. Run inference
        update_job_status(job_id, "processing", progress=30)
        hr_tensor = model_manager.infer(lr_tensor)
        
        # 4. Post-process (remove batch/channel dims)
        hr_array = hr_tensor.squeeze().numpy()
        
        # 5. Convert back to ANTs image (preserve metadata)
        hr_image = ants.from_numpy(
            hr_array,
            origin=lr_image.origin,
            spacing=lr_image.spacing,
            direction=lr_image.direction
        )
        
        # 6. Save output
        update_job_status(job_id, "processing", progress=80)
        output_path = f"outputs/{job_id}_sr.nii.gz"
        ants.image_write(hr_image, output_path)
        
        # 7. Complete
        update_job_status(
            job_id, 
            "completed", 
            progress=100,
            output_file=output_path
        )
        
        return {"status": "success", "output_file": output_path}
        
    except Exception as e:
        update_job_status(job_id, "failed", error=str(e))
        raise

```

#### **6.2.3 Batch Inference (Multiple Files)**

```python
@router.post("/infer/batch")
async def batch_inference(
    lr_file_ids: List[str],
    user_id: str = Depends(get_current_user)
):
    """Run inference on multiple files."""
    batch_job_id = str(uuid.uuid4())
    
    # Create parent job
    await create_batch_job(batch_job_id, lr_file_ids)
    
    # Trigger tasks in parallel (Celery group)
    tasks = group(
        inference_task.s(f"{batch_job_id}_{i}", file_id)
        for i, file_id in enumerate(lr_file_ids)
    )
    tasks.apply_async()
    
    return {"batch_job_id": batch_job_id}
```

### 6.3 Feature 3: 3D Visualization

#### **6.3.1 NiiVue Integration (Recommended - Easiest)**

```typescript
// components/MRIViewer.tsx
import { Niivue } from '@niivue/niivue';
import { useEffect, useRef } from 'react';

const MRIViewer = ({ lrFileUrl, hrFileUrl }: { lrFileUrl: string, hrFileUrl: string }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const nv = useRef<Niivue | null>(null);
  
  useEffect(() => {
    if (!canvasRef.current) return;
    
    // Initialize NiiVue
    nv.current = new Niivue();
    nv.current.attachToCanvas(canvasRef.current);
    
    // Load volumes
    nv.current.loadVolumes([
      { url: lrFileUrl, colormap: 'gray', opacity: 1 },
      { url: hrFileUrl, colormap: 'hot', opacity: 0.5 }
    ]);
    
    // Configure view
    nv.current.setSliceType(nv.current.sliceTypeMultiplanar);
    
    return () => {
      nv.current?.destroy();
    };
  }, [lrFileUrl, hrFileUrl]);
  
  return (
    <div className="viewer-container">
      <canvas ref={canvasRef} width={800} height={600} />
      
      {/* Controls */}
      <div className="controls">
        <button onClick={() => nv.current?.setSliceType(0)}>
          Axial
        </button>
        <button onClick={() => nv.current?.setSliceType(1)}>
          Coronal
        </button>
        <button onClick={() => nv.current?.setSliceType(2)}>
          Sagittal
        </button>
        <button onClick={() => nv.current?.setSliceType(4)}>
          Multi-planar
        </button>
      </div>
    </div>
  );
};
```

**NiiVue Features:**
- ✅ Multi-planar reconstruction (MPR)
- ✅ Volume rendering
- ✅ Overlay support (compare LR vs HR)
- ✅ Built specifically for NIfTI files
- ✅ Crosshair navigation
- ✅ Intensity windowing
- ✅ Drawing ROIs

#### **6.3.2 Advanced Comparison View**

```typescript
// components/ComparisonViewer.tsx
const ComparisonViewer = () => {
  const [viewMode, setViewMode] = useState<'side-by-side' | 'overlay' | 'diff'>('side-by-side');
  const [opacity, setOpacity] = useState(0.5);
  
  return (
    <div className="comparison-viewer">
      {/* View Mode Toggle */}
      <div className="toolbar">
        <button onClick={() => setViewMode('side-by-side')}>
          Side by Side
        </button>
        <button onClick={() => setViewMode('overlay')}>
          Overlay
        </button>
        <button onClick={() => setViewMode('diff')}>
          Difference Map
        </button>
        
        {viewMode === 'overlay' && (
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={opacity}
            onChange={(e) => setOpacity(parseFloat(e.target.value))}
          />
        )}
      </div>
      
      {/* Viewer Grid */}
      {viewMode === 'side-by-side' ? (
        <div className="grid grid-cols-2 gap-4">
          <MRIViewer fileUrl={lrFileUrl} title="Low Resolution" />
          <MRIViewer fileUrl={hrFileUrl} title="Super Resolution" />
        </div>
      ) : viewMode === 'overlay' ? (
        <MRIViewer 
          lrFileUrl={lrFileUrl} 
          hrFileUrl={hrFileUrl}
          hrOpacity={opacity}
        />
      ) : (
        <DifferenceMapViewer lrFileUrl={lrFileUrl} hrFileUrl={hrFileUrl} />
      )}
    </div>
  );
};
```

#### **6.3.3 Alternative: VTK.js (More Advanced)**

```typescript
// For more complex 3D rendering
import vtkFullScreenRenderWindow from '@kitware/vtk.js/Rendering/Misc/FullScreenRenderWindow';
import vtkNIFTIReader from '@kitware/vtk.js/IO/Images/NIFTIReader';
import vtkVolume from '@kitware/vtk.js/Rendering/Core/Volume';

const VTKViewer = ({ fileUrl }: { fileUrl: string }) => {
  useEffect(() => {
    const fullScreenRenderer = vtkFullScreenRenderWindow.newInstance();
    const renderer = fullScreenRenderer.getRenderer();
    const renderWindow = fullScreenRenderer.getRenderWindow();
    
    // Load NIFTI
    const reader = vtkNIFTIReader.newInstance();
    reader.setUrl(fileUrl).then(() => {
      const data = reader.getOutputData();
      
      const actor = vtkVolume.newInstance();
      const mapper = vtkVolumeMapper.newInstance();
      mapper.setInputData(data);
      actor.setMapper(mapper);
      
      renderer.addVolume(actor);
      renderer.resetCamera();
      renderWindow.render();
    });
    
    return () => {
      fullScreenRenderer.delete();
    };
  }, [fileUrl]);
  
  return <div id="vtk-container" />;
};
```

**VTK.js vs NiiVue:**

| Feature | NiiVue | VTK.js |
|---------|--------|--------|
| Medical imaging focus | ✅ Yes | ⚠️ General 3D |
| Learning curve | Easy | Steep |
| MPR views | ✅ Built-in | Need custom code |
| Volume rendering | ✅ Good | ✅ Excellent |
| Documentation | ✅ Good | ⚠️ Complex |
| Bundle size | Small | Large |

**🎯 Recommendation: Start with NiiVue, consider VTK.js only if you need advanced rendering**

---

## 7. Data Flow & API Design

### 7.1 RESTful API Endpoints

```
Authentication:
POST   /api/auth/register          - User registration
POST   /api/auth/login             - Get JWT token
POST   /api/auth/refresh           - Refresh token

Preprocessing:
POST   /api/preprocess/upload      - Upload & start preprocessing
GET    /api/jobs/{job_id}          - Get job status
GET    /api/jobs                   - List user's jobs
DELETE /api/jobs/{job_id}          - Cancel/delete job

Files:
GET    /api/files/{file_id}        - Download file
GET    /api/files/{file_id}/info   - Get file metadata
DELETE /api/files/{file_id}        - Delete file

Inference:
POST   /api/inference/single       - Single file inference
POST   /api/inference/batch        - Batch inference
GET    /api/inference/{job_id}     - Inference job status

Visualization:
GET    /api/files/{file_id}/serve  - Serve file for viewer (with byte-range support)
```

### 7.2 Database Schema

```sql
-- users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- jobs table
CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_type VARCHAR(50) NOT NULL, -- 'preprocessing' or 'inference'
    status VARCHAR(50) NOT NULL,    -- 'pending', 'processing', 'completed', 'failed'
    progress INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    metadata JSONB -- Flexible storage for job-specific data
);

-- files table
CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    file_type VARCHAR(50) NOT NULL, -- 'raw', 'hr', 'lr', 'sr'
    filename VARCHAR(255) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB -- Image dimensions, spacing, etc.
);

-- Create indexes
CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_files_user_id ON files(user_id);
CREATE INDEX idx_files_job_id ON files(job_id);
```

### 7.3 File Serving for Visualization

```python
# app/api/routes/files.py
from fastapi.responses import FileResponse, StreamingResponse
import aiofiles

@router.get("/files/{file_id}/serve")
async def serve_file(
    file_id: str,
    range: str | None = Header(None),
    user_id: str = Depends(get_current_user)
):
    """
    Serve file with support for HTTP Range requests (essential for large files).
    """
    # 1. Get file record
    file_record = await get_file_record(file_id, user_id)
    
    # 2. Handle range requests (for streaming large files)
    if range:
        # Parse range header: "bytes=0-1023"
        start, end = parse_range_header(range, file_record.file_size_bytes)
        
        async def file_iterator():
            async with aiofiles.open(file_record.storage_path, 'rb') as f:
                await f.seek(start)
                chunk_size = 64 * 1024  # 64KB chunks
                bytes_to_read = end - start + 1
                
                while bytes_to_read > 0:
                    chunk = await f.read(min(chunk_size, bytes_to_read))
                    if not chunk:
                        break
                    bytes_to_read -= len(chunk)
                    yield chunk
        
        return StreamingResponse(
            file_iterator(),
            media_type="application/octet-stream",
            headers={
                "Content-Range": f"bytes {start}-{end}/{file_record.file_size_bytes}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(end - start + 1)
            },
            status_code=206  # Partial Content
        )
    
    # 3. Full file response
    return FileResponse(
        file_record.storage_path,
        media_type="application/octet-stream",
        filename=file_record.filename
    )
```

---

## 8. Security & Privacy Considerations

### 8.1 Medical Data Privacy (HIPAA-Aware Design)

```python
# 1. File Anonymization
def anonymize_nifti(file_path: str) -> str:
    """Remove patient metadata from NIfTI headers."""
    img = nib.load(file_path)
    
    # Clear header fields that might contain PHI
    img.header['descrip'] = b''
    img.header['db_name'] = b''
    
    # Save anonymized version
    anon_path = file_path.replace('.nii.gz', '_anon.nii.gz')
    nib.save(img, anon_path)
    
    return anon_path

# 2. Audit Logging
def log_data_access(user_id: str, file_id: str, action: str):
    """Log all access to medical data."""
    audit_log.insert({
        'timestamp': datetime.utcnow(),
        'user_id': user_id,
        'file_id': file_id,
        'action': action,
        'ip_address': request.client.host
    })
```

### 8.2 Authentication & Authorization

```python
# app/auth/jwt_handler.py
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

### 8.3 File Upload Security

```python
# app/utils/file_validation.py
import magic

ALLOWED_EXTENSIONS = {'.nii.gz', '.nii'}
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB

async def validate_upload(file: UploadFile) -> bool:
    """Validate uploaded file for security."""
    
    # 1. Check extension
    if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(400, "Only NIfTI files allowed")
    
    # 2. Check file size
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)     # Reset
    
    if size > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large")
    
    # 3. Check MIME type (magic number validation)
    content = await file.read(1024)
    file.file.seek(0)
    
    mime = magic.from_buffer(content, mime=True)
    if mime not in ['application/gzip', 'application/x-gzip']:
        raise HTTPException(400, "Invalid file format")
    
    return True
```

### 8.4 Rate Limiting

```python
# app/middleware/rate_limit.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/preprocess/upload")
@limiter.limit("10/hour")  # Max 10 uploads per hour per IP
async def upload_endpoint(...):
    ...
```

---

## 9. Deployment Architecture

### 9.1 Development Setup (Local)

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: mri_sr_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  # Redis (Message Broker & Cache)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  # MinIO (S3-compatible storage)
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: password
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
  
  # FastAPI Backend
  backend:
    build: ./backend
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - minio
    volumes:
      - ./data:/app/data
      - ./configs:/app/configs
  
  # Celery Worker (CPU tasks - preprocessing)
  worker_preprocess:
    build: ./backend
    command: celery -A app.celery_app worker --loglevel=info -Q preprocessing
    env_file: .env
    depends_on:
      - redis
      - postgres
    volumes:
      - ./data:/app/data
  
  # Celery Worker (GPU tasks - inference)
  worker_inference:
    build: ./backend
    command: celery -A app.celery_app worker --loglevel=info -Q inference --concurrency=1
    env_file: .env
    depends_on:
      - redis
      - postgres
    volumes:
      - ./data:/app/data
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  
  # React Frontend
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      REACT_APP_API_URL: http://localhost:8000

volumes:
  postgres_data:
  minio_data:
```

### 9.2 Production Deployment Options

#### **Option A: Cloud VM (AWS EC2 / Azure VM)**

```
Architecture:
├── Frontend: Nginx serving React build
├── Backend: Gunicorn + FastAPI
├── Workers: Celery (2 preprocessing + 1 GPU inference)
├── Database: RDS PostgreSQL
├── Storage: S3
└── Message Queue: ElastiCache Redis
```

**Estimated AWS Cost:**
- EC2 t3.xlarge (4 vCPU, 16GB RAM): $120/month
- EC2 g4dn.xlarge (GPU for inference): $400/month
- RDS db.t3.small: $30/month
- S3 storage (1TB): $23/month
- **Total: ~$573/month**

#### **Option B: Kubernetes (Google Cloud / Azure AKS)**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-registry/mri-sr-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

**Benefits:**
- Auto-scaling
- Load balancing
- Rolling updates
- Self-healing

**Cost:** Similar to VM, but more operational overhead

#### **Option C: Serverless (AWS Lambda + ECS for workers)**

Not recommended due to:
- Long-running tasks (Lambda 15 min limit)
- Large dependencies (ANTsPy, PyTorch)
- GPU requirements

### 9.3 CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pytest backend/tests
          npm test --prefix frontend
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: |
          docker build -t $ECR_REGISTRY/backend:$GITHUB_SHA ./backend
          docker build -t $ECR_REGISTRY/frontend:$GITHUB_SHA ./frontend
      
      - name: Push to ECR
        run: |
          docker push $ECR_REGISTRY/backend:$GITHUB_SHA
          docker push $ECR_REGISTRY/frontend:$GITHUB_SHA
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to EC2
        run: |
          ssh $EC2_HOST "docker-compose pull && docker-compose up -d"
```

---

## 10. Development Roadmap

### Phase 1: MVP (4-6 weeks)

**Week 1-2: Backend Foundation**
- [ ] FastAPI project setup
- [ ] Database models & migrations
- [ ] JWT authentication
- [ ] File upload endpoint
- [ ] Basic Celery task

**Week 3-4: Preprocessing Integration**
- [ ] Integrate existing pipeline code
- [ ] Create preprocessing Celery task
- [ ] Job status tracking
- [ ] Error handling & logging

**Week 5-6: Frontend Basic UI**
- [ ] React project setup (Vite + TypeScript)
- [ ] Upload form
- [ ] Job status page
- [ ] File download

### Phase 2: Model Integration (2-3 weeks)

**Week 7-8:**
- [ ] Model loading & initialization
- [ ] Inference Celery task
- [ ] Inference API endpoints
- [ ] Batch inference support

**Week 9:**
- [ ] Frontend inference UI
- [ ] Model output visualization
- [ ] Performance optimization

### Phase 3: 3D Visualization (3-4 weeks)

**Week 10-11:**
- [ ] Integrate NiiVue library
- [ ] Basic 3D viewer component
- [ ] Multi-planar views
- [ ] Navigation controls

**Week 12-13:**
- [ ] Comparison view (side-by-side)
- [ ] Overlay mode with opacity control
- [ ] Difference map calculation
- [ ] Measurement tools (optional)

### Phase 4: Polish & Deployment (2 weeks)

**Week 14:**
- [ ] UI/UX improvements
- [ ] Error handling refinement
- [ ] Loading states & feedback
- [ ] Mobile responsiveness

**Week 15:**
- [ ] Docker setup
- [ ] Production environment config
- [ ] Deployment to cloud
- [ ] Documentation

**Week 16: Buffer for testing & bug fixes**

---

## 11. Cost & Resource Estimation

### 11.1 Development Costs

| Resource | Cost | Notes |
|----------|------|-------|
| **Domain Name** | $12/year | .com domain |
| **SSL Certificate** | Free | Let's Encrypt |
| **Development Tools** | Free | VS Code, Git, Docker |
| **Cloud Credits** | $300-500 | AWS/GCP free tier + student credits |

### 11.2 Hosting Costs (Monthly)

#### Budget Option (Development/Demo):
```
Single VPS (Hetzner/DigitalOcean)
- 8 vCPU, 32GB RAM, 500GB SSD: $60/month
- GPU not included (CPU inference only)
Total: ~$60/month
```

#### Production Option:
```
AWS Stack:
- EC2 t3.xlarge (API server): $120/month
- EC2 g4dn.xlarge (GPU inference): $400/month
- RDS PostgreSQL: $30/month
- S3 Storage (1TB): $23/month
- Data Transfer: $20/month
Total: ~$593/month
```

#### University Option:
```
Many universities provide:
- Free VM hosting
- Free GPU access (research clusters)
- Free cloud credits ($100-1000)
Total: $0/month (best for FYP!)
```

### 11.3 Hardware Requirements

**Development Machine:**
- 16GB RAM minimum (32GB recommended)
- Modern CPU (i5/Ryzen 5 or better)
- 500GB SSD
- GPU optional for testing inference

**Production Server:**
- Preprocessing: 32GB RAM, 8+ CPU cores
- Inference: 16GB+ VRAM GPU (RTX 3090, A5000, or cloud GPU)
- Storage: 1TB+ for user data

---

## 12. Recommended Learning Path

### 12.1 For Frontend Developer

**Week 1-2: React Fundamentals**
- React docs: https://react.dev
- TypeScript: https://www.typescriptlang.org/docs/
- React Query: https://tanstack.com/query/latest

**Week 3: 3D Graphics Basics**
- Three.js fundamentals: https://threejs.org/manual/
- WebGL concepts

**Week 4: Medical Imaging**
- NiiVue documentation: https://github.com/niivue/niivue
- NIfTI format basics

### 12.2 For Backend Developer

**Week 1: FastAPI**
- Official tutorial: https://fastapi.tiangolo.com/tutorial/
- Async programming in Python

**Week 2: Task Queues**
- Celery documentation: https://docs.celeryq.dev/
- Redis basics

**Week 3: Docker & Deployment**
- Docker tutorial: https://docs.docker.com/get-started/
- Docker Compose

**Week 4: Integration**
- Connect all components
- Testing & debugging

---

## 13. Critical Success Factors

### ✅ Must-Have Features
1. Reliable file upload (with resume capability)
2. Clear job status feedback
3. Basic 3D visualization (MPR views)
4. Secure authentication
5. Error handling & logging

### 🎯 Nice-to-Have Features
1. Email notifications
2. Batch operations
3. Advanced visualization (volume rendering)
4. Annotation tools
5. Result sharing

### ⚠️ Common Pitfalls to Avoid
1. **Underestimating file sizes** - NIfTI files are large, optimize transfers
2. **Ignoring long task times** - Provide accurate time estimates
3. **Poor error messages** - Medical imaging has many edge cases
4. **No progress feedback** - Users need to know processing status
5. **Forgetting metadata** - Preserve spatial information in outputs

---

## 14. Testing Strategy

### 14.1 Backend Testing

```python
# tests/test_preprocessing.py
import pytest
from app.tasks.preprocess_tasks import preprocess_pipeline_task

@pytest.mark.celery(result_backend='redis://')
def test_preprocessing_task(celery_worker, sample_nifti_file):
    """Test preprocessing task executes successfully."""
    job_id = "test-job-123"
    result = preprocess_pipeline_task.apply(
        args=[job_id, [sample_nifti_file]]
    ).get(timeout=300)
    
    assert result['status'] == 'success'
    assert len(result['output_files']) > 0
```

### 14.2 Frontend Testing

```typescript
// tests/UploadForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { UploadForm } from '../components/UploadForm';

test('validates file types', async () => {
  render(<UploadForm />);
  
  const file = new File(['dummy'], 'test.txt', { type: 'text/plain' });
  const input = screen.getByLabelText('Upload');
  
  fireEvent.change(input, { target: { files: [file] } });
  
  expect(await screen.findByText(/only nifti files/i)).toBeInTheDocument();
});
```

### 14.3 Integration Testing

```python
# tests/integration/test_full_pipeline.py
async def test_full_workflow(client, auth_token):
    """Test complete workflow: upload → preprocess → infer → download."""
    
    # 1. Upload file
    with open('tests/fixtures/test_scan.nii.gz', 'rb') as f:
        response = await client.post(
            '/api/preprocess/upload',
            files={'files': f},
            headers={'Authorization': f'Bearer {auth_token}'}
        )
    assert response.status_code == 200
    job_id = response.json()['job_id']
    
    # 2. Wait for completion
    # ... polling logic ...
    
    # 3. Run inference
    # ... inference request ...
    
    # 4. Download result
    # ... download test ...
```

---

## 15. Documentation & Handover

### 15.1 Required Documentation

1. **README.md** - Setup instructions
2. **API_DOCS.md** - API endpoint reference
3. **DEPLOYMENT.md** - Deployment guide
4. **ARCHITECTURE.md** - System design overview
5. **USER_GUIDE.md** - End-user instructions

### 15.2 Code Documentation

```python
# Use docstrings for all public functions
def preprocess_pipeline_task(job_id: str, file_paths: List[str]) -> dict:
    """
    Execute MRI preprocessing pipeline on uploaded files.
    
    This task performs:
    1. Brain extraction (HD-BET)
    2. N4 bias correction
    3. Intensity normalization
    4. MNI registration
    
    Args:
        job_id: Unique identifier for this processing job
        file_paths: List of absolute paths to input NIfTI files
    
    Returns:
        dict containing:
            - status: 'success' or 'failed'
            - output_files: List of generated file paths
            - errors: List of error messages (if any)
    
    Raises:
        CeleryRetryException: On transient failures (retried up to 3 times)
        
    Example:
        >>> result = preprocess_pipeline_task.apply_async(
        ...     args=['job-123', ['/data/scan1.nii.gz']],
        ...     task_id='job-123'
        ... )
    """
    ...
```

---

## 16. Final Recommendations

### 🎯 Recommended Tech Stack Summary

| Layer | Technology | Reasoning |
|-------|------------|-----------|
| **Frontend** | React + TypeScript | Industry standard, great ecosystem |
| **UI Framework** | TailwindCSS | Rapid development |
| **3D Viewer** | NiiVue | Built for medical imaging |
| **State Management** | Zustand + React Query | Simple, efficient |
| **Backend** | FastAPI | Fast, modern, Python integration |
| **Task Queue** | Celery + Redis | Robust, scalable |
| **Database** | PostgreSQL | Reliable, feature-rich |
| **Storage** | MinIO (dev) / S3 (prod) | S3-compatible, cost-effective |
| **Deployment** | Docker Compose | Simple yet powerful |

### 🚀 Getting Started Steps

1. **Week 1: Setup**
   ```bash
   # Backend
   mkdir mri-sr-web && cd mri-sr-web
   mkdir backend frontend
   
   # Initialize backend
   cd backend
   poetry init
   poetry add fastapi celery redis sqlalchemy
   
   # Initialize frontend
   cd ../frontend
   npm create vite@latest . -- --template react-ts
   npm install @niivue/niivue @tanstack/react-query
   ```

2. **Week 2: Core Features**
   - Implement file upload endpoint
   - Create database models
   - Build basic frontend form

3. **Week 3: Integration**
   - Connect to your existing pipeline
   - Set up Celery tasks
   - Test end-to-end

### 📞 Support Resources

- **FastAPI Discord**: Discord community
- **React Reddit**: r/reactjs
- **Medical Imaging**: Check MONAI forums
- **Stack Overflow**: Tag questions appropriately

---

## 17. Conclusion

This architecture provides a **scalable, maintainable foundation** for your FYP. Key advantages:

✅ **Separation of Concerns**: Frontend, API, and workers are independent  
✅ **Async Processing**: Long tasks don't block user interface  
✅ **Modern Stack**: Industry-relevant technologies  
✅ **Medical Imaging Focus**: Proper handling of NIfTI files and 3D visualization  
✅ **Production-Ready**: Can scale beyond FYP to real deployment  

**Estimated Development Time**: 14-16 weeks for fully functional system

**Team Suggestion**:
- 2 developers: 12-14 weeks
- 3 developers: 10-12 weeks (1 frontend, 1 backend, 1 integration)

Good luck with your Final Year Project! 🎓

---

## Appendix A: Sample File Structure

```
mri-sr-web/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── celery_app.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── preprocess.py
│   │   │   │   ├── inference.py
│   │   │   │   └── files.py
│   │   │   └── dependencies.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   └── file.py
│   │   ├── schemas/
│   │   │   └── ...
│   │   ├── tasks/
│   │   │   ├── preprocess_tasks.py
│   │   │   └── inference_tasks.py
│   │   └── utils/
│   │       ├── file_handler.py
│   │       └── model_loader.py
│   ├── src/  (your existing pipeline)
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadForm.tsx
│   │   │   ├── JobStatus.tsx
│   │   │   ├── MRIViewer.tsx
│   │   │   └── ComparisonViewer.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Upload.tsx
│   │   │   ├── Jobs.tsx
│   │   │   └── Viewer.tsx
│   │   ├── hooks/
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
├── .env.example
└── README.md
```

---

**Document Version**: 1.0  
**Last Updated**: February 22, 2026  
**Authors**: Technical Architecture Team  
**Review Status**: Ready for Implementation
