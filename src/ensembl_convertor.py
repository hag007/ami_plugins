import src.constants as constants
import os
import pandas as pd 
import numpy as np

def load_gene_list(gene_file_name, gene_list_path=None): #  ="TCGA-SKCM.htseq_counts.tsv"
    if os.path.splitext(gene_file_name)[1]==".sif":
        return get_network_genes(gene_file_name)
    f = open(gene_file_name,'r')
    lines = [l.strip() for l in f]
    f.close()
    return lines


def get_network_genes(network_file):
    df_network = pd.read_csv(network_file, sep="\t")
    src = np.array(df_network.iloc[:,0])
    dst = np.array(df_network.iloc[:,2])
    vertices = list(set(np.append(src, dst)))
    return vertices

