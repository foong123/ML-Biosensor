import numpy as np
import pandas as pd
import os, os.path
import csv

DIR = 'D:/unmc degree/year 4/fyp/[GTi] Specificity_dev/after_detection/'
dirListing = os.listdir(DIR)
#print(len(dirListing))
header_flag = 1
L = 1

for a in range(len(dirListing)):
    
    file_name = dirListing[a]
    excel_file = DIR + file_name
    print(file_name)
    wb = pd.ExcelFile(excel_file)

    worksheet_name_list = wb.sheet_names
    print(worksheet_name_list)

    for b in range(len(worksheet_name_list)):

        data = pd.read_excel(excel_file, sheet_name = b )

        frequencies = data['Frequency (Hz)'].values
        #print(frequencies)
        #print(type(frequencies))

        x_axis = data["Z' (Ω)"].values
        #print(x_axis)
        #print(type(x_axis))

        y_axis = data["-Z'' (Ω)"].values
        #print(y_axis)
        #print(type(y_axis))

        Z = x_axis + 1j*y_axis
        #print(Z)

        phase = data['-Phase (°)'].values
        #print(phase)

        csv_row = []
        csv_header = []

        counter = 0
        for k in np.arange(0,40,1):

            csv_row.append(x_axis[k])
            csv_header.append(frequencies[counter])
            counter = counter + 1

        counter = 0
        for i in np.arange(0,40,1):
            csv_row.append(y_axis[i])
            csv_header.append(frequencies[counter])
            counter = counter + 1

        csv_header.insert(0, "ID")
        csv_header.append("label")
        #print(csv_header)

        csv_row.insert(0, L)
        file_name = file_name.strip('.xlsx')
        label = file_name + "_" + worksheet_name_list[b]
        csv_row.append(label)

        csvfile = "D:/unmc degree/year 4/fyp/[GTi] Specificity_dev/compile/after_detect.csv"
        with open(csvfile, "a+",newline='') as fp:
            wr = csv.writer(fp, dialect='excel')

            if header_flag == 1:

                wr.writerow(csv_header)
                header_flag = header_flag + 1

            wr.writerow(csv_row)

        L = L + 1
