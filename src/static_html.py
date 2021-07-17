
import sys
sys.path.insert(0, '../../')
import numpy as np
import os
import time
import shutil
import json
import pandas as pd
import random

from src import constants
from src.ensembl2gene_symbol import  e2g_convertor
import zipfile

import multiprocessing
from functools import reduce
SH_MODULE_NAME = "module"
SH_NUM_GENES = "#_genes"
SH_ENRICHED = "enriched_groups"
SH_DETAILS = "more_details"

SH_TABLE_HEADERS = [SH_MODULE_NAME, SH_NUM_GENES, SH_ENRICHED, SH_DETAILS]

MODULE_TH = 10



def format_script(file_path, uid=True, **kwargs):
    formatted_script = open(file_path+".format").read().format(**kwargs)
    if uid:
        exec_file_name="{}_{}{}".format(os.path.splitext(file_path)[0] ,random.random(), os.path.splitext(file_path)[1]) #
    else:
        exec_file_name = file_path
    open(exec_file_name, "w+").write(formatted_script)
    return exec_file_name


def reduce_to_dict(x,y):
    if y["id"] in x:
        x[y["id"]]["modules"] = x[y["id"]]["modules"] + y["modules"]
    else:
        x[y["id"]]=y
    return x

def merge_two_dicts(x, y):

    z = x.copy()
    z.update(y)
    return z


def draw_network(module_nodes, active_genes, df_network):
    nodes_raw = [ {"score" : int(gene in active_genes), "id" : gene} for gene in module_nodes]
    nodes_formatted=[merge_two_dicts({"id" : k}, v) for k,v in reduce(reduce_to_dict, [{"eid": gene, "id": gene, "gene_symbol": e2g_convertor([gene])[0], "score" : int(gene in active_genes)} for gene in module_nodes], {}).items()]
    nodes_formatted=[{"data" : x, "label" : x["eid"], "selected" : True } for x in nodes_formatted]
    module_edges = [[x.iloc[0], x.iloc[2]] for i, x in df_network.iterrows() if x.iloc[0] in module_nodes and x.iloc[2] in module_nodes]
    additional_edges = [] # [[x.iloc[0], x.iloc[2]] for i, x in pd.read_csv(network_file_name, sep="\t").iterrows() if not (x.iloc[0] in active_genes and x.iloc[2] in active_genes) and (x.iloc[0] in active_genes or x.iloc[2] in active_genes)]
    # additional_nodes = [] # [y for x in (active_edges + additional_edges) for y in x if y if y not in active_genes]
    additional_nodes = [] # list(set(additional_nodes))

    return nodes_formatted + [{"data" : {"id" : x, "eid" : x, "modules" : []}, "label" : ""} for x in additional_nodes] + [{"data": {"id" : x[0]+"_"+x[1], "source":x[0], "target":x[1]}, "label" : ""} for x in additional_edges] + [{"data": {"id" : x[0]+"_"+x[1], "source":x[0], "target":x[1]}, "label" : "-"} for x in module_edges]



def generate_report_from_template(cy, module_index, go_report, output_folder):
    go_report.loc[:,'pval']=go_report.loc[:,'pval'].apply(lambda a: '{:0.3e}'.format(a))
    go_report.loc[:,'qval']=go_report.loc[:,'qval'].apply(lambda a: '{:0.3e}'.format(a))
    report_file_name=format_script(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../data', "graph.html"), NUM_OF_GENES=len([x for x in cy if not "source" in x["data"]]), GO_REPORT=go_report.loc[:,['index', 'GO id','GO name','GO root','pval', 'qval']].iloc[:np.min([go_report.shape[0],100])].to_dict('records'), GRAPH=json.dumps(cy))

    shutil.move(report_file_name, os.path.join(output_folder, "module_{}.html".format(module_index)))
    return "module_{}.html".format(module_index)


def visualize_module(module_file_name, module_index, active_genes_file_name, network_file_name, go_file_name, output_folder):
    print("visualize module {} produced for {} ".format(module_index, active_genes_file_name))
    module_nodes=pd.read_csv(module_file_name, index_col=0, header=None).index.values
    active_genes=pd.read_csv(active_genes_file_name, index_col=0, header=None).index.values
    go_report=pd.read_csv(go_file_name, sep='\t')
    df_network=pd.read_csv(network_file_name, sep="\t")
    cy = draw_network(module_nodes, active_genes, df_network)
    generate_report_from_template(cy, str(module_index), go_report, output_folder)


