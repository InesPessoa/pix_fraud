#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:16:03 2019

@author: inespessoa
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as imbPipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn import feature_selection
from sklearn.model_selection import cross_val_predict

    
df_sample = pd.read_csv(r"sample_featured.csv", index_col=0) 
x = df_sample.drop(columns=["isfraud"]).values
y = df_sample["isfraud"].values

df_sample_test = pd.read_csv(r"sample_test_featured.csv", index_col=0) 
x_test = df_sample_test.values

clf = DecisionTreeClassifier()
fs = feature_selection.SelectPercentile(feature_selection.f_classif, percentile=10)

pipeline = imbPipeline([("undersampler", RandomUnderSampler()),
                        ("scale", StandardScaler()),
                        ("fs", fs),
                        ("reduce_dims", PCA(0.9)), #ver o que se passa
                        ("decisiontree", clf)
                        ])


scrore = cross_val_score(pipeline, x, y, scoring='accuracy', cv=5).mean()
y_pred = cross_val_predict(pipeline, x, y, cv=5)
conf_mat2 = confusion_matrix(y, y_pred)
print(conf_mat2)
pipeline.fit(x, y)
prediction = pipeline.predict_proba(x_test)
prediction = pd.DataFrame({"id": df_sample_test.index.values, "isfraud":prediction[:,1]})
prediction.set_index("id", inplace=True)
prediction.to_csv("results.csv")
