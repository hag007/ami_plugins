import argparse
import os
from src.go import check_group_enrichment
import src.constants as constants
from  src.static_html import visualize_module
import pandas as pd

def main_go_enrichment():

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
        results=check_group_enrichment(cur_module, background_genes, os.path.join(constants.dir_path,"data"), th=qval_th)
        df_results=pd.DataFrame(data=results)
        output_go_filename=f'{os.path.join(output_folder,"module_go")}_{i}.tsv'
        output_module_filename=f'{os.path.join(output_folder,"module_genes")}_{i}.txt'
        df_results.to_csv(output_go_filename, sep='\t',index_label="index")
        open(output_module_filename,'w+').write("\n".join(cur_module))
        print(f'written GO enrichment results to {output_go_filename} and {output_module_filename}')


def main_visualize_module():

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-m', '--module_file_name', dest='module_file_name', help='', default="")
    parser.add_argument('-a', '--active_genes_file_name', dest='active_genes_file_name', default="")
    parser.add_argument('-n', '--network_file_name', dest='network_file_name', default="")
    parser.add_argument('-g', '--go_file_name', dest='go_file_name', default="")
    parser.add_argument('-o', '--output_folder', dest='output_folder', default="")


    args = parser.parse_args()
    module_file_name = args.module_file_name
    active_genes_file_name = args.active_genes_file_name 
    network_file_name = args.network_file_name
    go_file_name = args.go_file_name
    output_folder = args.output_folder
    module_index = os.path.splitext(os.path.basename(module_file_name))[0].split('_')[-1]
    visualize_module(module_file_name, module_index, active_genes_file_name, network_file_name, go_file_name, output_folder)
    print(f'finished generating module ${module_index}')

