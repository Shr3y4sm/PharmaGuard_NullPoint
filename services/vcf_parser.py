def parse_vcf(file) -> dict:
    """
    Parse a VCF v4.2 file and extract pharmacogenomic variants.
    
    Parameters:
    -----------
    file : file-like object
        The VCF file uploaded via Flask (e.g., file from request.files)
        
    Returns:
    --------
    dict
        Structure:
        {
            "vcf_parsing_success": True/False,
            "variants": {
                "CYP2D6": [{"rsid": "rs...", "star": "*4"}, ...],
                "CYP2C19": [...],
                ...
            }
        }
    """
    
    # Supported pharmacogenomic genes
    SUPPORTED_GENES = {
        "CYP2D6",
        "CYP2C19",
        "CYP2C9",
        "SLCO1B1",
        "TPMT",
        "DPYD"
    }
    
    # Result structure
    result = {
        "vcf_parsing_success": False,
        "variants": {}
    }
    
    try:
        # Initialize gene dictionaries
        for gene in SUPPORTED_GENES:
            result["variants"][gene] = []
        
        # Read file line by line
        for line in file:
            # Handle both bytes and string
            if isinstance(line, bytes):
                line = line.decode('utf-8').strip()
            else:
                line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip header lines
            if line.startswith("#"):
                continue
            
            try:
                # Parse VCF line
                fields = line.split('\t')
                
                # VCF standard format: CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, ...
                if len(fields) < 8:
                    continue
                
                info_field = fields[7]
                
                # Parse INFO field (KEY=VALUE;KEY=VALUE;...)
                info_dict = {}
                for info_pair in info_field.split(';'):
                    if '=' in info_pair:
                        key, value = info_pair.split('=', 1)
                        info_dict[key] = value
                    else:
                        info_dict[info_pair] = True
                
                # Extract required fields
                gene = info_dict.get("GENE", "").upper()
                rsid = info_dict.get("RS", "")
                star = info_dict.get("STAR", "")
                
                # Only process if gene is supported
                if gene not in SUPPORTED_GENES:
                    continue
                
                # Build variant object
                variant = {}
                
                if rsid:
                    variant["rsid"] = rsid
                
                if star:
                    variant["star"] = star
                
                # Only add if we have at least rsid or star
                if variant:
                    result["variants"][gene].append(variant)
            
            except Exception as e:
                # Skip malformed lines
                continue
        
        result["vcf_parsing_success"] = True
        
    except Exception as e:
        # Catch any unexpected errors during file reading
        print(f"Error parsing VCF file: {e}")
        result["vcf_parsing_success"] = False
        result["error"] = str(e)
    
    return result
