#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 16:35:12 2019

@author: inespessoa
"""
import pandas as pd
import numpy as np

def unique_values(df, feature):
    values = df[feature].values
    unique_values = np.unique(values)
    return unique_values

def not_fraudlent_data(df, users, cards):
    df_not_fraud =  df[df["isfraud"]==0]
    df_not_fraud = df_not_fraud[
            (df_not_fraud["user_id"].isin(users)) |\
            (df_not_fraud["card_id"].isin(cards))]
    sample_df_not_fraud = df_not_fraud.sample(n=int(len(df_not_fraud)*0.001))
    return sample_df_not_fraud

df_fraud = pd.read_csv(r"fraudelent_data.csv") 
df_fraud.set_index("id", inplace=True)
unique_users = unique_values(df_fraud, "user_id")
unique_cards = unique_values(df_fraud, "card_id")
chunks = pd.read_csv(
        r"train_v2.csv",
        chunksize=100000
        )
df_sample = pd.concat(
    [not_fraudlent_data(chunk, unique_users, unique_cards)\
         for chunk in chunks])
df_sample.set_index("id", inplace=True)
df_sample.to_csv("not_fraudelent_data.csv") 
pd.concat([df_sample, df_fraud]).to_csv("sample.csv")