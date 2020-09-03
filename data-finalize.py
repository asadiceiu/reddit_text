# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 01:28:50 2020

@author: azaman

This will open all data grabbed from reddit and put into a single file removing any duplicates based on url. 
The duplicates might exists because we downloaded data based on keywords and the same post on reddit could
include more than one keywords. 
"""
import pandas as pd, os, re
import numpy as np, glob


#files = np.concatenate((glob.glob('grabbed_data/*.csv', recursive=True), glob.glob('grabbed_data/keyword/*.csv', recursive=True)))
# get all files fromgrabbed_data/keyword directory
files = glob.glob('grabbed_data/keyword/*.csv', recursive=True)
# read the first file
df = pd.read_csv(files[0])
count = len(df)
# read all file and concat the dataset to the first dataset sequentially with dropping any duplicate entries based on the url
for f in files:
    df2 = pd.read_csv(f)
    count += len(df2)
    df = pd.concat([df, df2]).drop_duplicates(subset=['url']).reset_index().drop(columns=['index','Unnamed: 0'])
    print(f, len(df), count)
# write all data to a single csv file
df.to_csv('reddit-all.csv')