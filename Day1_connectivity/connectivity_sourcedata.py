#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 11:45:40 2025

@author: liuzzil2
"""

import numpy as np
import matplotlib.pyplot as plt
import mne
from mne_connectivity import spectral_connectivity_epochs
from mne_connectivity import envelope_correlation

#%%
data = np.load('/Users/liuzzil2/OneDrive - National Institutes of Health/MEG_course/ADV_WORKSHOP/sub-ON02811.npy')
fs = 600
tsamp = data.shape[2]
t = (tsamp-1)/fs
time = np.linspace(0, t, tsamp, endpoint=False)

l_freq = 13
h_freq = 30
filtered_data = mne.filter.filter_data(data, fs, l_freq, h_freq)

n_del = int(fs/4)
timekeep = np.ones(time.shape)
timekeep[0:n_del] = 0
timekeep[-n_del:len(time)] = 0
timef = time[timekeep==1]

filtered_data = filtered_data[:,:,timekeep==1]

# plot the simulated data
ep = 5 # epoch to plot
fig1, ax = plt.subplots()
ax.plot(timef,filtered_data[ep,0,:])
ax.plot(timef,filtered_data[ep,1,:])
ax.plot(timef,filtered_data[ep,2,:])
ax.set(xlabel='time (s)', title='%d-%dHz filtered simulated data'%(l_freq,h_freq))
ax.set(xlim=(1, 1.5))

#%%
def plot_corr(corr, title):
    fig, ax = plt.subplots(figsize=(4, 4), constrained_layout=True)
    im = ax.imshow(corr, cmap="viridis", clim=np.percentile(corr[corr!=0], [5, 95]))
    fig.colorbar(im, orientation='vertical')
    fig.suptitle(title)
    
    
phconn = spectral_connectivity_epochs(
    data,
    method="dpli",
    sfreq=fs,
    # indices=indices,
    fmin=l_freq,
    fmax=h_freq,
    faverage=True
    ).get_data(output="dense")[:, :, 0]    
  
phconn = phconn + phconn.T # Add transpose to plot simmetric matrices
plot_corr(phconn, "PLI")



#%% Envelope correlation

envcon = envelope_correlation(filtered_data, 
                     names=None, 
                     orthogonalize=False, 
                     log=False, 
                     absolute=True, 
                     verbose=None)
# Average over epochs
envcon = envcon.combine()
envcon = envcon.get_data(output="dense")[:, :, 0]


envcon_ortho = envelope_correlation(filtered_data, 
                     names=None, 
                     orthogonalize='pairwise', 
                     log=False, 
                     absolute=True, 
                     verbose=None)
# Average over epochs
envcon_ortho = envcon_ortho.combine()
envcon_ortho = envcon_ortho.get_data(output="dense")[:, :, 0]



plot_corr(envcon, "Envelope correlation  non-corrected")
plot_corr(envcon_ortho, "Envelope correlation with pairwise orthogonalization")
