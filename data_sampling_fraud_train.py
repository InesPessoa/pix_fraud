#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:20:33 2019

@author: inespessoa
"""
import pandas as pd
import numpy as np

def fraudlent_data(df):
    df_fraud =  df[df["isfraud"]==1]
    sample_df_fraud = df_fraud.sample(n=int(len(df_fraud)*0.001))
    return sample_df_fraud
     
chunks = pd.read_csv(
        r"train_v2.csv",
        chunksize=100000
        )
df_sample = pd.concat(
    [fraudlent_data(chunk) for chunk in chunks])
df_sample.set_index("id", inplace=True)
df_sample.to_csv("fraudelent_data.csv") 
    