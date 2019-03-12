import numpy as np
import mne
import os 
dir_path = os.getcwd()
# Read the CSV file as a NumPy array
data = np.loadtxt(dir_path+'/tmp/edf.csv', delimiter=',')

# Some information about the channels
ch_names = ['CH 1', 'CH 2', 'CH 3']  # TODO: finish this list

# Sampling rate of the Nautilus machine
sfreq = 500  # Hz

# Create the info structure needed by MNE
info = mne.create_info(ch_names, sfreq)

# Finally, create the Raw object
raw = mne.io.RawArray(data, info)

# Plot it!
raw.plot()