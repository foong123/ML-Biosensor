import numpy as np
import pandas as pd
import os, os.path
import matplotlib.pyplot as plt 

DIR = "D:/unmc degree/year 4/fyp/[GTi] Specificity_dev/after_detection/"
# DIR = "D:/unmc degree/year 4/fyp/[GTi] IgG concentration_sensitivity (calibration)_dev/[GTi] IgG concentration_sensitivity (calibration)/no_igg_excel/"
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
    #print(worksheet_name_list)

    for b in range(len(worksheet_name_list)):

        print(L)
        data = pd.read_excel(excel_file, sheet_name = b )

        frequencies = data['Frequency (Hz)'].values
        #print(frequencies)

        x_axis = data["Z' (Ω)"].values
        #print(x_axis)

        y_axis = -1 * data["-Z'' (Ω)"].values
        #print(y_axis)

        Z = x_axis + 1j*y_axis
        #print(Z)

        phase = data['-Phase (°)'].values
        #print(phase)

        # keep only the impedance data in the first quandrant
        frequencies = frequencies[np.imag(Z) < 0]
        Z = Z[np.imag(Z) < 0]

        from impedance.circuits import Randles, CustomCircuit
        import impedance.model_io as model_io
        from impedance.plotting import plot_nyquist

        circuit = Randles(initial_guess=[.01, .005, .5, .9, 200, 0.01], CPE=True)
        #circuit = 'R0-p(R1-A1,E1)'
        #initial_guess = [100, 1000, .01, 0.01,1]

        #circuit = CustomCircuit(circuit, initial_guess=initial_guess)

        circuit.fit(frequencies, Z)
        #To print model details
        #print(circuit)

        #Randles circuit parameters
        Randles_param = circuit.get_param_names()
        #print(Randles_param)

        #check type
        #print(type(Randles_param))

        #Randles circuit values of the parameters
        Randles_param_values = circuit.parameters_
        #print(Randles_param_values)
        #print(Randles_param_values.size)

        Randles_circuit = []
        csv_header = []
        csvrow = []

        i = 0 
        for k in Randles_param[0]:

            string_concat = "%s: %s" %(k, Randles_param_values[i])
            csv_header.append(k)
            #print(Randles_param_values[i])
            #print(k)
            csvrow.append(Randles_param_values[i])
            #Randles_circuit.append(string_concat) 
            i = i + 1

            #f_pred = np.logspace(5,-2)
            #randlesCPE_fit = circuit.predict(f_pred)
            #fig, ax = plt.subplots(figsize=(5,5))
            #plot_nyquist(ax, frequencies, Z)
            #plot_nyquist(ax, f_pred, randlesCPE_fit, fmt='-')
            #plt.show()

        #print(Randles_circuit)

        #write to a csv file
        import csv
        csv_header.insert(0, "ID")
        csv_header.append("label")

        csvrow.insert(0, L)
        file_name = file_name.strip('.xlsx')
        label = file_name + "_" + worksheet_name_list[b]
        csvrow.append(label)

        csvfile = "D:/unmc degree/year 4/fyp/[GTi] Specificity_dev/compile/compile_after.csv"
        #csvfile = "D:/unmc degree/year 4/fyp/[GTi] IgG concentration_sensitivity (calibration)_dev/[GTi] IgG concentration_sensitivity (calibration)/no_igg_excel/compile.csv"
        with open(csvfile, "a+",newline='') as fp:
            wr = csv.writer(fp, dialect='excel')

            if header_flag == 1:

                wr.writerow(csv_header)
                header_flag = header_flag + 1

            wr.writerow(csvrow)

        L = L + 1
