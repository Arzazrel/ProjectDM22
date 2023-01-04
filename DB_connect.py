# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:42:45 2023

@author: Alex

explanation: file containing the class that manage the connection and the operation with mysql DB
"""
import mysql.connector as connector
import os
import pandas as pd

class DB_connect:
    # constructor
    def __init__(self):
        # var that will contain the connection to DB
        self.connection = None
        # dictionary that contain the value for the connection to DB mysql 
        self.parameter_conn = {}
        
    # set the parameter for the connection to DB mysql
    def set_parameter_conn(self, user, password, host, database):
        # parameter are : user, password, host, database
        self.parameter_conn['user'] = user
        self.parameter_conn['password'] = password
        self.parameter_conn['host'] = host
        self.parameter_conn['database'] = database
        
    # method to open connection
    def open_connect(self):
        # check if dictionary isn't empty
        if len(self.parameter_conn) != 0:
            try:
                self.connection = connector.connect(user=self.parameter_conn['user'], password=self.parameter_conn['password'],host=self.parameter_conn['host'],database=self.parameter_conn['database'])
            except connector.Error as err:
                if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
    
    # method to close connection
    def close_connect(self):
        # check if there is a connection
        if self.connection.is_connected():
            # close connection
            self.connection.close()
        
    """ -- method used in development to populate the DB --
    # method that add celestial bodies to DB mysql from a file csv, path passed by parameter 
    def from_csv_to_DB(self, path):
        # check the path
        if not os.path.exists(path):   # check if a directory already exists...
            return "file specificato non esistente"
        # read csv file
        df = pd.read_csv(path)
        # preprocessing
        # remove useless column
        dfProc0 = df.drop(columns=['obj_ID','run_ID', 'rerun_ID','cam_col','field_ID','spec_obj_ID','plate','MJD','fiber_ID'])
        # remove redshift column
        dfReduced = dfProc0.drop(columns=['redshift'])
        # remove incorrect sample in position 79545 with values [224.00652611366,-0.624303881323656,-9999,-9999,18.1656,18.01675,-9999,"STAR"] 
        df_preprocessed = dfReduced.drop([79543])
        
        # open cursor
        cursor = self.connection.cursor()
        # insert data
        db_row = df_preprocessed.shape[0]
        for i in range(db_row):
            add_celestial_bodies = ("INSERT INTO celestial_bodies (alpha, delta, u, g, r, i, z, class, observer_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            
            data_celestial_bodies = (df_preprocessed.iloc[i,0],df_preprocessed.iloc[i,1],df_preprocessed.iloc[i,2],df_preprocessed.iloc[i,3],df_preprocessed.iloc[i,4],df_preprocessed.iloc[i,5],df_preprocessed.iloc[i,6],df_preprocessed.iloc[i,7],1)
            # execute insert
            cursor.execute(add_celestial_bodies, data_celestial_bodies)
            
        # Make sure data is committed to the database
        self.connection.commit()
        # close cursor
        cursor.close()
    """
        
#file_path = os.path.join(out_dir,'prova.csv') # Join one or more path components intelligently
file_path = 'dataset\star_classification.csv'
# test di prova
c = DB_connect()
c.set_parameter_conn('Alex', '', '127.0.0.1', 'dm_project_db')
c.open_connect()
#c.from_csv_to_DB(file_path)
c.close_connect()