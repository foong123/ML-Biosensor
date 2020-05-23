from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import time
import sys
import tkinter as tk

sys.path.insert(1, '/home/pi/Desktop/fyp/project/panadol_prediction/')
sys.path.insert(1, '/home/pi/Desktop/fyp/project/dengue_detection/')
from demo_ann_Panadol import Thread1, Regression
from demo_ann_Dengue import Thread2, NN_Model
from demo_svm_Panadol import Thread3
from demo_svm_Dengue import Thread4
import os

currentDirectory = os.getcwd()
window = Tk()
#window.iconphoto(False, tk.PhotoImage(file = '/home/pi/Desktop/fyp/project/GUI/GUI_images/biosensor_icon.png'))

#Utilities functions
def all_children(window):
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

#Main/Home page
def Home_page():

    global window
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    window.title("FYP")
    #Window size
    window.geometry('500x200')      #Window size

    #Title 
    Title = Label(window, text="Welcome!", font=("Arial Bold", 30))
    Title.config(anchor = CENTER)
    Title.pack()
    #Panadol concentration estimation button
    Panadol_btn = Button(window, text="Panadol concentration estimation", command = Panadol_task)
    Panadol_btn.place(x=10, y=100)

    #Dengue detection button
    Dengue_btn = Button(window, text="Dengue detection", command = Dengue_task)
    Dengue_btn.place(x=310, y=100)

    #About button
    About_btn = Button(window, text="About", command = About_button_clicked)
    About_btn.place(x=410, y=150)

#About page
def About_page():

    #window = Tk()
    window.title("FYP - About")
    #Window size
    window.geometry('400x200')      #Window size
    #About_title
    About_title = Label(window, text="About", font=("Arial Bold", 20))
    About_title.config(anchor = CENTER)
    About_title.pack()
    #Description 
    About_Description = Label(window, text="A simple UI for ML based post analysis",font=("Arial Bold", 12))
    About_Description.place(x=0, y=50)

    #Back button
    Back_btn = Button(window, text="Back", command = Return_Home)
    Back_btn.place(x=150, y=150)

#Task Descripton page
def Task_description_page(): 

    global task 
    if task == 1:

        title = "Panadol"
        text = "Welcome to Panadol Concentration Estimator" 

    elif task == 2:

        title = "Dengue"
        text = "Welcome to Dengue Detector" 

    #window = Tk()
    window.title("FYP - {}".format(title))
    #Window size
    window.geometry('500x150')      #Window size
    #Description 
    Description_1 = Label(window, text=text,font=("Arial Bold", 12))
    Description_1.place(x=0, y=30)

    #Description 
    Description_1 = Label(window, text="Click on the tutorial to see how to use it",font=("Arial Bold", 12))
    Description_1.place(x=0, y=60)

    #Tutorial button
    Tutorial_btn = Button(window, text="Tutorial", command = Tutorial_button_clicked)
    Tutorial_btn.place(x=0, y=100)

    #Check button
    Back_btn = Button(window, text="Start", command = Start_button_clicked)
    Back_btn.place(x=300, y=100)

    #Back button
    Back_btn = Button(window, text="Back", command = Return_Home)
    Back_btn.place(x=400, y=100)

#Tutorial page
def Tutorial_Page():

    global task

    if task == 1:

        title = "Panadol"
        file = "DPV"
        file_dimension = "120"

    elif task == 2:

        title = "Dengue"
        file = "EIS"
        file_dimension = "6"

    #Window size
    window.geometry('700x250')      #Window size

    #Title
    title = Label(window, text="{} Detection - Tutorial".format(title), font=("Arial Bold", 20))
    title.config(anchor = CENTER)
    title.pack()

    window.title("FYP - {} Detection - Tutorial".format(title))    

    Description_1 = Label(window, text="1) Click Start and insert the {} sensor file.".format(file), font=("Arial Bold", 10))
    Description_1.place(x=0, y=40)

    Description_2 = Label(window, text="2) Find the location of {} sensor file that wanted to be tested".format(file), font=("Arial Bold", 10))
    Description_2.place(x=0, y=60)

    Description_3 = Label(window, text="3) The {} sensor file should be in .csv format".format(file), font=("Arial Bold", 10))
    Description_3.place(x=0, y=80)

    Description_4 = Label(window, text="4) Make sure the sensor file has {} columns (dimensions)".format(file_dimension), font=("Arial Bold", 10))
    Description_4.place(x=0, y=100)

    Description_5 = Label(window, text="5) Once inserted the file click Check! ", font=("Arial Bold", 10))
    Description_5.place(x=0, y=120)

    Description_6 = Label(window, text="6) Wait for a few seconds and the results will prompt out", font=("Arial Bold", 10))
    Description_6.place(x=0, y=140)

    #Back button
    Back_btn = Button(window, text="Back", command = Task_Back_button_clicked)
    Back_btn.place(x=300, y=200)

