#!/usr/bin/env python3

import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--qcovs', type=int, required=True,
                        help='query coverage by subject threshold')
    parser.add_argument('--cols', type=str, required=True,
                        help='Column names for BLAST results')
    parser.add_argument('--input', type=str, required=True,
                        help='BLAST results')
    parser.add_argument('--output', type=str, required=True,
                        help='filtered results')
                        

    args = parser.parse_args()
    return args

def filter():
    args = parse_args()

    df = pd.read_csv(
        args.input,
        index_col = None,
        header    = None,
        names     = args.cols.split(),
        sep       = '\t'
        )
    
    df = df[df['covs'] >= args.qcovs]
    
    df.to_csv(args.output, index = False, header = False, sep = '\t')

if __name__ == '__main__':
    filter()