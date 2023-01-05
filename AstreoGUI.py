# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
from tkinter import *
from threading import Thread
from threading import Semaphore
# import of my files
import Classifier as Clf
import DB_connect as DB_conn

# global values
window = Tk()
status = {'state' : 'initial' }        #indicate the view to be displayed by the application
    #the different status are:
        # - initial : initial login or signin view
        # - user_view : user view
        # - add_view : view for add new celestial bodies, in this view the evaluator uses machine learning classifier
user_info = {}  # dictionary contain the user info such as username, userid, admin...
# var that contain the object of the classifier
clf = Clf.Classifier()
# semaphore for work with classifier
clf_semaphore = Semaphore(1)
# object for the comunication to the DB
conn = DB_conn.DB_connect()
# parameter for connection to DB
parameter_conn = {}
parameter_conn['user'] = 'Alex'
parameter_conn['password'] = ''
parameter_conn['host'] = '127.0.0.1'
parameter_conn['database'] = 'dm_project_db'
# -- variable text for label in GUI
# text that shows the class of the new object classified by classifier
classify_text = StringVar()
classify_text.set(':')
# text that shows the error that occour in the initial view
error_text_initial_view = StringVar()
error_text_initial_view.set('')
# text that shows the error that occour in the add view
error_text_add_view = StringVar()
error_text_add_view.set('')

# methods
# method that cleans GUI elements
def cleanGUI():
    list = window.grid_slaves()
    for l in list:
        l.destroy()
# method for handling the closing of the window by the user
def on_closing():
    # close connection if is open
    if conn.is_conn():
        conn.close_connect()
    # close window
    window.destroy()

# method that cleans GUI elements in a frame passeb by parameter
def clean_frame_GUI(frame_elem):
    list = frame_elem.grid_slaves()
    for l in list:
        l.destroy()
        
# method executed when the signin button is clicked
def btn_signin_clicked(username, psw):
    #check input
    if username and psw:
        print("username: ", username, " psw: ", psw)
        # send username and psw to server
        
        # checks passed 
        # save username
        user_info['username'] = username
        
        # update the error mex
        error_text_initial_view.set("")
        # update the state
        status['state'] = "user_view"
        current_view_to_visualise()
    else:
        # set error text
        error_text_initial_view.set("Invalid username or psw, please try again.")
    
# method executed when the login button is clicked
def btn_login_clicked(username, psw):
    #check input
    if username and psw:
        print("username: ", username, " psw: ", psw)
        # send username and psw to server
        
        # checks passed 
        # save username
        user_info['username'] = username
        
        # update the error mex
        error_text_initial_view.set("")
        #update the state
        status['state'] = "user_view"
        current_view_to_visualise()
    else:
        # set error text
        error_text_initial_view.set("Invalid username or psw, please try again.")
    
# --- methods for change view
# method for coming back to login/signin view, when the logout button is clicked
def btn_logout_clicked():
    #update the state
    status['state'] = "initial"
    current_view_to_visualise()
    
# method for goes to add_view
def btn_add_view():
    #update the state
    status['state'] = "add_view"
    current_view_to_visualise()
    
# method for goes to user_view
def btn_user_view():
    #update the state
    status['state'] = "user_view"
    current_view_to_visualise()
    
