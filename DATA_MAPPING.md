# Backend → Frontend Data Mapping

## Quick Reference: JSON to UI Elements

### Risk Assessment Section

| Backend Field | UI Element | Location |
|--------------|-----------|----------|
| `risk_assessment.risk_label` | Large risk status text | Risk Profile Card (top) |
| `risk_assessment.severity` | Severity score number | Green/Yellow/Red badge |
| `risk_assessment.confidence_score` | Gauge chart (0-1 scale) | Right side of card |

**Example:**
```json
{
  "risk_assessment": {
    "risk_label": "SAFE",           → "SAFE" (green, 6xl font)
    "severity": 1.2,                → "1.2 (LOW)" (green badge)
    "confidence_score": 0.95        → Gauge filled 95%
  }
}
```

### Pharmacogenomic Profile

| Backend Field | UI Element | Location |
|--------------|-----------|----------|
| `pharmacogenomic_profile.gene_name` | Detected Variant (part 1) | Below gauge |
| `pharmacogenomic_profile.star_alleles` | Detected Variant (part 2) | Below gauge |
| `pharmacogenomic_profile.phenotype` | Predicted Phenotype | Below variant |
| `pharmacogenomic_profile.drug` | Metadata text | Profile tab |

**Example:**
```json
{
  "pharmacogenomic_profile": {
    "gene_name": "CYP2D6",          → "Detected Variant: CYP2D6: *1/*2"
    "star_alleles": "*1/*2",        ↗
    "phenotype": "NORMAL METABOLIZER", → "Predicted Phenotype: NORMAL METABOLIZER"
    "drug": "CODEINE"               → "Metadata: CODEINE - CYP2D6 (*1/*2)"
  }
}
```

### Clinical Information

| Backend Field | UI Element | Location |
|--------------|-----------|----------|
| `clinical_recommendation` | Paragraph text | Recommendation tab (Tab 1) |
| `llm_generated_explanation` | Paragraph text | Explanation tab (Tab 2) |
| `guideline_url` | Hyperlink | Profile tab (Citation) |

**Example:**
```json
{
  "clinical_recommendation": "Standard dosing...",  → Tab 1 content
  "llm_generated_explanation": "This patient...", → Tab 2 content
  "guideline_url": "https://cpicpgx.org/..."     → Blue clickable link in Tab 0
}
```

## Color Coding Rules

### Risk Label → Color Mapping

```javascript
// SAFE or NORMAL
risk_label.includes('SAFE') || risk_label.includes('NORMAL')
→ Green (#22c55e)

// MODERATE or CAUTION
risk_label.includes('MODERATE') || risk_label.includes('CAUTION')
→ Yellow (#eab308)

// HIGH or CRITICAL
risk_label.includes('HIGH') || risk_label.includes('CRITICAL')
→ Red (#ef4444)

// Unknown
default
→ Gray (#6b7280)
```

### Severity Score → Badge Text

```javascript
severity < 1  → "NONE"
severity < 3  → "LOW"
severity < 6  → "MODERATE"
severity < 8  → "HIGH"
severity >= 8 → "CRITICAL"
```

### Confidence Score → Gauge

```javascript
confidence_score = 0.0 to 1.0
→ Gauge arc: 0% to 100% filled
→ Stroke color matches risk_label color
```

## Element IDs Reference

### Input Elements
- `#vcf-file-input` - File upload input
- `#dropzone` - Drag-and-drop area
- `#drug-selector-box` - Drug dropdown trigger
- `#selected-drugs` - Container for drug tags
- `#run-analysis-btn` - Submit button

### Display Elements
- `#risk-status` - Large "SAFE" text
- `#severity-score` - Severity number
- `#severity-level` - Severity text "(LOW)"
- `#gauge-arc` - SVG gauge path
- `#detected-variant` - Variant display
- `#predicted-phenotype` - Phenotype display

### Tab Elements
- `#tab-profile` - Profile tab content
- `#tab-recommendation` - Recommendation tab content
- `#tab-explanation` - Explanation tab content
- `#metadata-text` - Drug-gene metadata
- `#guideline-link` - CPIC URL link

### JSON Panel
- `#json-output` - Formatted JSON text
- `#copy-json` - Copy button
- `#download-json` - Download button

## CSS Classes Reference

### Visibility
```css
.hidden          /* display: none !important */
```

### Loading States
```css
.opacity-75      /* Semi-transparent during loading */
.cursor-not-allowed  /* Disabled cursor */
```

### Risk Colors (Tailwind)
```css
.text-green-500  /* Safe status text */
.text-yellow-500 /* Moderate status text */
.text-red-500    /* High/Critical status text */

.bg-green-100    /* Safe badge background */
.text-green-800  /* Safe badge text */

.bg-yellow-100   /* Moderate badge background */
.text-yellow-800 /* Moderate badge text */

.bg-red-100      /* High badge background */
.text-red-800    /* High badge text */
```

### Drug Tags
```css
.bg-blue-100     /* Tag background */
.text-blue-800   /* Tag text */
```

## API Request Format

