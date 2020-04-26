import numpy as np
import pandas as pd

data = pd.read_csv('EIS.csv')
#print(data)

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

circuit = Randles(initial_guess=[.01, .005, .5, .9, 200, 0.01], CPE=True)
#circuit = 'R0-p(R1,E1)-W1'
#initial_guess = [.01, .005, .1, .9,200, 0.01]

#circuit = CustomCircuit(circuit, initial_guess=initial_guess)

circuit.fit(frequencies, Z)
#To print model details
print(circuit)

#Randles circuit parameters
Randles_param = circuit.get_param_names()
#print(Randles_param)

#check type
#print(type(Randles_param))

#Randles circuit values of the parameters
Randles_param_values = circuit.parameters_
#print(Randles_param_values)
#print(Randles_param_values.size)

Randles_values = circuit.parameters_
print(Randles_values)

Z_fit = circuit.predict(frequencies)

import matplotlib.pyplot as plt
from impedance.plotting import plot_nyquist
fig, ax = plt.subplots()
plot_nyquist(ax, frequencies, Z, fmt='o')
plot_nyquist(ax, frequencies, Z_fit, fmt='-')
plt.legend(['Data', 'Fit'])
plt.show()

#Save the model
#model_io.model_export(circuit, 'template_model.json')

#To import the model
#loaded_template = model_io.model_import('template_model.json')

#print("Loaded Template")
#print(loaded_template)