# method executed for change the view visualised
def current_view_to_visualise():
    #print("eseguo current, status è : ",status)
    cleanGUI()
    if status['state'] == "initial":
        # create variable for the GUI elements
        explainText = "Welcome to Astreo.\nIf you are already logged in, enter your username and password and press the login button.\nIf you have yet to register, enter your username and password and then press the signin button."
    
        # create the GUI elements and place them 
        # - frame top
        top_frame = Frame(window, width=580, height=180, bg='grey')
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        top_frame.grid_propagate(False)
        
        explainTextLabel = Label(top_frame, text=explainText)
        explainTextLabel.grid(row=0, column=0, sticky="W", padx=10, pady=10)
        
        # - middle frame
        middle_frame = Frame(window, width=580, height=180, bg='grey')
        middle_frame.grid(row=1, column=0, padx=10, pady=10)
        
        userNameLabel = Label(middle_frame,text="Username: ")
        userNameLabel.grid(row=1, column=1, sticky="N", padx=20, pady=10)
    
        userNameInput = Entry(middle_frame)
        userNameInput.grid(row=1, column=2, sticky="WE", padx=10)
    
        userPswLabel = Label(middle_frame,text="Username: ")
        userPswLabel.grid(row=2, column=1, sticky="N", padx=20, pady=10)
    
        userPswInput = Entry(middle_frame, show="*")
        userPswInput.grid(row=2, column=2, sticky="WE", padx=10)
    
        # buttons to login/sign in
        btn_start = Button(middle_frame, text="Sign in", command=lambda: btn_signin_clicked(userNameInput.get(),userPswInput.get()))
        btn_start.grid(row=3, column=1)
    
        btn_test = Button(middle_frame, text="Login", command=lambda: btn_login_clicked(userNameInput.get(),userPswInput.get()))
        btn_test.grid(row=3,column=2)
        
        # - bottom frame in the login/signin view : contain the error text if occour an error
        bottom_frame_LS = Frame(window, width=580, height=180, bg='grey')
        bottom_frame_LS.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        bottom_frame_LS.grid_propagate(False)
        
        error_label_initial_view = Label(bottom_frame_LS, textvariable=error_text_initial_view, bg='grey')
        error_label_initial_view.grid(row=0, column=0, padx=10, pady=10)
        
    elif status['state'] == "user_view":
        # create variable for the GUI elements
        if user_info.get('username') != None:
            username = user_info.get('username')
        else:
            username = "Unknown"
        # create the GUI elements and place them 
        # - top bar frame : contain username of the logged user and the logout button
        top_bar_frame = Frame(window, width=580, height=40, bg='grey')
        top_bar_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")
        top_bar_frame.grid_propagate(False)
        # username label
        username_label = Label(top_bar_frame, text=username)
        username_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)
        # button
        btn_logout = Button(top_bar_frame, text="Logout", command=btn_logout_clicked)
        btn_logout.grid(row=0, column=1, sticky='e',padx=5, pady=10)
        btn_logout.pack(side = RIGHT)
        
        # - middle frame : contain buttons to add and display celestial bodies in the DB
        middle_frame = Frame(window, width=580, height=80, bg='grey')
        middle_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        middle_frame.grid_propagate(False)
        
        # buttons
        btn_vis_global = Button(middle_frame, text="Visualise global list of celestial bodies", command=btn_logout_clicked)
        btn_vis_global.grid(row=1, column=0)
        
        btn_add = Button(middle_frame, text="Add celestial body", command=btn_add_view)
        btn_add.grid(row=0, column=1)
        
        btn_vis_own = Button(middle_frame, text="visualise own list of celestial bodies", command=btn_logout_clicked)
        btn_vis_own.grid(row=1, column=2)
        
        # - table frame : contain the list of celestial bodies
        table_frame = Frame(window, width=580, height=460, bg='grey')
        table_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_propagate(False)
        
    elif status['state'] == "add_view":
        # create variable for the GUI elements
        explainText = "In this screen you can add celestial bodies that you have observed.\nPut the parameters in the corresponding fields.\nPress the classification button to get a prediction of the type of celestial body observed: GALAXY, STAR, QSO.\nPress the add button to save."
        # create the GUI elements and place them 
        # - top frame : contain explain text
        top_frame = Frame(window, width=580, height=85, bg='grey')
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        top_frame.grid_propagate(False)
        # label for the explain text
        explain_text_label = Label(top_frame, text=explainText)
        explain_text_label.grid(row=0, column=0, sticky="W", padx=0, pady=10)
        
        # - frame for the input field for the celestial body features
        features_input_frame = Frame(window, width=580, height=405, bg='grey')
        features_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        features_input_frame.grid_propagate(False)
        # Right Ascension angle : [0 , 360]
        right_ascension_label = Label(features_input_frame,text="Right Ascension angle: ")
        right_ascension_label.grid(row=0, column=0, sticky="N", padx=10, pady=10)
    
        right_ascension_input = Entry(features_input_frame)
        right_ascension_input.grid(row=0, column=1, sticky="WE", padx=10)
        # Declination angle : [-90 , 90]
        declination_angle_label = Label(features_input_frame,text="Declination angle: ")
        declination_angle_label.grid(row=0, column=2, sticky="N", padx=10, pady=10)
    
        declination_angle_input = Entry(features_input_frame)
        declination_angle_input.grid(row=0, column=3, sticky="WE", padx=10)
        # u = Ultraviolet filter in the photometric system
        u_label = Label(features_input_frame,text="Ultraviolet filter: ")
        u_label.grid(row=1, column=0, sticky="N", padx=10, pady=10)
    
        u_input = Entry(features_input_frame)
        u_input.grid(row=1, column=1, sticky="WE", padx=10)
        # g = Green filter in the photometric system
        g_label = Label(features_input_frame,text="Green filter: ")
        g_label.grid(row=2, column=0, sticky="N", padx=10, pady=10)
    
        g_input = Entry(features_input_frame)
        g_input.grid(row=2, column=1, sticky="WE", padx=10)
        # r = Red filter in the photometric system
        r_label = Label(features_input_frame,text="Red filter: ")
        r_label.grid(row=3, column=0, sticky="N", padx=10, pady=10)
    
        r_input = Entry(features_input_frame)
        r_input.grid(row=3, column=1, sticky="WE", padx=10)
        # i = Near Infrared filter in the photometric system
        i_label = Label(features_input_frame,text="Near Infrared filter: ")
        i_label.grid(row=4, column=0, sticky="N", padx=10, pady=10)
    
        i_input = Entry(features_input_frame)
        i_input.grid(row=4, column=1, sticky="WE", padx=10)
        # z = Infrared filter in the photometric system
        z_label = Label(features_input_frame,text="Infrared filter: ")
        z_label.grid(row=5, column=0, sticky="N", padx=10, pady=10)
    
        z_input = Entry(features_input_frame)
        z_input.grid(row=5, column=1, sticky="WE", padx=10)
        
        # empty labels for formatting
        empty_0 = Label(features_input_frame, text='', bg='grey')
        empty_0.grid(row=6, column=0)
        empty_1 = Label(features_input_frame, text='', bg='grey')
        empty_1.grid(row=7, column=0)
        empty_2 = Label(features_input_frame, text='', bg='grey')
        empty_2.grid(row=8, column=0)
        
        # botton to classify the celestial body by classifier (Random Forest)
        btn_classify = Button(features_input_frame, text="Classify", command=lambda: btn_check_classify(right_ascension_input.get(), declination_angle_input.get(), u_input.get(), g_input.get(), r_input.get(), i_input.get(), z_input.get()))
        btn_classify.grid(row=9, column=0)
        # label for the result of classifier
        result_classifier_label = Label(features_input_frame, textvariable=classify_text)
        result_classifier_label.grid(row=9, column=1, sticky="W", padx=0, pady=5)
        # botton to add the celestial body to DB
        btn_add_CB = Button(features_input_frame, text="Add", command=btn_logout_clicked)
        btn_add_CB.grid(row=10, column=3)
        # botton to return back to user view
        btn_userview = Button(features_input_frame, text="Back", command=btn_user_view)
        btn_userview.grid(row=11, column=3)
        
        # - frame to visualize error mex in add view
        error_frame_add_view = Frame(window, width=580, height=60, bg='grey')
        error_frame_add_view.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        error_frame_add_view.grid_propagate(False)
        
        error_label_add_view = Label(error_frame_add_view, textvariable=error_text_add_view, bg='grey')
        error_label_add_view.grid(row=0, column=0, padx=10, pady=10)
        
