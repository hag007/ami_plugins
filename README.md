# DOMINO

AMI plugins: utilities for AMI algorithms.


- [Requirements](#requirements)
- [Installation](#installation)
- [Input File Formats](#input-file-formats)
- [Basic Usage](#basic-usage)
- [Main output files](#main-output-files)
- [Advanced usage](#advanced-usage)
- [Example files](#example-files)



## Requirements
DOMINO was tested under the following settings:
- Python 3.6, Python 3.7 (Note that for further versions of python some dependency packages are currently not available via pip)
- Linux OS (Ubuntu 14.04 LTS, Ubuntu 18.04.4 LTS)

## Installation

### From sources
Download the sources and install according to the following:

Clone the repo from Github:
```
git clone https://github.com/hag007/ami_plugins.git
cd ami_plugins
```

AMI plugins is written in Python3. The necessary libraries will all be installed by the `setup.py` script.
We recommend using a virtual environment. For example, in Linux, before running `setup.py`:
```
python3 -m venv ami_plugins-env
source ami_plugins-env/bin/activate
```
Then, run setup.py:
```
python setup.py install
```

## Input File Formats

- A file containing a line-separated set of genes for which you wish to test the enrichment

- A file containing a the backgound set against against which you wish to test the background. 
* this file can be either an sif network file (with an sif extension) of line-separated set of backgound genes

## Basic Usage

To run GO enrichment, run the following line:
```
go_enrichment --tested_genes </path/to/network.sif> --background_genes </path/to/output_file> --qval_th 0.05 --output_folder
```

The common command line options are:

`-t/--tested_genes`: File name of the tested genes.

`-n/--network_file`: File name of the background genes.

`-q/--qval_th`: qval threshold for BH correction for multiple testing.

`-o/--output_folder`: output folder for the enrichment results.



## Main output files

`output_folder/tested_genes_enrichment.tsv`: A tsv file containing the results of GO enrichment analysis

## Example files

Example files of networks in simplified sif format and an active gene file are available under "examples" folder  