```javascript
// FormData construction
const formData = new FormData();
formData.append('vcf_file', fileObject);
formData.append('drugs', 'WARFARIN,CODEINE');  // Comma-separated

// Fetch request
fetch('/api/analysis', {
    method: 'POST',
    body: formData
});
```

## Success Response Structure

```json
{
  "status": "success",
  "analyses": [
    {
      "drug": "WARFARIN",
      "gene_analysed": "CYP2C9",
      "pharmacogenomic_profile": {
        "drug": "WARFARIN",
        "gene_name": "CYP2C9",
        "star_alleles": "*1/*2",
        "phenotype": "NORMAL METABOLIZER"
      },
      "clinical_recommendation": "Standard dosing...",
      "llm_generated_explanation": "This patient...",
      "risk_assessment": {
        "risk_label": "SAFE",
        "severity": 1.2,
        "confidence_score": 0.95
      },
      "guideline_url": "https://cpicpgx.org/guidelines/guideline-for-warfarin-and-cyp2c9/"
    }
  ]
}
```

## Error Response Structure

```json
{
  "status": "error",
  "error": "Error message here"
}
```

## Event Handlers Summary

| Event | Element | Handler Function |
|-------|---------|-----------------|
| Click | `#dropzone` | Open file picker |
| Change | `#vcf-file-input` | Handle file selection |
| Drag Over | `#dropzone` | Show drop zone active state |
| Drop | `#dropzone` | Handle file drop |
| Click | `#drug-selector-box` | Toggle dropdown |
| Click | `.drug-option` | Add/remove drug |
| Click | Drug tag X | Remove specific drug |
| Click | `#clear-all` | Clear all drugs |
| Click | `#run-analysis-btn` | Submit analysis |
| Click | `.tab-button` | Switch tabs |
| Click | `#copy-json` | Copy JSON to clipboard |
| Click | `#download-json` | Download JSON file |
| Click | `#refresh-json` | Refresh JSON display |

## Validation Rules

### VCF File
```javascript
// Must end with .vcf
file.name.endsWith('.vcf') === false
→ Show error: "Invalid file type. Please upload a .vcf file."
→ Add red border to dropzone

file.name.endsWith('.vcf') === true
→ Show success: "[filename] loaded successfully"
→ Add green border to dropzone
```

### Drug Selection
```javascript
// At least one drug required
appState.selectedDrugs.size === 0
→ Show error: "At least one drug is required."

appState.selectedDrugs.size > 0
→ Hide error
→ Enable analysis
```

## Session Management

### Session ID
```javascript
// Generated on page load
const sessionId = `${Math.floor(1000 + Math.random() * 9000)}-BETA`;
// Example: "2843-BETA", "7156-BETA"
```

### Progress Tracking
```javascript
// Initial state
progress = 0%

// During analysis
progress = Loading... (button shows spinner)

// After completion
progress = 100%
```

## Gauge Chart Math

### SVG Path
```
Arc length = π × radius = 3.14159 × 50 = 157
Dash array = 157 (full circle length)
```

### Confidence to Offset
```javascript
const circumference = 157;
const offset = circumference - (circumference * confidence);

// Examples:
confidence = 0.0  → offset = 157 (empty gauge)
confidence = 0.5  → offset = 78.5 (half filled)
confidence = 1.0  → offset = 0 (fully filled)
```

## Toast Notifications

```javascript
// Function
showToast(message)

// Behavior
- Appears bottom-right
- Dark gray background
- White text
- Auto-disappears after 2 seconds
- Z-index: 50 (always on top)

// Usage Examples
showToast('JSON copied to clipboard')
showToast('JSON downloaded')
showToast('JSON refreshed')
```

## Troubleshooting

### Issue: Results not showing
**Check:**
1. `data.analyses` is array with at least 1 item
2. `elements.resultsContainer.classList.remove('hidden')` called
3. Browser console for JavaScript errors

### Issue: Gauge not updating
**Check:**
1. `confidence_score` is number between 0 and 1
2. `#gauge-arc` element exists in DOM
3. Stroke color matches risk level

### Issue: Tabs not switching
**Check:**
1. Tab buttons have correct `data-tab` attribute
2. Tab content divs have correct IDs (`tab-profile`, etc.)
3. `switchTab(tabName)` function called on click

### Issue: JSON not copying
**Check:**
1. Browser supports `navigator.clipboard` API
2. Page served over HTTPS (or localhost)
3. User granted clipboard permissions

## Performance Notes

### File Size Limits
- VCF files: No explicit limit (handle large files with care)
- Recommended: < 5MB for optimal performance

### API Response Time
- Typical: 2-5 seconds
- Includes: VCF parsing + LLM generation
- Button disabled during processing

### Browser Compatibility
- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- Tailwind CSS requires modern CSS support
- Font Awesome 6.x icons

---

**Quick Start:**
1. Upload VCF: Drag file to dropzone
2. Select Drugs: Click dropdown, choose drugs
3. Run Analysis: Click blue button
4. View Results: Check risk status + tabs
5. Export: Copy or download JSON

**Common Pattern:**
```javascript
Upload VCF → Select Drugs → Run Analysis → View Results → Export JSON
```