# ------------------------------------ methods for classifier ------------------------------------
# method for make and fit the classifier in background
def make_classifier():
    # acquire token
    clf_semaphore.acquire()
    clf.preprocess_ds()
    clf.train_model()
    # release token
    clf_semaphore.release(1)
    print("Classificatore trained")
    
# method for checking the input data of the new celestial body
def btn_check_classify(alpha, delta, u, g, r, i, z):
    # check input
    if alpha and delta and u and g and r and i and z:
        # convert the values
        try:
            alpha = float(alpha)
            delta = float(delta)
            u = float(u)
            g = float(g)
            r = float(r)
            i = float(i)
            z = float(z)
        except ValueError:
            # set error text
            error_text_add_view.set("Invalid values entered, please try again.")
            return 
        # check alpha -> Right Ascension angle : [0 , 360]
        if alpha < 0 or alpha > 360:
            # error mex
            error_text_add_view.set("Invalid value for Right Ascension angle. it must be between 0 and 360°.")
            return
        # check delta -> Declination angle : [-90 , 90]
        if delta < -90 or delta > 90:
            # error mex
            error_text_add_view.set("Invalid value for Declination angle. it must be between -90 and 90°.")
            return
        
        # all check passed, call prediction
        new_object = [[alpha,delta,u,g,r,i,z],]
        # one thread perform the predict in background for avoiding that the main thread remains locked 
        # while waiting for the classifier to be trained or ready
        t_predict = Thread(target=classify_new_obj,args=(new_object,))
        t_predict.start()
    else:
        # set error text
        error_text_add_view.set("Some values are missing, please enter all values.")
    
# method that classify the new object passed as parameter and write the classes in the view
def classify_new_obj(new_obj):
    # text to visualize to notify the work
    classify_text.set(": Working...")
    
    # acquire token
    clf_semaphore.acquire()
    # check if classifier is ready for classify
    if clf.classifier_is_ready():
        # update classify_label text
        classify_text.set(": " + clf.predict(new_obj))
    else:
        # set error text
        error_text_add_view.set("Classifier does not work, please try closing and reopening the program.")
    # release token
    clf_semaphore.release(1)

# ------------------------------------ main ------------------------------------        
if __name__ == "__main__":
    window.title("Astreo")
    window.geometry('600x600')
    window.resizable(False, False)
    # window.configure(background="white")
    
    current_view_to_visualise()
    # at the start one thread make and fit the classifier in background
    t = Thread(target=make_classifier)
    t.start()
    
    # at the start open the connection to DB
    conn.set_parameter_conn(parameter_conn['user'], parameter_conn['password'], parameter_conn['host'] , parameter_conn['database'])
    
        #window.update_idletasks()
        #window.update()
    # handle the window closing by the user
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()