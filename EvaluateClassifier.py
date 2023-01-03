# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 10:34:10 2022

@author: Alex
"""
# program that evaluate several classifier to find the best of them, at the end draw plots and make a t-test
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_validate
# for statistical test
from scipy.stats import wilcoxon
# for t-test
from scipy import stats

#prepare the df for the classifiers
# - read dataset from csv
df = pd.read_csv('dataset\star_classification.csv')

# -- preprocessing
# -- remove useless column
dfProc0 = df.drop(columns=['obj_ID','run_ID', 'rerun_ID','cam_col','field_ID','spec_obj_ID','plate','MJD','fiber_ID'])
# -- remove redshift column
dfReduced = dfProc0.drop(columns=['redshift'])
# --remove incorrect sample in position 79545 with values [224.00652611366,-0.624303881323656,-9999,-9999,18.1656,18.01675,-9999,"STAR"] 
dfPreprocessed = dfReduced.drop([79543])
# --array of training sample
X = dfPreprocessed.iloc[:,[0,1,2,3,4,5,6]]
# -- array of target values
Y = dfPreprocessed.loc[:,"class"]

# fit the classifiers and obtain accuracy
# - first classifier -> Random Forest (100)
clf_RF = RandomForestClassifier(n_estimators=100)
# classifier score
scores_RF = cross_validate(clf_RF, X, Y, cv=10,n_jobs=-1)

# - second classifer -> KNN (5)
clf_KNN = KNeighborsClassifier(5)
# classifier score
scores_KNN = cross_validate(clf_KNN, X, Y, cv=10,n_jobs=-1)

# - third classifer -> J48 
clf_tree = DecisionTreeClassifier(random_state=0)
# classifier score
scores_tree = cross_validate(clf_tree, X, Y, cv=10,n_jobs=-1)

# merge performance of the classifiers
metrics = pd.DataFrame({'RandomForest':scores_RF['test_score'],'KNN': scores_KNN['test_score'],'J48': scores_tree['test_score']})
print(metrics)
# plot accuracy
metrics.boxplot()

# statistical test
# - wilcox test
print("Result of wilcox test: ",wilcoxon(metrics['RandomForest'],metrics['KNN']))
# - t-test
print("Result of t-test: ",stats.ttest_rel(metrics['RandomForest'], metrics['KNN']))