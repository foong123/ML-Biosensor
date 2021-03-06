import time
import sys
import os
import PIL.Image
import random
import os
sys.path.insert(1, '/home/pi/Desktop/fyp/project/panadol_prediction/')
sys.path.insert(1, '/home/pi/Desktop/fyp/project/dengue_detection/')
from demo_ann_Panadol import Thread1, Regression
from demo_ann_Dengue import Thread2, NN_Model
from demo_svm_Panadol import Thread3
from demo_svm_Dengue import Thread4
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import ttk
from tkinter import *

currentDirectory = os.getcwd()
window = Tk()
window.iconphoto(False, PhotoImage(file = '/home/pi/Desktop/fyp/project/GUI/GUI_Image/biosensor_icon.png'))

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

    #Center window
    window.resizable(False, False)  # This code helps to disable windows from resizing

    #window size
    window_height = 250
    window_width = 460
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    #window title
    window.title("FYP")

    #Random window background color
    red = random.randint(0,255)
    green = random.randint(0,255)
    blue = random.randint(0,255)
    color = '#{:02x}{:02x}{:02x}'.format(red,green,blue)
    window.configure(bg = color)

    #Welcome image
    img = PIL.Image.open("/home/pi/Desktop/fyp/project/GUI/GUI_Image/welcome.png")
    img = img.resize((170, 160), PIL.Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(window, image=img)
    panel.image = img
    panel.config(anchor = CENTER)
    panel.pack()

    #Panadol concentration estimation button
    Panadol_btn = Button(window, text="Panadol concentration estimation", command = Panadol_task)
    Panadol_btn.place(x=10, y=170)

    #Dengue detection button
    Dengue_btn = Button(window, text="Dengue detection", command = Dengue_task)
    Dengue_btn.place(x=310, y=170)

    #About button
    About_btn = Button(window, text="About", command = About_button_clicked)
    About_btn.place(x=310, y=210)

#About page
def About_page():

    window.title("FYP - About")
    window.geometry("550x430")

    #About_title
    About_title = Label(window, text="About", font=("Arial Bold", 20))
    About_title.config(anchor = CENTER)
    About_title.pack()
    #Description
    About_Description = Label(window,
                            text="A simple GUI for ML based post analysis. This is part of the final year project.Created by Foong Pak Chuen, MEng. Electrical and Electronic Engineering Student",
                            font=("Arial Bold", 12),
                            wraplength=500)
    About_Description.place(x=0, y=50)

    #Logo
    img = PIL.Image.open("/home/pi/Desktop/fyp/project/GUI/GUI_Image/UNMC_logo.png")
    img = img.resize((450, 250), PIL.Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(window, image=img)
    panel.image = img
    panel.place(x=50, y=150)

    #Back button
    Back_btn = Button(window, text="Back", command = Return_Home)
    Back_btn.place(x=0, y=10)

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
    window.geometry("500x130")

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

    #Title
    title = Label(window, text="{} Detection - Tutorial".format(title), font=("Arial Bold", 20))
    title.config(anchor = CENTER)
    title.pack()

    window.title("FYP - {} Detection - Tutorial".format(title))
    window.geometry("700x250")

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

    window.title("FYP - {} Detection - Select Test File".format(title))
    window.geometry("600x300")

    #Browse Button
    Browse_button = Button(window, text = "Browse A File", command = fileDialog)
    Browse_button.place(x=0, y=100)

    #Back Button
    Back_button = Button(window, text="Back", command = Task_Back_button_clicked)
    Back_button.place(x=300, y=200)

    #Description
    Description_1 = Label(window, text="Select a {} sensor file to estimate the Panadol Concentration".format(file), font=("Arial Bold", 10))
    Description_1.place(x=0, y=60)

#Result page
def Result_Page():

    global saved_result

    #Title
    title = Label(window, text="Result", font=("Arial Bold", 15))
    title.config(anchor = CENTER)
    title.pack()

    if task == 1:
        title = "Panadol"
        file = "DPV"
        result = open("/home/pi/Desktop/fyp/project/GUI/ML_results/Panadol_results/Panadol_result.txt", "r")

    elif task == 2:
        title = "Dengue"
        file = "EIS"
        result = open("/home/pi/Desktop/fyp/project/GUI/ML_results/Dengue_results/Dengue_result.txt", "r")

    window.title("FYP - {} Result".format(title))
    window.geometry("400x400")

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
    root.resizable(False, False)
    window_height = 100
    window_width  = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width/2) - (window_width/2))
    y_coordinate = int((screen_height/2) -(window_height/2))

    root.geometry("{}x{}+{}+{}".format(window_width,window_height,x_coordinate,y_coordinate))


    root.title("Loading")
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
