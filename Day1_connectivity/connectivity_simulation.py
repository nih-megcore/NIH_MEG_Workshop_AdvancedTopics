#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 10:37:30 2025

@author: liuzzil2
"""

import numpy as np
import matplotlib.pyplot as plt
from mne_connectivity import spectral_connectivity_epochs

#%% 
fs = 600 # sampling frequency
t = 5 # total time in seconds
f = 50 # oscillation frequency in Hz
fa = 4 # amplitude modulation frequency
phi2 = np.deg2rad(90) # phase shift of oscillation 2
phi3 = np.deg2rad(10) # phase shift of oscillation 2

phia2 = np.deg2rad(30) # phase shift of amplitude modulation for oscillation 2
phia3 = np.deg2rad(10) # phase shift of amplitude modulation for oscillation 2

time = np.linspace(0, t, int(fs*t), endpoint=False)

oscill1 = np.sin(2*np.pi*f*time) # sine wave at frequency f
oscill2 = np.sin(2*np.pi*f*time + phi2) # wave at frequency f
oscill3 = np.sin(2*np.pi*f*time + phi3) # wave at frequency f

# noise parameters
mu = 0 # noise mean
sigma = 0.5 # noise std
noise1 = np.random.normal(mu, sigma, len(time))
noise2 = np.random.normal(mu, sigma, len(time))
noise3 = np.random.normal(mu, sigma, len(time))

# amplitude
A1 = np.sin(2*np.pi*fa*time)
A2 = np.sin(2*np.pi*fa*time + phia2)
A3 = np.sin(2*np.pi*fa*time + phia3)

signal1 = oscill1*A1 + noise1
signal2 = oscill2*A2 + noise2
signal3 = oscill3*A3 + noise3

# plot the simulated data
fig1, ax = plt.subplots()
ax.plot(time,signal1)
ax.plot(time,signal2)
ax.plot(time,signal3)
ax.set(xlabel='time (s)', title='%dHz sine waves with random noise'%(f))

ax.set(xlim=(0, 0.5))


#%% Create multiple epochs of simulated data by changing the noise

simdata = []

for epoc in range(20):
    noise1 = np.random.normal(mu, sigma, len(time))
    noise2 = np.random.normal(mu, sigma, len(time))
    noise3 = np.random.normal(mu, sigma, len(time))

    signal1 = oscill1*A1 + noise1
    signal2 = oscill2*A2 + noise2
    signal3 = oscill3*A3 + noise3
    
    simdata.append(np.array([signal1,signal2,signal3]))
  
  

#%%
indices = ([0, 0], [1, 2])

conn = []

for method in ["pli", "wpli", "dpli"]:
    conn.append(
        spectral_connectivity_epochs(
            simdata,
            method=method,
            sfreq=fs,
            indices=indices,
            fmin=45,
            fmax=55,
            faverage=True,
        ).get_data()[:, 0]
    )
conn = np.array(conn)


###############################################################################
# The estimated connectivites are shown in the figure below, which provides
# insight into the differences between PLI/wPLI, and dPLI.
#
#
# **Similarities Of All Measures**
#
# * Capture presence of connectivity in same situations (phase difference of
#   :math:`\pm\frac{\pi}{2}`)
# * Do not predict connectivity when phase difference is a multiple of
#   :math:`\pi`
# * Bounded between :math:`0` and :math:`1`
#
# **How dPLI is Different Than PLI/wPLI**
#
# * Null connectivity is :math:`0` for PLI and wPLI, but :math:`0.5` for dPLI
# * dPLI differentiates whether the reference signal is leading or lagging the
#   other signal (lagging if :math:`0 <= dPlI < 0.5`, leading if
#   :math:`0.5 < dPLI <= 1.0`)


x = np.arange(2)

plt.figure()
plt.bar(x - 0.2, conn[0], 0.2, align="center", label="PLI")
plt.bar(x, conn[1], 0.2, align="center", label="wPLI")
plt.bar(x + 0.2, conn[2], 0.2, align="center", label="dPLI")

plt.title("Connectivity Estimation Comparison")
plt.xticks(x, (r"$\pi/2$", r"$\pi/18$"))
plt.legend()
plt.xlabel("Phase Difference")
plt.ylabel("Estimated Connectivity")

plt.show()