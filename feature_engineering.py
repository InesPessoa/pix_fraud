# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:32:47 2019

@author: inespessoa
"""
import pandas as pd
import numpy as np

def frequency_in_transactions(df, column_name, group):
    """
    calculates the percentage in total transactions
    that each categorical value appears
    """
    series = df[column_name]
    count_values = series.value_counts()
    percent_values = series.apply(lambda x: count_values[x]/len(series))
    df[column_name + group] = percent_values
    return df

def diff_from_avg(df, column_name, group):
    series = df[column_name]
    mean = np.mean(series.values)
    std = np.std(series.values)
    if std != 0:
       df[column_name + group] = (series.values - mean)/std
    else:
        df[column_name + group] = np.zeros(len(df.index))
    return df

def timedelta_avg(df, column_name, group):
    df.sort_values(by=[column_name], inplace=True)
    diff_values = df[column_name].diff().dropna().values
    if len(diff_values) > 1:
        mean = np.mean(diff_values.dropna().values)
        std = np.std(diff_values.dropna().values)
        df[column_name + group] = (diff_values.fillna(mean).values - mean)/std
    else:
        df[column_name + group] = np.zeros(len(df.index))
    return df

#csv_name = "sample"
csv_name = "sample_test"
df = pd.read_csv(csv_name + ".csv", index_col=0)
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
#df_dummies_user_id = pd.get_dummies(df["user_id"])
#df_dummies_card_id = pd.get_dummies(df["card_id"])
categorical_values = np.array(["product_id", "product_department",
                      "product_category", "user_id", "card_id"])
for i in np.delete(categorical_values, -2):
    df = df.groupby(["user_id"]).apply(lambda x: frequency_in_transactions(x, i, "user"))
for i in np.delete(categorical_values, -1):
    df = df.groupby(["card_id"]).apply(lambda x: frequency_in_transactions(x, i, "card"))
for i in np.delete(np.delete(categorical_values, -1), -1):
    df = df.groupby(["card_id", "user_id"]).apply(lambda x: frequency_in_transactions(x, i, "card_user"))
numerical_values = np.array(["C15", "C16", "C17", "C18",
                       "C19","C20", "C21", "amount"])
for i in numerical_values:
    df = df.groupby(["user_id"]).apply(lambda x: diff_from_avg(x, i, "user"))
for i in numerical_values:
    df = df.groupby(["card_id"]).apply(lambda x: diff_from_avg(x, i, "card"))
for i in numerical_values:
    df = df.groupby(["card_id", "user_id"]).apply(lambda x: diff_from_avg(x, i, "card_user"))
df = df.groupby(["user_id"]).apply(lambda x: diff_from_avg(x, "timestamp", "user"))
df = df.groupby(["card_id"]).apply(lambda x: diff_from_avg(x, "timestamp", "card"))
df = df.groupby(["card_id", "user_id"]).apply(lambda x: frequency_in_transactions(x, "timestamp", "card_user"))
#df = pd.concat([
#                df_dummies_user_id, 
#                df_dummies_card_id,
#                df], axis=1)
df.drop(columns=["product_id", "product_department",\
                 "product_category", "user_id", "card_id", "timestamp"], inplace=True)
df.to_csv(csv_name + "_featured" ".csv")
    
    
    
