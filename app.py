from flask import Flask, render_template, request
from services.cpic_loader import load_cpic_data
from cpic_engine import initialize_cpic_engine
from services.vcf_parser import parse_vcf
from services.drug_gene_matcher import match_drug_with_vcf
from services.phenotype_engine import determine_phenotype

app = Flask(__name__)

# Load CPIC data at startup
try:
    CPIC_ENGINE = initialize_cpic_engine("data/cpic_gene-drug_pairs.xlsx")
except Exception as e:
    print(f"Fatal error: Could not load CPIC data - {e}")
    raise


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze VCF file and drugs for pharmacogenomic variants and phenotypes.
    """
    try:
        # Get uploaded VCF file
        if 'vcf_file' not in request.files:
            return render_template('index.html', error="No VCF file provided")
        
        vcf_file = request.files['vcf_file']
        if vcf_file.filename == '':
            return render_template('index.html', error="No VCF file selected")
        
        # Get drug input
        drugs_input = request.form.get('drugs', '')
        if not drugs_input:
            return render_template('index.html', error="No drugs provided")
        
        # Parse VCF file
        print("=" * 60)
        print("Starting VCF analysis...")
        vcf_data = parse_vcf(vcf_file)
        print(f"VCF parsing success: {vcf_data.get('vcf_parsing_success')}")
        
        # Check if VCF parsing was successful
        if not vcf_data.get('vcf_parsing_success'):
            error_msg = vcf_data.get('error', 'Unknown VCF parsing error')
            print(f"VCF parsing failed: {error_msg}")
            return render_template('index.html', error=f"VCF parsing error: {error_msg}")
        
        # Print parsed genes
        parsed_genes = list(vcf_data.get('variants', {}).keys())
        genes_with_variants = [g for g in parsed_genes if vcf_data['variants'][g]]
        print(f"Genes found in VCF: {genes_with_variants}")
        
        # Split drugs by comma and strip whitespace
        drug_list = [d.strip() for d in drugs_input.split(',') if d.strip()]
        print(f"Analyzing {len(drug_list)} drug(s): {drug_list}")
        
        # Build results
        results = []
        
        for drug in drug_list:
            print(f"\n--- Processing drug: {drug} ---")
            
            # Match drug with VCF data
            match_result = match_drug_with_vcf(drug, vcf_data, CPIC_ENGINE)
            print(f"Drug match result: {match_result}")
            
            # Check if drug is valid and gene found in VCF
            if match_result.get('valid') and match_result.get('gene_found_in_vcf'):
                gene = match_result.get('gene')
                variant_count = match_result.get('variant_count', 0)
                
                # Get variants for this gene
                gene_variants = vcf_data['variants'].get(gene, [])
                print(f"Found {variant_count} variant(s) for gene {gene}")
                
                # Determine phenotype
                phenotype_result = determine_phenotype(gene, gene_variants)
                print(f"Phenotype result: {phenotype_result}")
                
                # Build result entry
                result_entry = {
                    "drug": match_result.get('drug'),
                    "gene": gene,
                    "phenotype": phenotype_result.get('phenotype'),
                    "diplotype": phenotype_result.get('diplotype'),
                    "variant_count": variant_count,
                    "cpic_level": match_result.get('cpic_level')
                }
                results.append(result_entry)
                print(f"Added to results: {result_entry}")
            
            elif match_result.get('valid'):
                # Drug is valid but gene not found in VCF
                print(f"Drug {drug} is valid but no variants found in VCF")
                result_entry = {
                    "drug": match_result.get('drug'),
                    "gene": match_result.get('gene'),
                    "phenotype": "Not available in VCF",
                    "diplotype": None,
                    "variant_count": 0,
                    "cpic_level": match_result.get('cpic_level')
                }
                results.append(result_entry)
            
            else:
                # Drug not valid
                print(f"Drug {drug} not valid: {match_result.get('error')}")
                result_entry = {
                    "drug": match_result.get('drug'),
                    "error": match_result.get('error'),
                    "phenotype": "Error"
                }
                results.append(result_entry)
        
        print(f"\n{'=' * 60}")
        print(f"Analysis complete. Total results: {len(results)}")
        print(f"Results: {results}")
        
        # Pass results to template
        return render_template('index.html', results=results, vcf_parsed=True)
    
    except Exception as e:
        print(f"Unexpected error in /analyze: {str(e)}")
        return render_template('index.html', error=f"Analysis error: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)