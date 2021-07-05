import argparse
import os
from src.go import check_group_enrichment
import src.constants as constants
import pandas as pd

def main():

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-t', '--tested_genes', dest='tested_genes', help='', default="")
    parser.add_argument('-n', '--background_genes', dest='background_genes', help='', default="")
    parser.add_argument('-q', '--qval_th', dest='qval_th', default="")
    parser.add_argument('-o', '--output_folder', dest='output_folder', default="")


    args = parser.parse_args()
    tested_genes = args.tested_genes
    background_genes = args.background_genes
    output_folder = args.output_folder
    qval_th = float(args.qval_th)
    lns=open(tested_genes, 'r').readlines()
    for i, l in enumerate(lns):
        cur_module=l.strip()[1:-1].split(", ")
        print(len(l))
        results=check_group_enrichment(cur_module, background_genes, os.path.join(constants.dir_path,"data"), th=qval_th)
        df_results=pd.DataFrame(data=results)
        output_filename=f'{os.path.join(output_folder,os.path.splitext(os.path.basename(tested_genes))[0])}_{i}.tsv'
        df_results.to_csv(output_filename, sep='\t', index=False)
        print(f'written GO enrichment results to {output_filename}')
#         return(results)

