# 🧬 PharmaGuard - AI-Powered Pharmacogenomics Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

> An AI-powered web application that analyzes patient genetic data (VCF files) and drug prescriptions to predict personalized pharmacogenomic risks, delivering clinically actionable recommendations powered by Google Gemini LLM.

---

## 📺 Demo & Presentation

- **🌐 Live Demo:** https://pharmaguard-nullpoint.onrender.com/
- **🎥 LinkedIn Video:** 

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [cURL Examples](#-curl-examples)
- [Performance & Limits](#-performance--limits)
- [Security Considerations](#-security-considerations)
- [Troubleshooting & FAQ](#-troubleshooting--faq)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Team](#-team)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**PharmaGuard** addresses the critical challenge of adverse drug reactions (ADRs) by leveraging pharmacogenomics and artificial intelligence. The platform analyzes patient genetic variants from VCF files and cross-references them with CPIC (Clinical Pharmacogenetics Implementation Consortium) guidelines to provide:

- **Real-time risk assessment** for drug-gene interactions
- **Personalized dosage recommendations** based on metabolic phenotypes
- **LLM-generated clinical explanations** for healthcare professionals
- **Evidence-based guidance** aligned with CPIC Level A recommendations

### Problem Statement
Adverse drug reactions cause ~100,000 deaths annually in the US. Genetic variations affect drug metabolism, requiring personalized treatment approaches.

### Solution
PharmaGuard bridges the gap between genetic testing and clinical decision-making by automating pharmacogenomic analysis and providing actionable insights in seconds.

---

## ⚡ Quick Start

Get PharmaGuard running in under 5 minutes:

```bash
# 1. Clone repository
git clone https://github.com/Shr3y4sm/PharmaGuard_NullPoint.git
cd PharmaGuard_NullPoint

# 2. Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 5. Run application
python app.py
```

**Open browser:** http://localhost:5000

Test with sample file:
- Upload: `data/sample_poor_metabolizer.vcf`
- Drug: `CODEINE`


---

## ✨ Key Features

### 🔬 **Genetic Analysis**
- ✅ VCF v4.2 file parsing with INFO field extraction (GENE, STAR, RS)
- ✅ Support for 6 pharmacogenomic genes: CYP2D6, CYP2C19, CYP2C9, SLCO1B1, TPMT, DPYD
- ✅ Diplotype-to-phenotype mapping (PM, IM, NM, RM, URM classifications)
- ✅ Confidence scoring based on data completeness

### 💊 **Drug Safety Assessment**
- ✅ Analysis of 6 critical drugs: CODEINE, WARFARIN, CLOPIDOGREL, SIMVASTATIN, AZATHIOPRINE, FLUOROURACIL
- ✅ **Gemini Fallback**: Automatic LLM analysis for any drug not in CPIC database
- ✅ CPIC guideline integration (Level A evidence)
- ✅ Risk stratification: Safe, Adjust Dosage, Toxic, Ineffective, Unknown
- ✅ Multi-drug analysis support (comma-separated input)

### 🤖 **AI-Powered Recommendations**
- ✅ Google Gemini 2.5 Flash integration for clinical insights
- ✅ Structured JSON responses with dosage adjustments
- ✅ Mechanism of action explanations
- ✅ Drug-drug interaction warnings
- ✅ **Fallback LLM**: Analyzes unsupported drugs using Gemini

### 🎨 **Interactive Web Interface**
- ✅ Drag-and-drop file upload with validation
- ✅ Real-time analysis with loading states
- ✅ Color-coded risk badges (🟢 Safe, 🟠 Adjust, 🔴 Toxic, 🔵 Review)
- ✅ Expandable tabs: Pharmacogenic Profile, Clinical Recommendations, Explanations
- ✅ Downloadable JSON reports + copy-to-clipboard

### 🛡️ **Quality & Security**
- ✅ 5MB file size limit enforcement (client + server)
- ✅ File type validation (.vcf only)
- ✅ Comprehensive error handling with user-friendly messages
- ✅ Environment variable management (.env for API keys)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  HTML5 UI (Drag-Drop, Forms, Result Display)            │  │
│  │  JavaScript (Fetch API, Dynamic DOM Updates)            │  │
│  │  CSS3 (Responsive Design, Color-Coded Risk Badges)      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP POST (VCF + Drugs)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FLASK WEB SERVER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Routes: / (UI), /analyze (HTML), /api/analysis (JSON)  │  │
│  │  Error Handlers: 413 (File Size), 400/500 (Validation)  │  │
│  │  Config: 5MB Max Upload, CORS, Session Management       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌─────────────────┐ ┌────────────┐ ┌──────────────┐
│  VCF PARSER     │ │ CPIC ENGINE│ │  LLM SERVICE │
│  • Parse VCF    │ │ • Load Data│ │  • Gemini AI │
│  • Extract INFO │ │ • Filter   │ │  • Prompting │
│  • Validate     │ │ • Match    │ │  • JSON Parse│
└────────┬────────┘ └─────┬──────┘ └──────┬───────┘
         │                │                │
         ▼                ▼                ▼
┌─────────────────────────────────────────────────────────┐
│              ANALYSIS PIPELINE                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │  1. Drug-Gene Matcher: Validate drug-gene pairs   │ │
│  │  2. Phenotype Engine: Diplotype → Phenotype       │ │
│  │  3. Risk Assessment: Phenotype → Risk Label       │ │
│  │  4. Response Builder: Structured JSON Output      │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                   DATA SOURCES                           │
│  • cpic_gene-drug_pairs.xlsx (300+ drug-gene mappings) │
│  • Phenotype Mapping Database (650+ diplotype rules)   │
│  • Google Gemini API (Clinical recommendations)        │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input:** VCF file + drug name(s) uploaded via web interface
2. **VCF Parsing:** Extract variants (GENE, STAR, RS) from INFO field
3. **Drug Matching:** Validate drugs against CPIC database, identify primary genes
4. **Phenotype Determination:** Map diplotypes to metabolic phenotypes (NM, PM, IM, etc.)
5. **Risk Assessment:** Calculate risk labels and confidence scores
6. **LLM Enhancement:** Generate clinical recommendations via Gemini API
7. **Response:** Return structured JSON with all analysis results

---

## 🛠️ Tech Stack

### **Backend**
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Flask** | 3.0.0 | Web framework & REST API |
| **pandas** | 2.3.3 | Data processing & CPIC data manipulation |
| **openpyxl** | 3.1.2 | Excel file parsing (CPIC database) |
| **requests** | 2.31.0 | HTTP client for Gemini API calls |
| **python-dotenv** | 1.0.0 | Environment variable management |

### **Frontend**
| Technology | Purpose |
|------------|---------|
| **HTML5** | Semantic markup & structure |
| **CSS3** | Responsive design, animations, color-coding |
| **JavaScript (ES6+)** | Async API calls, DOM manipulation, drag-and-drop |
| **Fetch API** | RESTful communication |

### **AI & Data**
| Service | Purpose |
|---------|---------|
| **Google Gemini 2.5 Flash** | LLM-powered clinical recommendations |
| **CPIC Database** | Pharmacogenomic guidelines (300+ drugs) |
| **Custom Phenotype Engine** | 650+ diplotype-to-phenotype mappings |

### **Development Tools**
- **Git** - Version control
- **VS Code** - IDE
- **PowerShell** - Scripting & automation
- **curl** - API testing

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository
```bash
git clone https://github.com/Shr3y4sm/PharmaGuard_NullPoint.git
cd PharmaGuard_NullPoint
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy the example environment file and configure your API key:
```bash
# Copy template
cp .env.example .env

# Edit .env and add your Google Gemini API key
# GOOGLE_API_KEY=your_gemini_api_key_here
```

Or create `.env` manually:
```bash
# .env
GOOGLE_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
```

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## � Environment Variables

Copy `.env.example` to `.env` and configure these variables:

### Required
| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | `AIzaSyD1234...` |

### Optional
| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode (development/production) | `development` |
| `HOST` | Server host address | `0.0.0.0` |
| `PORT` | Server port number | `5000` |
| `MAX_FILE_SIZE_MB` | Maximum upload size | `5` |
| `SECRET_KEY` | Flask session secret (auto-generated) | Random |

### Setup
```bash
# Copy template
cp .env.example .env

# Edit with your editor
nano .env
# or
vim .env
```

### Example .env file
```env
# Google Gemini API Key (get from https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY=AIzaSyD1234567890abcdefghij

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1

# Server Configuration
HOST=0.0.0.0
PORT=5000

# File Upload Configuration
MAX_FILE_SIZE_MB=5

# Security (change for production)
SECRET_KEY=dev_secret_key_change_in_production
```

---

## �📖 Usage

### Web Interface Usage

1. **Open the application** in your browser: `http://localhost:5000`

2. **Upload VCF File:**
   - Click the upload area OR drag-and-drop a `.vcf` file
   - File must be VCF v4.2 format with INFO tags (GENE, STAR, RS)
   - Maximum file size: 5MB
   - **Use sample files** from `data/` directory for testing (see [Sample VCF Files](#sample-vcf-files))

3. **Enter Drug Name(s):**
   - Type drug name in the text field (e.g., `CODEINE`)
   - For multiple drugs, use comma separation: `CODEINE, WARFARIN`
   - OR select from the suggested drugs dropdown

4. **Analyze:**
   - Click "Analyse Drug Risk" button
   - Wait for processing (typically 3-5 seconds)

5. **View Results:**
   - **Risk Badge:** Color-coded safety indicator
   - **Confidence Score:** Model certainty percentage
   - **Tab 1 - Pharmacogenic Profile:** Gene, diplotype, phenotype, detected variants
   - **Tab 2 - Clinical Recommendation:** Dosage adjustments, monitoring requirements
   - **Tab 3 - Clinical Explanation:** Mechanism, evidence, interaction notes
   - **JSON Output:** Complete structured response (downloadable)

### Sample VCF Files

Six test VCF files are provided in the `data/` directory:

| File | Patient Type | Risk Level | Best For Testing |
|------|-------------|------------|------------------|
| `sample_normal_metabolizer.vcf` | Normal metabolizer | Low | Standard dosing scenarios |
| `sample_poor_metabolizer.vcf` | Poor metabolizer | **HIGH** | High-risk warnings, dosage reduction |
| `sample_ultra_rapid_metabolizer.vcf` | Ultra-rapid | Moderate | Enhanced metabolism cases |
| `sample_multi_drug.vcf` | Complex case | Mixed | Multi-drug analysis |
| `sample_wildtype.vcf` | Wild-type alleles | Minimal | Baseline genotype |
| `test_patient.vcf` | General test | Moderate | Development testing |

**📖 See [data/README.md](data/README.md) for detailed descriptions and testing scenarios.**

#### Quick Test Example
```bash
# Test with poor metabolizer profile
# Upload: data/sample_poor_metabolizer.vcf
# Drugs: CODEINE
# Expected: HIGH RISK warning with dosage reduction recommendation
```

### Expected Output
```json
{
  "patient_id": "PATIENT_XXXXXXXX",
  "drug": "CODEINE",
  "timestamp": "2026-02-19T13:23:44.710999Z",
  "risk_assessment": {
    "risk_label": "Safe",
    "confidence_score": 0.95,
    "severity": "none"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "CYP2D6",
    "diplotype": "*1/*1",
    "phenotype": "NM",
    "detected_variants": [
      {"rsid": "rs1065852", "star": "*1"},
      {"rsid": "rs28371725", "star": "*1"}
    ]
  },
  "clinical_recommendation": {
    "dosage_adjustment": "Administer codeine at standard doses...",
    "monitoring": "Monitor for therapeutic efficacy and adverse effects...",
    "alternative_drugs": [],
    "urgency": "routine"
  },
  "llm_generated_explanation": {
    "summary": "The patient is a CYP2D6 Normal Metabolizer...",
    "mechanism": "Codeine is a prodrug that requires O-demethylation...",
    "interaction_notes": ["While CYP2D6 metabolism is normal..."],
    "evidence_basis": "This recommendation is based on CPIC Level A..."
  }
}
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Get Web Interface
```http
GET /
```
**Description:** Returns the main HTML interface

**Response:** HTML page

---

#### 2. Analyze (HTML Response)
```http
POST /analyze
```

**Description:** Process VCF + drugs, return HTML with embedded results

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:**
  - `vcf_file` (file): VCF file upload
  - `drugs` (string): Comma-separated drug names

**Response:** HTML page with results

---

#### 3. API Analysis (JSON Response) ⭐
```http
POST /api/analysis
```

**Description:** Process VCF + drugs, return structured JSON

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:**
  ```
  vcf_file: [Binary VCF File]
  drugs: "CODEINE, WARFARIN"
  ```

**Success Response (200):**
```json
{
  "success": true,
  "total_results": 2,
  "responses": [
    {
      "patient_id": "PATIENT_ABC123",
      "drug": "CODEINE",
      "timestamp": "2026-02-19T13:23:44.710999Z",
      "risk_assessment": {
        "risk_label": "Safe",
        "confidence_score": 0.95,
        "severity": "none"
      },
      "pharmacogenomic_profile": { ... },
      "clinical_recommendation": { ... },
      "llm_generated_explanation": { ... },
      "quality_metrics": {
        "vcf_parsing_success": true,
        "variant_count": 2,
        "data_completeness": "high"
      }
    }
  ],
  "debug": {
    "vcf_genes_found": ["CYP2D6", "CYP2C19"],
    "cpic_drugs_loaded": ["CODEINE", "WARFARIN", "CLOPIDOGREL", "SIMVASTATIN", "FLUOROURACIL"],
    "drugs_requested": ["CODEINE", "WARFARIN"]
  }
}
```

**Error Response (400):**
```json
{
  "error": "VCF parsing failed",
  "details": "Invalid VCF format"
}
```

**Error Response (413):**
```json
{
  "error": "File too large",
  "details": "The uploaded file exceeds the 5MB size limit."
}
```

**Error Response (500):**
```json
{
  "error": "Analysis error",
  "details": "Internal server error message"
}
```

### Response Schema

#### Risk Assessment Object
```typescript
{
  "risk_label": "Safe" | "Adjust Dosage" | "Toxic" | "Review Required",
  "confidence_score": 0.0 - 0.99,  // Model confidence
  "severity": "none" | "low" | "moderate" | "critical"
}
```

#### Pharmacogenomic Profile Object
```typescript
{
  "primary_gene": string,           // e.g., "CYP2D6"
  "diplotype": string,               // e.g., "*1/*1"
  "phenotype": "PM" | "IM" | "NM" | "RM" | "URM" | "Unknown",
  "detected_variants": [
    {
      "rsid": string,                // e.g., "rs1065852"
      "star": string                 // e.g., "*1"
    }
  ]
}
```

---
## 📝 cURL Examples

### Example 1: Analyze Single Drug
```bash
curl -X POST http://localhost:5000/api/analysis \
  -F "vcf_file=@data/sample_poor_metabolizer.vcf" \
  -F "drugs=CODEINE"
```

### Example 2: Analyze Multiple Drugs
```bash
curl -X POST http://localhost:5000/api/analysis \
  -F "vcf_file=@data/sample_multi_drug.vcf" \
  -F "drugs=CODEINE, WARFARIN, CLOPIDOGREL"
```

### Example 3: Save Response to File
```bash
curl -X POST http://localhost:5000/api/analysis \
  -F "vcf_file=@data/sample_normal_metabolizer.vcf" \
  -F "drugs=WARFARIN" \
  -o response.json

cat response.json | jq '.'  # Pretty print JSON
```

### Example 4: With Pretty-Printed Output
```bash
curl -X POST http://localhost:5000/api/analysis \
  -F "vcf_file=@data/test_patient.vcf" \
  -F "drugs=CODEINE" \
  | jq '.'
```

### Example 5: Extract Specific Fields
```bash
curl -X POST http://localhost:5000/api/analysis \
  -F "vcf_file=@data/sample_poor_metabolizer.vcf" \
  -F "drugs=SIMVASTATIN" \
  | jq '.responses[0].risk_assessment'
```

### Example 6: Check Server Health
```bash
curl -X GET http://localhost:5000/
```

---

## ⚙️ Performance & Limits

### File Constraints
- **Maximum VCF File Size:** 5 MB
- **Supported Format:** VCF v4.2 only
- **Required INFO Fields:** GENE, STAR, RS
- **Processing Time:** 3-5 seconds per drug analysis

### Supported Pharmacogenes
```
CYP2D6   - Codeine, tramadol, metoprolol metabolism
CYP2C19  - Clopidogrel, omeprazole metabolism
CYP2C9   - Warfarin, NSAIDs metabolism
SLCO1B1  - Simvastatin transport
TPMT     - Immunosuppressant metabolism
DPYD     - Fluorouracil metabolism
```

### Supported Drugs (5 drugs, CPIC Level A)
```
CODEINE         - Opioid analgesic
WARFARIN        - Anticoagulant
CLOPIDOGREL     - Antiplatelet agent
SIMVASTATIN     - Statin (HMG-CoA reductase inhibitor)
FLUOROURACIL    - Chemotherapy agent
```

### Phenotype Classifications
```
PM  - Poor Metabolizer        (increased drug levels)
IM  - Intermediate Metabolizer (moderate metabolism)
NM  - Normal Metabolizer       (standard metabolism)
RM  - Rapid Metabolizer        (decreased drug levels)
URM - Ultra-Rapid Metabolizer  (very low drug levels)
```

---

## 🔒 Security Considerations

### API Key Management
- ✅ **Never commit** `.env` file to version control
- ✅ **Use `.env.example`** as template for configuration
- ✅ **Regenerate API keys** if compromised
- ✅ **Rotate keys regularly** in production

### File Upload Security
- ✅ **VCF validation** before processing
- ✅ **File size limits** (5MB max)
- ✅ **Type checking** (.vcf extension only)
- ✅ **Automatic cleanup** of uploaded files

### Data Privacy
- ⚠️ **No data persistence:** Files are deleted after analysis
- ⚠️ **LLM requests:** Patient data sent to Google Gemini API
- ⚠️ **HIPAA compliance:** Not certified; use with caution for real PHI
- ⚠️ **Audit logging:** Enable in production environment

### Production Security Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use HTTPS/SSL certificates
- [ ] Set strong SECRET_KEY
- [ ] Configure CORS properly
- [ ] Enable request logging
- [ ] Set up rate limiting
- [ ] Use environment-specific configs
- [ ] Enable comprehensive error logging
- [ ] Implement authentication for API endpoints
- [ ] Use secure headers middleware

---

## 🆘 Troubleshooting & FAQ

### Q: "ModuleNotFoundError: No module named 'flask'"
**A:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Q: "GOOGLE_API_KEY not found"
**A:** Create `.env` file from template:
```bash
cp .env.example .env
# Then edit and add your API key
```

### Q: Application starts but port already in use
**A:** Use different port or kill existing process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Or use different port
flask run --port 5001
```

### Q: "File too large" error (413)
**A:** VCF file exceeds 5MB limit. Use smaller file or compress:
```bash
# Check file size
ls -lh data/your_file.vcf

# Use provided sample files instead
```

### Q: API returns "error": "VCF parsing failed"
**A:** Check VCF format requirements:
- Must be VCF v4.2 format
- Must have INFO fields: GENE, STAR, RS
- Check for invalid characters
- Use sample files to verify format

### Q: "Cannot import module 'cpic_engine'"
**A:** Ensure you're in project root directory:
```bash
cd PharmaGuard_NullPoint
python app.py
```

### Q: Analysis returns "risk_label": "Review Required"
**A:** This is normal! Means insufficient variant data. Possible causes:
- Missing genes in VCF file
- Non-standard diplotype combinations
- Confidence score below threshold

### Q: CPIC data loading errors
**A:** Verify file exists:
```bash
ls -la data/cpic_gene-drug_pairs.xlsx
```

### Q: Browser shows "Cannot GET /"
**A:** Application not running. Start server:
```bash
python app.py
```

### Q: Drag-and-drop not working
**A:** Try these steps:
1. Refresh browser (Ctrl+Shift+R hard refresh)
2. Check browser console for JavaScript errors
3. Try uploading file via file selector button
4. Use supported browser (Chrome, Firefox, Safari, Edge)

### Q: LLM explanation is empty or generic
**A:** These issues may cause this:
- API rate limit exceeded
- Network connectivity issues
- Invalid API key
- Invalid drug-gene combination

### Q: How to test without internet?
**A:** LLM features won't work offline, but VCF parsing and risk assessment will:
```bash
# Disable LLM service
# Comment out LLM_PROVIDER in app.py
```

---
## � Deployment

PharmaGuard can be deployed to multiple cloud platforms. See **[DEPLOYMENT.md](DEPLOYMENT.md)** for comprehensive deployment instructions.

### Quick Deploy Options

| Platform | Deployment Method | Documentation |
|----------|------------------|---------------|
| **Heroku** | `git push heroku main` | [Heroku Guide](DEPLOYMENT.md#heroku-deployment) |
| **AWS Elastic Beanstalk** | `eb deploy` | [AWS Guide](DEPLOYMENT.md#aws-elastic-beanstalk) |
| **Azure App Service** | `az webapp up` | [Azure Guide](DEPLOYMENT.md#azure-app-service) |
| **Google Cloud Platform** | `gcloud app deploy` | [GCP Guide](DEPLOYMENT.md#google-cloud-platform) |
| **Docker** | `docker-compose up` | [Docker Guide](DEPLOYMENT.md#docker-deployment) |

### Pre-Deployment Checklist

- [ ] Google Gemini API key configured
- [ ] Environment variables set (`.env` or platform-specific)
- [ ] Application tested locally
- [ ] HTTPS/SSL enabled for production
- [ ] Maximum file upload size configured (5MB default)

**📖 Read [DEPLOYMENT.md](DEPLOYMENT.md) for detailed platform-specific instructions, best practices, and troubleshooting.**

---

## �📂 Project Structure

```
PharmaGuard_NullPoint/
│
├── app.py                      # Flask application (routes, endpoints)
├── cpic_engine.py              # CPIC data filtering & initialization
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys) - DO NOT COMMIT
├── .env.example                # Environment template (COMMIT THIS)
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── DEPLOYMENT.md               # Deployment guide for cloud platforms
│
├── data/
│   ├── cpic_gene-drug_pairs.xlsx           # CPIC database (300+ drugs)
│   ├── README.md                           # Sample VCF documentation
│   ├── test_patient.vcf                    # Original test file
│   ├── sample_normal_metabolizer.vcf       # Normal metabolizer test
│   ├── sample_poor_metabolizer.vcf         # Poor metabolizer (HIGH RISK)
│   ├── sample_ultra_rapid_metabolizer.vcf  # Ultra-rapid metabolizer
│   ├── sample_multi_drug.vcf               # Complex multi-drug case
│   └── sample_wildtype.vcf                 # Wild-type baseline
│
├── services/
│   ├── cpic_loader.py          # Excel data loader
│   ├── vcf_parser.py           # VCF v4.2 parser
│   ├── drug_gene_matcher.py   # Drug-gene validation
│   ├── phenotype_engine.py    # Diplotype-to-phenotype mapping
│   ├── response_builder.py    # JSON response generation
│   └── llm_service.py          # Gemini AI integration
│
├── static/
│   ├── css/
│   │   └── styles.css          # UI styling (responsive, color-coded)
│   └── js/
│       └── script.js           # Frontend logic (drag-drop, API calls)
│
└── templates/
    └── index.html              # Main UI template
```

### Key Modules

- **`app.py`**: Flask server with routes and error handling
- **`cpic_engine.py`**: Filters CPIC data to 5 supported drugs
- **`services/vcf_parser.py`**: Parses VCF files, extracts INFO fields
- **`services/drug_gene_matcher.py`**: Validates drug-gene pairs
- **`services/phenotype_engine.py`**: Maps 650+ diplotypes to phenotypes
- **`services/response_builder.py`**: Generates structured JSON responses
- **`services/llm_service.py`**: Google Gemini API client with JSON extraction
- **`static/js/script.js`**: Drag-and-drop, form validation, dynamic UI updates
- **`static/css/styles.css`**: Color-coded badges, responsive design

---

## 👥 Team

### NullPoint Team

| **Shreyas M** | 
| **Harshavardhan K** |
| **Ramanuja U K** |
| **Jagannath Nayak** |

### Contributions

- **Full Stack Development:** UI/UX design, Flask backend, API integration
- **AI Integration:** Google Gemini LLM implementation, prompt engineering
- **Data Engineering:** CPIC database processing, phenotype mapping system
- **Quality Assurance:** Testing, error handling, validation logic

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/AmazingFeature`
3. **Commit your changes:** `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch:** `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Check code style
flake8 .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments


- **RIFT 2026 HACKATHON, PW Institute of Innovation**
- **CPIC (Clinical Pharmacogenetics Implementation Consortium)** for pharmacogenomic guidelines
- **Google Gemini AI** for LLM-powered clinical recommendations
- **Open-source community** for libraries and tools (Flask, pandas, etc.)

<div align="center">

</div>
