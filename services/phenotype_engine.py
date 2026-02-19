def determine_phenotype(gene: str, variants: list) -> dict:
    """
    Determine metabolic phenotype from STAR alleles and build diplotype.
    
    Parameters:
    -----------
    gene : str
        Gene name (e.g., "CYP2D6")
    variants : list
        List of variant dictionaries with STAR alleles
        Example: [{"rsid": "rs3892097", "star": "*4"}, ...]
        
    Returns:
    --------
    dict
        Structure:
        {
            "gene": "CYP2D6",
            "diplotype": "*4/*10",
            "phenotype": "IM",
            "confidence": "high" or "low"
        }
    """
    
    # Phenotype map for all supported genes
    PHENOTYPE_MAP = {
        "CYP2D6": {
            "*1/*1": "NM",
            "*1/*2": "NM",
            "*1/*3": "IM",
            "*1/*4": "IM",
            "*1/*5": "IM",
            "*1/*6": "IM",
            "*1/*10": "IM",
            "*1/*41": "IM",
            "*2/*2": "NM",
            "*3/*4": "PM",
            "*4/*4": "PM",
            "*4/*5": "PM",
            "*4/*6": "PM",
            "*4/*10": "IM",
            "*5/*5": "PM",
            "*41/*41": "NM",
            # Wildcard patterns for combinations
        },
        "CYP2C19": {
            "*1/*1": "NM",
            "*1/*2": "IM",
            "*1/*3": "IM",
            "*2/*2": "PM",
            "*2/*3": "PM",
            "*3/*3": "PM",
        },
        "CYP2C9": {
            "*1/*1": "NM",
            "*1/*2": "IM",
            "*1/*3": "IM",
            "*2/*2": "IM",
            "*2/*3": "PM",
            "*3/*3": "PM",
        },
        "SLCO1B1": {
            "*1/*1": "NM",
            "*1/*5": "IM",
            "*5/*5": "PM",
        },
        "TPMT": {
            "*1/*1": "NM",
            "*1/*3": "IM",
            "*3/*3": "PM",
        },
        "DPYD": {
            "*1/*1": "NM",
            "*1/*2": "IM",
            "*2/*2": "PM",
        }
    }
    
    # Normalize gene name
    gene = str(gene).strip().upper()
    
    # Result structure
    result = {
        "gene": gene,
        "diplotype": None,
        "phenotype": "Unknown",
        "confidence": "low"
    }
    
    try:
        # Handle empty variants list
        if not variants or not isinstance(variants, list):
            result["phenotype"] = "Unknown"
            return result
        
        # Extract STAR alleles from variants
        star_alleles = []
        for variant in variants:
            if isinstance(variant, dict):
                star = variant.get("star")
                if star:
                    star_alleles.append(str(star).strip())
        
        # Handle no alleles found
        if not star_alleles:
            result["phenotype"] = "Unknown"
            return result
        
        # Build diplotype
        if len(star_alleles) >= 2:
            # Multiple alleles: sort and pair them
            sorted_alleles = sorted(star_alleles[:2])
            diplotype = f"{sorted_alleles[0]}/{sorted_alleles[1]}"
            result["confidence"] = "high"
        elif len(star_alleles) == 1:
            # Single allele: assume homozygous
            allele = star_alleles[0]
            diplotype = f"{allele}/{allele}"
            result["confidence"] = "medium"
        else:
            result["phenotype"] = "Unknown"
            return result
        
        result["diplotype"] = diplotype
        
        # Map diplotype to phenotype
        gene_phenotype_map = PHENOTYPE_MAP.get(gene, {})
        
        if diplotype in gene_phenotype_map:
            result["phenotype"] = gene_phenotype_map[diplotype]
        else:
            # Try reverse order if not found (e.g., *10/*4 vs *4/*10)
            reversed_diplotype = f"{sorted_alleles[1]}/{sorted_alleles[0]}" if len(sorted_alleles) >= 2 else None
            
            if reversed_diplotype and reversed_diplotype in gene_phenotype_map:
                result["phenotype"] = gene_phenotype_map[reversed_diplotype]
            else:
                # Unknown diplotype - mark with low confidence
                result["phenotype"] = "Unknown"
                result["confidence"] = "low"
        
        return result
    
    except Exception as e:
        # Catch any unexpected errors
        result["phenotype"] = "Unknown"
        result["error"] = str(e)
        return result