#Browse File page
def Browse_File_Page():

    global task
    #Title
    title = Label(window, text="Select File", font=("Arial Bold", 15))
    title.place(x=0, y=10)  
    if task == 1:
        title = "Panadol"
        file = "DPV"

    elif task == 2:
        title = "Dengue"
        file = "EIS"
    
    #Browse Button
    Browse_button = Button(window, text = "Browse A File", command = fileDialog)
    Browse_button.place(x=0, y=100)

    #Back Button
    Back_button = Button(window, text="Back", command = Task_Back_button_clicked)
    Back_button.place(x=300, y=200)

    window.title("FYP - {} Detection - Select Test File".format(title))
    #Window size
    window.geometry('600x300')      #Window size
    #Description
    Description_1 = Label(window, text="Select a {} sensor file to estimate the Panadol Concentration".format(file), font=("Arial Bold", 10))
    Description_1.place(x=0, y=60)

#Result page
def Result_Page():

    global saved_result

    #Title
    title = Label(window, text="Result", font=("Arial Bold", 15))
    title.place(x=0, y=10)
    if task == 1:
        title = "Panadol"
        file = "DPV"
        print ("haha")
        result = open("/home/pi/Desktop/fyp/project/GUI/ML_results/Panadol_results/Panadol_result.txt", "r")
        print ("hahaha")

    elif task == 2:
        title = "Dengue"
        file = "EIS"
        result = open("/home/pi/Desktop/fyp/project/GUI/ML_results/Dengue_results/Dengue_result.txt", "r")

    window.title("FYP - {} Result".format(title))
    #Window size
    window.geometry('400x400')      #Window size

    #Print Results from text file
    a = result.read()
    Results_label = Label(window, text=a, font=("Arial Bold", 10), wraplength = 350)
    Results_label.place(x=0, y=50)
    #Return Home Button
    Return_Home_button = Button(window, text = "Return Home", command = Return_Home)
    Return_Home_button.place(x=0, y=350)

    #Save Results Button
    Save_Results_button = Button(window, text = "Save Result", command = Save_Result)
    Save_Results_button.place(x=150, y=350)

    #Rerun Button
    Back_button = Button(window, text="Rerun", command = Start_button_clicked)
    Back_button.place(x=300, y=350)

    saved_result = a

#Buttons
#Open About page
def About_button_clicked():
    global window
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    About_page()

#Open Panadol task page
def Panadol_task():
    global window, task
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    task = 1
    Task_description_page()

#Open Dengue task page
def Dengue_task():
    global window, task
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    task = 2
    Task_description_page()

#Return home
def Return_Home():
    global window
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    Home_page()

#Open Tutorial page
def Tutorial_button_clicked():
    global window
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    Tutorial_Page()

#Return to task page
def Task_Back_button_clicked():

    global window
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    Task_description_page()

#Open Browse file page
def Start_button_clicked():

    global window
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    Browse_File_Page()

#Open file dialog to select file
def fileDialog():

    global input_filename
    filename =  filedialog.askopenfilename(initialdir = currentDirectory,title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    #print(filename) #debug line
    text = 'Selected file: ' + filename
    #Description
    Description_1 = Label(window, text=text, font=("Arial Bold", 10))
    Description_1.place(x=0, y=140)
    input_filename = filename

    if input_filename != "":
        #print(filename) #debug line
        #Back button
        if task == 1:
            Check_btn = Button(window, text="Check", command = Run_ML)

        elif task == 2:
            Check_btn = Button(window, text="Check", command = Run_ML)

        Check_btn.place(x=100, y=200)
    else:

        Description_1 = Label(window, text="No selected file", font=("Arial Bold", 10))
        Description_1.place(x=0, y=140)

#Run the checker and open result page
def Run_ML():
    global task,input_filename
    root = Tk()
    progcomp = ttk.Progressbar(root, orient='horizontal', length=200, mode = 'determinate', maximum=100)
    progcomp.grid()
    if task == 1:
        check = Thread1(progcomp,input_filename)
        #check = Thread3(progcomp, input_filename)    #for svm
        check.start()

    elif task == 2:
        check = Thread2(progcomp,input_filename)
        #check = Thread4(progcomp,input_filaname)    #for svm
        check.start()

    root.mainloop()
    root.destroy()
    widget_list = all_children(window)
    for item in widget_list:
        item.destroy()

    Result_Page()

def Save_Result():

    if task == 1:
        f = open("/home/pi/Desktop/fyp/project/GUI/Saved_results/Panadol/saved_result.txt", "a+")

    elif task == 2:
        f = open("/home/pi/Desktop/fyp/project/GUI/Saved_results/Dengue/saved_result.txt", "a+")

    f.write("\n")
    f.write(saved_result)
    f.write("\n")

    Saved_text = Label(window, text="Saved", font=("Arial Bold", 10))
    Saved_text.place(x=150, y=300)

Home_page()

window.mainloop()
