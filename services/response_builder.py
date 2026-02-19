import json
from datetime import datetime
import uuid


def build_response_json(
    drug: str,
    gene: str,
    phenotype: str,
    diplotype: str,
    variant_count: int,
    variants: list,
    vcf_parsing_success: bool,
    cpic_level: str = None,
    patient_id: str = None,
    clinical_recommendation: dict = None,
    llm_explanation: dict = None
) -> dict:
    """
    Build the structured JSON response matching the required schema.
    
    Parameters:
    -----------
    drug : str
        Drug name (uppercase)
    gene : str
        Primary gene symbol
    phenotype : str
        Metabolic phenotype (PM, IM, NM, RM, URM, Unknown)
    diplotype : str
        Diplotype string (e.g., "*1/*4")
    variant_count : int
        Number of detected variants
    variants : list
        List of variant dictionaries with rsid, star, etc.
    vcf_parsing_success : bool
        Whether VCF parsing was successful
    cpic_level : str
        CPIC evidence level (A, B, C)
    patient_id : str
        Patient ID (auto-generated if not provided)
    clinical_recommendation : dict
        Clinical recommendation from LLM
    llm_explanation : dict
        LLM-generated explanation
        
    Returns:
    --------
    dict
        Structured JSON matching the required schema
    """
    
    # Generate patient ID if not provided
    if not patient_id:
        patient_id = f"PATIENT_{uuid.uuid4().hex[:8].upper()}"
    
    # Get current timestamp in ISO8601 format
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Determine risk assessment based on phenotype
    risk_assessment = _determine_risk_assessment(phenotype, cpic_level, drug)
    
    # Build pharmacogenomic profile
    pharmacogenomic_profile = {
        "primary_gene": gene,
        "diplotype": diplotype,
        "phenotype": phenotype,
        "detected_variants": variants if variants else []
    }
    
    # Build quality metrics
    quality_metrics = {
        "vcf_parsing_success": vcf_parsing_success,
        "variant_count": variant_count,
        "data_completeness": "high" if variant_count > 0 else "low"
    }
    
    # Build main response
    response = {
        "patient_id": patient_id,
        "drug": drug,
        "timestamp": timestamp,
        "risk_assessment": risk_assessment,
        "pharmacogenomic_profile": pharmacogenomic_profile,
        "clinical_recommendation": clinical_recommendation or {
            "dosage_adjustment": "Pending LLM analysis",
            "monitoring": "Standard monitoring recommended",
            "alternative_drugs": [],
            "urgency": "routine"
        },
        "llm_generated_explanation": llm_explanation or {
            "summary": "Awaiting LLM analysis",
            "mechanism": "Not available",
            "interaction_notes": [],
            "evidence_basis": "Pending"
        },
        "quality_metrics": quality_metrics
    }
    
    return response


def _determine_risk_assessment(phenotype: str, cpic_level: str = None, drug: str = None) -> dict:
    """
    Determine risk assessment based on phenotype and CPIC level.
    
    Parameters:
    -----------
    phenotype : str
        Metabolic phenotype
    cpic_level : str
        CPIC evidence level
    drug : str
        Drug name (optional, for context)
        
    Returns:
    --------
    dict
        Risk assessment with risk_label, confidence_score, severity
    """
    
    # Risk mapping based on phenotype
    phenotype_risk_map = {
        "PM": {"label": "Toxic", "severity": "critical", "confidence": 0.95},
        "IM": {"label": "Adjust Dosage", "severity": "moderate", "confidence": 0.85},
        "NM": {"label": "Safe", "severity": "none", "confidence": 0.90},
        "RM": {"label": "Adjust Dosage", "severity": "low", "confidence": 0.80},
        "URM": {"label": "Ineffective", "severity": "high", "confidence": 0.85},
        "Unknown": {"label": "Unknown", "severity": "low", "confidence": 0.60}
    }
    
    # Get default risk
    risk_data = phenotype_risk_map.get(phenotype, phenotype_risk_map["Unknown"])
    
    # Adjust confidence based on CPIC level
    confidence = risk_data["confidence"]
    if cpic_level == "A":
        confidence = min(0.99, confidence + 0.05)
    elif cpic_level == "B":
        confidence = min(0.95, confidence + 0.03)
    elif cpic_level == "C":
        confidence = max(0.70, confidence - 0.10)
    
    return {
        "risk_label": risk_data["label"],
        "confidence_score": round(confidence, 2),
        "severity": risk_data["severity"]
    }


def prepare_llm_prompt(
    drug: str,
    gene: str,
    phenotype: str,
    diplotype: str,
    cpic_level: str = None,
    variants: list = None
) -> str:
    """
    Prepare a structured prompt for LLM API to generate patient-friendly clinical recommendations.
    
    Parameters:
    -----------
    drug : str
        Drug name
    gene : str
        Gene symbol
    phenotype : str
        Metabolic phenotype
    diplotype : str
        Diplotype
    cpic_level : str
        CPIC evidence level
    variants : list
        Detected variants
        
    Returns:
    --------
    str
        Formatted prompt for LLM with patient-friendly language
    """
    
    phenotype_explanation = {
        "PM": "Poor Metabolizer (your body breaks down this drug slowly)",
        "IM": "Intermediate Metabolizer (your body breaks down this drug at a moderate pace)",
        "NM": "Normal Metabolizer (your body breaks down this drug at a normal pace)",
        "RM": "Rapid Metabolizer (your body breaks down this drug quickly)",
        "URM": "Ultra-Rapid Metabolizer (your body breaks down this drug very quickly)",
        "Unknown": "Unknown Metabolizer status"
    }
    
    phenotype_desc = phenotype_explanation.get(phenotype, phenotype)
    
    prompt = f"""You are a healthcare expert explaining medication genetics to a patient in simple, easy-to-understand language.

PATIENT'S GENETIC PROFILE:
- Medication: {drug}
- Gene involved: {gene} (this gene controls how your body processes {drug})
- Your metabolism type: {phenotype_desc}
- Your genetic combination: {diplotype}
- Science confidence: {cpic_level or 'Standard'} level evidence
- Genetic markers found: {len(variants or [])} identified

IMPORTANT: Use simple language, avoid medical jargon, explain things a patient can understand, and be encouraging.

Please provide information in this JSON format:
{{
  "clinical_recommendation": {{
    "dosage_adjustment": "In simple terms, whether you should take more, less, or standard amounts of {drug}",
    "monitoring": "What you and your doctor should watch for or check regularly",
    "alternative_drugs": ["Other medications that might work better for you based on your genetics"],
    "urgency": "How important it is to discuss this with your doctor: routine|important|urgent"
  }},
  "llm_generated_explanation": {{
    "summary": "A simple 1-2 sentence explanation of what your genetics mean for {drug}",
    "mechanism": "In plain English, how your genes affect how {drug} works in your body",
    "interaction_notes": ["Simple practical tips you should know about taking {drug}", "Other important things to discuss with your doctor"],
    "evidence_basis": "How confident doctors are in this information (based on scientific research)"
  }}
}}

Remember: Write for a patient who has no medical background. Use 'you' and 'your'. Be supportive and clear."""
    
    return prompt


def format_response_for_json_output(response_dict: dict) -> str:
    """
    Format the response dictionary as pretty JSON string.
    
    Parameters:
    -----------
    response_dict : dict
        The response dictionary
        
    Returns:
    --------
    str
        Formatted JSON string
    """
    return json.dumps(response_dict, indent=2)
