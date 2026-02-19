# 🔧 PharmaGuard Backend Architecture Documentation

**Version:** 1.0  
**Last Updated:** February 20, 2026  
**Framework:** Flask 3.0.0  
**Language:** Python 3.8+

---

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [API Endpoints](#api-endpoints)
3. [Request/Response Formats](#requestresponse-formats)
4. [Backend Services](#backend-services)
5. [Data Flow](#data-flow)
6. [Supported Features](#supported-features)
7. [Error Handling](#error-handling)
8. [Configuration](#configuration)

---

## 🏗️ System Overview

### Architecture Type
**Monolithic Flask Application** with modular service layer

### Technology Stack
- **Web Framework:** Flask 3.0.0
- **LLM Integration:** Google Gemini 2.5 Flash (optional)
- **Data Processing:** pandas, openpyxl
- **File Upload:** multipart/form-data
- **Response Format:** JSON (field order preserved)

### Core Capabilities
✅ VCF v4.2 file parsing  
✅ 6 pharmacogenomic genes analysis  
✅ 6 supported drugs (expandable)  
✅ CPIC guideline integration  
✅ AI-powered clinical recommendations  
✅ Risk assessment with phenotype classification  

---

## 🌐 API Endpoints

### 1️⃣ **GET /** 
**Purpose:** Serve main web application  
**Response:** HTML page (index.html)  
**Use Case:** Primary user interface

```http
GET http://localhost:5000/
```

---

### 2️⃣ **POST /analyze**
**Purpose:** Form-based analysis with HTML response  
**Content-Type:** `multipart/form-data`  
**Response:** HTML page with results embedded  

**Request Parameters:**
```
vcf_file: file (required) - VCF file (.vcf, max 5MB)
drugs: string (required) - Comma-separated drug names (e.g., "CODEINE, WARFARIN")
```

**Response:** Rendered HTML template with results

**Use Case:** Traditional form submission (not recommended for new UI)

---

### 3️⃣ **POST /api/analysis** ⭐ **PRIMARY ENDPOINT**
**Purpose:** JSON API for programmatic access  
**Content-Type:** `multipart/form-data`  
**Response:** JSON (structured, field-order preserved)

**Request Parameters:**
```
vcf_file: file (required) - VCF file (.vcf, max 5MB)
drugs: string (required) - Comma-separated drug names
```

**Success Response (200):**
```json
{
  "total_analyses": 1,
  "analyses": [
    {
      "patient_id": "PATIENT_XXXXXXXX",
      "drug": "CODEINE",
      "timestamp": "2026-02-19T20:17:37.011428Z",
      "risk_assessment": {
        "risk_label": "Safe|Adjust Dosage|Toxic|Ineffective|Unknown",
        "confidence_score": 0.95,
        "severity": "none|low|moderate|high|critical"
      },
      "pharmacogenomic_profile": {
        "primary_gene": "CYP2D6",
        "diplotype": "*1/*1",
        "phenotype": "PM|IM|NM|RM|URM|Unknown",
        "detected_variants": [
          {"rsid": "rs1065852", "star": "*1"},
          {"rsid": "rs28371725", "star": "*1"}
        ]
      },
      "clinical_recommendation": {
        "dosage_adjustment": "Consult healthcare provider...",
        "monitoring": "Standard monitoring recommended",
        "alternative_drugs": [],
        "urgency": "routine|important|urgent"
      },
      "llm_generated_explanation": {
        "summary": "Patient-friendly explanation...",
        "mechanism": "How the medication works...",
        "interaction_notes": ["Note 1", "Note 2"],
        "evidence_basis": "Clinical guideline source"
      },
      "quality_metrics": {
        "vcf_parsing_success": true,
        "variant_count": 2,
        "data_completeness": "high|low"
      },
      "guideline_url": "https://cpicpgx.org/guidelines/..."
    }
  ]
}
```

**Error Response (400):**
```json
{
  "error": "Error type",
  "details": "Detailed error message"
}
```

**Error Response (413):**
```json
{
  "error": "File too large",
  "details": "File exceeds 5MB limit"
}
```

---

## 🔄 Request/Response Formats

### 📤 Frontend Request Format

**Using JavaScript Fetch:**
```javascript
const formData = new FormData();
formData.append('vcf_file', vcfFileObject);
formData.append('drugs', 'CODEINE, WARFARIN, SIMVASTATIN');

const response = await fetch('/api/analysis', {
  method: 'POST',
  body: formData
});

const result = await response.json();
```

**Using curl:**
```bash
curl -X POST \
  -F "vcf_file=@patient.vcf" \
  -F "drugs=CODEINE,WARFARIN" \
  http://localhost:5000/api/analysis
```

### 📥 Drug Input Format

**Accepted Formats:**
- Single drug: `"CODEINE"`
- Multiple drugs (comma-separated): `"CODEINE, WARFARIN, SIMVASTATIN"`
- Case-insensitive (backend converts to uppercase)
- Spaces are trimmed automatically

**Supported Drugs:**
1. CODEINE (CYP2D6)
2. WARFARIN (CYP2C9, VKORC1)
3. CLOPIDOGREL (CYP2C19)
4. SIMVASTATIN (SLCO1B1)
5. AZATHIOPRINE (TPMT, NUDT15)
6. FLUOROURACIL (DPYD)

---

## 🛠️ Backend Services

### Service Architecture
```
app.py (Flask routes)
    ├── services/vcf_parser.py          → VCF file parsing
    ├── services/drug_gene_matcher.py   → Drug-to-gene mapping
    ├── services/phenotype_engine.py    → Phenotype classification
    ├── services/cpic_loader.py         → CPIC data loading
    ├── services/llm_service.py         → Gemini AI integration
    └── services/response_builder.py    → JSON response construction
```

### 1. **vcf_parser.py**
**Responsibility:** Parse VCF v4.2 files and extract genetic variants

**Input:**
- File object (from Flask request.files)

**Output:**
```python
{
    "vcf_parsing_success": True,
    "variants": {
        "CYP2D6": [{"rsid": "rs1065852", "star": "*1"}],
        "CYP2C19": [...],
        # ... other genes
    }
}
```

**Features:**
- Validates VCF format (v4.2)
- Extracts rs IDs and star alleles
- Filters for 6 pharmacogenomic genes
- Handles empty/malformed files

**Supported Genes:**
- CYP2D6, CYP2C19, CYP2C9, SLCO1B1, TPMT, DPYD

---

### 2. **drug_gene_matcher.py**
**Responsibility:** Match drugs to relevant genes using CPIC data

**Input:**
- Drug name (string)
- VCF parsed data
- CPIC engine (loaded data)

**Output:**
```python
{
    "valid": True,
    "drug": "CODEINE",
    "gene": "CYP2D6",
    "gene_found_in_vcf": True,
    "variant_count": 2,
    "cpic_level": "A",
    "guideline_url": "https://cpicpgx.org/..."
}
```

---

### 3. **phenotype_engine.py**
**Responsibility:** Determine metabolizer phenotype from genotype

**Input:**
- Gene name
- List of variants

**Output:**
```python
{
    "phenotype": "NM",  # PM, IM, NM, RM, URM, Unknown
    "diplotype": "*1/*1"
}
```

**Phenotype Classifications:**
- **PM:** Poor Metabolizer
- **IM:** Intermediate Metabolizer
- **NM:** Normal Metabolizer
- **RM:** Rapid Metabolizer
- **URM:** Ultra-Rapid Metabolizer
- **Unknown:** Cannot determine

---

### 4. **cpic_loader.py**
**Responsibility:** Load CPIC guideline data from Excel

**Data Source:** `data/cpic_gene-drug_pairs.xlsx`

**Loaded Data Structure:**
```python
{
    "CODEINE": {
        "gene": "CYP2D6",
        "cpic_level": "A",
        "guideline_url": "https://cpicpgx.org/guidelines/..."
    },
    # ... other drugs
}
```

---

### 5. **llm_service.py**
**Responsibility:** Generate patient-friendly clinical recommendations using Google Gemini

**Features:**
- Exponential backoff retry logic (3 attempts)
- Rate limit handling (429 errors)
- Patient-friendly language
- Structured JSON output
- Fallback responses for unsupported drugs

**API Configuration:**
- Model: `gemini-2.0-flash-exp`
- Temperature: 0.3 (deterministic)
- Max tokens: 1024
- API Key: from `GOOGLE_API_KEY` environment variable

**Output:**
```python
{
    "clinical_recommendation": {
        "dosage_adjustment": "...",
        "monitoring": "...",
        "alternative_drugs": [],
        "urgency": "routine"
    },
    "llm_generated_explanation": {
        "summary": "...",
        "mechanism": "...",
        "interaction_notes": [],
        "evidence_basis": "..."
    }
}
```

---

### 6. **response_builder.py**
**Responsibility:** Construct final JSON response with exact field ordering

**Key Features:**
- Preserves field order (critical for schema compliance)
- Generates patient IDs (PATIENT_XXXXXXXX)
- ISO8601 timestamps
- Risk assessment calculation
- Quality metrics

**Risk Assessment Logic:**
| Phenotype | Risk Label | Severity | Confidence |
|-----------|-----------|----------|------------|
| PM | Toxic | Critical | 0.95 |
| IM | Adjust Dosage | Moderate | 0.85 |
| NM | Safe | None | 0.90 |
| RM | Adjust Dosage | Low | 0.80 |
| URM | Ineffective | High | 0.85 |
| Unknown | Unknown | Low | 0.60 |

---

## 🔄 Data Flow

### End-to-End Analysis Flow

```
┌─────────────────┐
│   User Upload   │
│  VCF + Drugs    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Endpoint │
│  /api/analysis  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   VCF Parser    │◄───── Validates & extracts variants
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Drug Matcher    │◄───── Maps drug → gene
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Phenotype Engine│◄───── Classifies metabolizer type
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Service    │◄───── Generates recommendations (optional)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Response Builder │◄───── Constructs final JSON
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Response  │
│   to Frontend   │
└─────────────────┘
```

### Processing Steps Per Drug:

1. **Upload & Validation** (vcf_parser)
   - Check file size (< 5MB)
   - Validate VCF format
   - Extract variants for 6 genes

2. **Drug-Gene Matching** (drug_gene_matcher)
   - Lookup drug in CPIC database
   - Get associated gene(s)
   - Check if gene variants exist in VCF
   - Retrieve guideline URL

3. **Phenotype Classification** (phenotype_engine)
   - Analyze variant combinations
   - Determine diplotype (*X/*Y)
   - Classify phenotype (PM/IM/NM/RM/URM)

4. **Risk Assessment** (response_builder)
   - Calculate risk label based on phenotype
   - Assign severity level
   - Compute confidence score

5. **AI Enhancement** (llm_service) - Optional
   - Generate patient-friendly explanation
   - Provide dosage recommendations
   - Suggest monitoring protocols
   - List alternative medications

6. **JSON Construction** (response_builder)
   - Format in exact schema order
   - Add timestamps & patient ID
   - Include quality metrics
   - Append guideline citation

---

## ✨ Supported Features

### ✅ Currently Implemented

- ✅ VCF v4.2 file parsing
- ✅ 6 pharmacogenomic genes (CYP2D6, CYP2C19, CYP2C9, SLCO1B1, TPMT, DPYD)
- ✅ 6 supported drugs (CODEINE, WARFARIN, CLOPIDOGREL, SIMVASTATIN, AZATHIOPRINE, FLUOROURACIL)
- ✅ Multi-drug analysis (comma-separated)
- ✅ CPIC Level A/B/C evidence support
- ✅ Phenotype classification (PM/IM/NM/RM/URM)
- ✅ Risk assessment (Safe/Adjust/Toxic/Ineffective/Unknown)
- ✅ Clinical guideline citations with URLs
- ✅ Google Gemini AI integration (optional)
- ✅ Rate limiting with exponential backoff
- ✅ Patient-friendly explanations
- ✅ File size validation (5MB max)
- ✅ Empty/malformed VCF rejection
- ✅ JSON schema 100% compliance
- ✅ Field order preservation (Flask 3.0)

### ⚙️ Configuration

**Environment Variables:**
```bash
GOOGLE_API_KEY=your_gemini_api_key_here  # Optional
```

**File Limits:**
```python
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
```

**Supported VCF Format:**
- VCF v4.2 specification
- Must contain variant annotations
- ##fileformat=VCFv4.2 header required

---

## ⚠️ Error Handling

### Error Types & Responses

| Error Type | HTTP Code | Response |
|------------|-----------|----------|
| No VCF file | 400 | `{"error": "No VCF file provided"}` |
| No drugs | 400 | `{"error": "No drugs provided"}` |
| Empty VCF | 400 | `{"error": "VCF parsing failed", "details": "VCF file is empty"}` |
| Invalid VCF | 400 | `{"error": "VCF parsing failed", "details": "Invalid VCF format"}` |
| File too large | 413 | `{"error": "File too large", "details": "..."}` |
| Server error | 500 | `{"error": "Analysis error", "details": "..."}` |

### LLM Fallback Behavior

**When Gemini API fails:**
- Returns default recommendations
- Graceful degradation (no crash)
- Partial response with placeholders:
  ```json
  "clinical_recommendation": {
    "dosage_adjustment": "Pending LLM analysis",
    "monitoring": "Standard monitoring recommended",
    ...
  }
  ```

**When rate limited (429 errors):**
- Automatic retry with exponential backoff
- Delays: 1s → 2s → 4s
- After 3 attempts: falls back to default response

---

## 📊 Response Schema (Exact Field Order)

**CRITICAL:** Field order is preserved and must not change!

```json
{
  "total_analyses": 1,
  "analyses": [
    {
      "patient_id": "...",              // 1st
      "drug": "...",                    // 2nd
      "timestamp": "...",               // 3rd
      "risk_assessment": {...},         // 4th
      "pharmacogenomic_profile": {...}, // 5th
      "clinical_recommendation": {...}, // 6th
      "llm_generated_explanation": {...}, // 7th
      "quality_metrics": {...},         // 8th
      "guideline_url": "..."            // 9th (optional)
    }
  ]
}
```

**Flask Configuration:**
```python
app.json.sort_keys = False  # REQUIRED for Flask 3.0+
```

---

## 🔌 Frontend Integration Guide

### What the Frontend Needs to Send

```javascript
// 1. Collect VCF file from input
const vcfFile = document.getElementById('vcf-upload').files[0];

// 2. Collect drug selections (comma-separated)
const drugs = "CODEINE, WARFARIN";  // Or from multi-select

// 3. Create FormData
const formData = new FormData();
formData.append('vcf_file', vcfFile);
formData.append('drugs', drugs);

// 4. Send POST request
const response = await fetch('/api/analysis', {
  method: 'POST',
  body: formData
});

// 5. Parse JSON response
const data = await response.json();
```

### What the Frontend Receives

**On Success:**
```javascript
{
  total_analyses: 1,
  analyses: [{
    patient_id: "PATIENT_ABC123",
    drug: "CODEINE",
    risk_assessment: {
      risk_label: "Safe",  // Use for badge color
      confidence_score: 0.95,  // Display as 95%
      severity: "none"  // none|low|moderate|high|critical
    },
    pharmacogenomic_profile: {
      primary_gene: "CYP2D6",  // Display in profile
      phenotype: "NM",  // Normal Metabolizer
      ...
    },
    clinical_recommendation: {
      dosage_adjustment: "...",  // Tab 1 content
      ...
    },
    llm_generated_explanation: {
      summary: "...",  // Tab 2 content
      ...
    }
  }]
}
```

**On Error:**
```javascript
{
  error: "Error type",
  details: "Detailed message"
}
```

### UI Display Mapping

| Backend Field | UI Component | Example |
|--------------|--------------|---------|
| `risk_assessment.risk_label` | Risk badge | "SAFE" (green) |
| `risk_assessment.severity` | Severity indicator | "None" |
| `risk_assessment.confidence_score` | Progress bar/gauge | 95% |
| `pharmacogenomic_profile.*` | Tab 0: Profile | Gene, phenotype, variants |
| `clinical_recommendation.*` | Tab 1: Recommendations | Dosage, monitoring |
| `llm_generated_explanation.*` | Tab 2: Explanation | Summary, mechanism |
| `guideline_url` | Citation link | Blue hyperlink |

---

## 🚀 Quick Start Testing

### Test with curl:
```bash
curl -X POST \
  -F "vcf_file=@data/test_patient.vcf" \
  -F "drugs=CODEINE" \
  http://localhost:5000/api/analysis
```

### Test with Python:
```python
import requests

files = {'vcf_file': open('data/test_patient.vcf', 'rb')}
data = {'drugs': 'CODEINE, WARFARIN'}
response = requests.post('http://localhost:5000/api/analysis', 
                        files=files, data=data)
print(response.json())
```

---

## 📝 Notes for Frontend Developers

### ✅ DO:
- Use `/api/analysis` endpoint (not `/analyze`)
- Send drugs as comma-separated string
- Check `response.ok` before parsing JSON
- Display errors from `error` and `details` fields
- Show loading states during uploads
- Validate file size client-side (< 5MB)
- Accept only .vcf files

### ❌ DON'T:
- Don't modify JSON field order in responses
- Don't assume LLM data is always present (check for defaults)
- Don't send empty drug strings
- Don't rely on `/analyze` endpoint (HTML response)
- Don't parse JSON fields in different order

---

## 🎯 Summary for New UI Development

**What the backend provides:**
1. ✅ Robust VCF parsing with validation
2. ✅ Drug-gene-phenotype analysis
3. ✅ Risk assessment with confidence scores
4. ✅ AI-powered recommendations (optional)
5. ✅ Clinical guideline citations
6. ✅ Structured JSON responses

**What the frontend needs to handle:**
1. File upload with drag-and-drop
2. Drug selection (multi-select or tags)
3. Loading states during analysis
4. Error message display
5. Results visualization (tabs, badges, gauges)
6. JSON display/copy/download
7. Responsive design

**API Contract:**
- **Endpoint:** `POST /api/analysis`
- **Input:** FormData with `vcf_file` and `drugs`
- **Output:** JSON with `total_analyses` and `analyses` array
- **Errors:** JSON with `error` and `details` fields

**Ready to integrate!** The backend is stable, tested, and production-ready. 🚀
