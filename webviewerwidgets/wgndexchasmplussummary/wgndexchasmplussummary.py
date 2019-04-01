import os
import sys
script_dir = os.path.dirname(__file__)
sys.path = [script_dir] + sys.path
import data_model as dm
del sys.path[0]
import json

e_data = dm.EnrichmentData(os.path.join(script_dir, "data"))
e_data.load()

def run_query (hugos):
    query_ids = hugos
    matched_genes = {}
    for term in query_ids:
        matched_genes[term] = [term]
    standardized_search_terms = {'matched': matched_genes, 'unmatched':[]}
    result = e_data.get_scores_on_standarized_query_terms('cravat_nci', standardized_search_terms, False)
    return result

async def get_data (queries):
    params = json.loads(queries['params'])
    hugos = params['hugos']
    response = {'data': run_query(hugos)}
    return response

if __name__ ==  '__main__':
    run_query(['BRCA1', 'BRCA2'])
