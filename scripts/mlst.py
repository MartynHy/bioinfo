#!/usr/bin/env python3

import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--cols', type=str, required=True)
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--input2', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()
    return args

def mlst():

    args = parse_args()

    df_query = pd.read_csv(args.input, index_col=None, header=None, names=args.cols.split(), sep='\t')
    df_mlst = pd.read_table(args.input2)

    

    df_query = df_query.loc[:, 'gene':'allele']
    df_query = df_query.set_index('gene')
    df_query_sq = df_query.squeeze('columns')
    df_query_sq = df_query_sq.astype(int)

    results = df_mlst[df_mlst[df_query_sq.index].astype(int) == df_query_sq]
    results.to_csv(args.output, index = False, header = False, sep = '\t')

if __name__ == '__main__':
    mlst()
