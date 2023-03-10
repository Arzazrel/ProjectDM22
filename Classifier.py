# -*- coding: utf-8 -*-
"""
@author: Alessandro Diana

explanation: file containing the class that trains the classifier and predicts the newly added celestial bodies
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

class Classifier:
    # constructor
    def __init__(self):
        # var ready indicate if the classifier is ready for prediction or not
        self.ready = False
        # var that will contain the classifier
        self.classifier = None
        # var that will contain the preprocessed DS
        self.df_preprocessed = None
        
    # method for read and preprocessed DS, used in the development and testing phase
    def preprocess_ds(self):
        # read dataset from csv
        df = pd.read_csv('dataset\star_classification.csv')
        # preprocessing
        # remove useless column
        dfProc0 = df.drop(columns=['obj_ID','run_ID', 'rerun_ID','cam_col','field_ID','spec_obj_ID','plate','MJD','fiber_ID'])
        # remove redshift column
        dfReduced = dfProc0.drop(columns=['redshift'])
        # remove incorrect sample in position 79545 with values [224.00652611366,-0.624303881323656,-9999,-9999,18.1656,18.01675,-9999,"STAR"] 
        self.df_preprocessed = dfReduced.drop([79543])
       
    # method for set the dataset by parameter
    def set_ds(self, dataset):
        if len(dataset) != 0:
            self.df_preprocessed = pd.DataFrame(dataset)    
        
    # method to train the model, to make classifier
    def train_model(self):
        # array of training sample
        X = self.df_preprocessed.iloc[:,[0,1,2,3,4,5,6]]
        # array of target values
        Y = self.df_preprocessed.loc[:,7]
        
        # model
        self.classifier = RandomForestClassifier(n_estimators=100)
        # fit the model
        self.classifier.fit(X.values, Y)
        
        # set that classifier is ready to predict
        self.ready = True
    
    # method to classify a new object
    def predict(self, new_object):
        try:
            result = self.classifier.predict(new_object)
            return result[0]
        except ValueError:
            return "That was no valid number. Try again..."
        
    # method that return the mean result of 10 cross validation
    def cross_validation_result(self):
        # array of training sample
        X = self.df_preprocessed.iloc[:,[0,1,2,3,4,5,6]]
        # array of target values
        Y = self.df_preprocessed.loc[:,"class"]
        
        # classifier score
        scores = cross_validate(self.classifier, X, Y, cv=10,n_jobs=-1)
        result ="punteggio del classificatore: " + scores['test_score'].mean()
        return result
    
    # method that retur if the classifier is ready or not
    def classifier_is_ready(self):
        return self.ready