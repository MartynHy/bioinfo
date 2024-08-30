#!/usr/bin/env python3

import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--cols', type=str, required=True)
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)

    args = parser.parse_args()
    return args

def filtered_modif():

    args = parse_args()

    df = pd.read_csv(args.input, index_col=None, header=None, names=args.cols.split(), sep='\t')

    df.drop_duplicates('qseqid', inplace = True) 

    df[['gene', 'allele']] = df['qseqid'].str.rsplit(pat = '_', expand = True)
    

    if len(df.index) !== 7 and df['gene'].is_unique()== False:
        print('ST and CC of strain is unknown')
        break
    else:
        pass

    df.to_csv(args.output, index = False, header = False, sep = '\t')

if __name__ == '__main__':
    filtered_modif()