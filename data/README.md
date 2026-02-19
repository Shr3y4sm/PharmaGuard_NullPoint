# 🧬 Sample VCF Files

This directory contains sample VCF (Variant Call Format) files for testing PharmaGuard's pharmacogenomic analysis capabilities.

## 📁 Available Samples

### 1. `sample_normal_metabolizer.vcf`
**Patient ID**: NORMAL_001  
**Risk Level**: Low  
**Description**: Standard metabolizer profile with heterozygous variants  
**Genes**: CYP2C19, CYP2C9  
**Use Case**: Testing normal metabolizer phenotype analysis  
**Expected Results**: 
- Standard dosing recommendations
- Low to moderate risk flags
- Typical phenotype assignments

---

### 2. `sample_poor_metabolizer.vcf`
**Patient ID**: POOR_002  
**Risk Level**: HIGH  
**Description**: Poor metabolizer profile with multiple homozygous variants  
**Genes**: CYP2C19, CYP2C9  
**Use Case**: Testing high-risk patient scenarios  
**Expected Results**: 
- Dosage reduction recommendations
- Multiple high-risk warnings
- Poor metabolizer phenotype
- Requires careful monitoring

---

### 3. `sample_ultra_rapid_metabolizer.vcf`
**Patient ID**: ULTRA_003  
**Risk Level**: Moderate  
**Description**: Ultra-rapid metabolizer profile  
**Genes**: CYP2C19  
**Use Case**: Testing enhanced metabolism scenarios  
**Expected Results**: 
- Increased dosage may be needed
- Reduced drug efficacy warnings
- Ultra-rapid metabolizer phenotype

---

### 4. `sample_multi_drug.vcf`
**Patient ID**: COMPLEX_004  
**Risk Level**: Complex  
**Description**: Comprehensive case with variants in multiple genes  
**Genes**: CYP2C19, CYP2C9, SLCO1B1, MTHFR  
**Use Case**: Testing multi-drug analysis and complex interactions  
**Expected Results**: 
- Multiple drug recommendations
- Various phenotype assignments
- Comprehensive clinical guidance
- Drug-drug interaction considerations

---

### 5. `sample_wildtype.vcf`
**Patient ID**: WILDTYPE_005  
**Risk Level**: Minimal  
**Description**: All wild-type alleles (no variants)  
**Genes**: SLCO1B1, MTHFR  
**Use Case**: Testing baseline/normal genotype scenarios  
**Expected Results**: 
- Standard dosing for all drugs
- Normal metabolizer status
- Minimal risk warnings

---

### 6. `test_patient.vcf`
**Patient ID**: TEST_PATIENT  
**Risk Level**: Moderate  
**Description**: Original test file with CYP2D6 and CYP2C19 variants  
**Genes**: CYP2D6, CYP2C19  
**Use Case**: General testing and development  

---

## 🧪 Testing Each Sample

### Using the Web Interface

1. Navigate to `http://localhost:5000`
2. Upload any sample VCF file
3. Enter drug names (e.g., CODEINE, WARFARIN, CLOPIDOGREL)
4. Click "Analyze" to see results

### Using cURL

```bash
curl -X POST http://localhost:5000/analyze \
  -F "vcf_file=@data/sample_poor_metabolizer.vcf" \
  -F "drugs=CODEINE, WARFARIN"
```

### Example Test Scenarios

#### Scenario 1: Test Poor Metabolizer with CODEINE
```bash
# Upload: sample_poor_metabolizer.vcf
# Drugs: CODEINE
# Expected: High risk warning, dosage reduction recommended
```

#### Scenario 2: Test Multi-Drug Analysis
```bash
# Upload: sample_multi_drug.vcf
# Drugs: CODEINE, WARFARIN, CLOPIDOGREL, SIMVASTATIN
# Expected: Multiple recommendations with varying risk levels
```

#### Scenario 3: Test Wildtype Patient
```bash
# Upload: sample_wildtype.vcf
# Drugs: WARFARIN
# Expected: Standard dosing recommended
```

---

## 📊 VCF Format Details

All sample files follow VCF v4.2 format specification:

```
##fileformat=VCFv4.2
##fileDate=YYYYMMDD
##source=PharmaGuard_Sample
##reference=GRCh38
#CHROM  POS     ID          REF ALT QUAL    FILTER  INFO    FORMAT  SAMPLE
chr22   42126611 rs4244285  G   A   100     PASS    DP=50   GT:DP   0/1:50
```

### Genotype Codes
- `0/0`: Homozygous reference (wild-type)
- `0/1`: Heterozygous variant
- `1/1`: Homozygous variant

---

## 🎯 Supported Genes & Drugs

### Genes in Samples
- **CYP2C19**: Affects CLOPIDOGREL metabolism
- **CYP2C9**: Affects WARFARIN metabolism
- **CYP2D6**: Affects CODEINE metabolism
- **SLCO1B1**: Affects SIMVASTATIN transport
- **DPYD**: Affects FLUOROURACIL metabolism
- **TPMT**: Affects various immunosuppressants

### Testable Drugs
- CODEINE
- WARFARIN
- CLOPIDOGREL
- SIMVASTATIN
- FLUOROURACIL

---

## 🔬 Creating Custom VCF Files

To create your own test VCF files:

1. **Use VCF v4.2 format**
2. **Include required headers**: fileformat, reference, INFO, FORMAT
3. **Add variant lines**: CHROM, POS, ID (rs number), REF, ALT, QUAL, FILTER, INFO, FORMAT, SAMPLE
4. **Use GRCh38 coordinates** for chromosome positions
5. **Include relevant pharmacogenes**: CYP2C19, CYP2C9, CYP2D6, etc.

### Example Variant Line
```
chr22   42126611    rs4244285   G   A   100 PASS    DP=50;AF=0.5    GT:DP   0/1:50
```

### Key rs Numbers (SNP IDs)
- **rs4244285**: CYP2C19*2 (poor metabolizer)
- **rs1799853**: CYP2C9*2 (reduced function)
- **rs1057910**: CYP2C9*3 (reduced function)
- **rs12248560**: CYP2C19*17 (increased function)
- **rs4149056**: SLCO1B1*5 (reduced function)

---

## 📚 Additional Resources

- [VCF Specification](https://samtools.github.io/hts-specs/VCFv4.2.pdf)
- [PharmGKB Database](https://www.pharmgkb.org/)
- [CPIC Guidelines](https://cpicpgx.org/)
- [dbSNP Database](https://www.ncbi.nlm.nih.gov/snp/)

---

## ⚠️ Important Notes

1. **Test Data Only**: These files are for testing purposes only and do not represent real patient data
2. **Simplified**: Real VCF files may contain hundreds of variants; these are focused on pharmacogenes
3. **GRCh38**: All coordinates use GRCh38/hg38 reference genome
4. **HIPAA Compliance**: Never use real patient VCF files without proper authorization

---

**Last Updated**: February 2026  
**Version**: 1.0.0
