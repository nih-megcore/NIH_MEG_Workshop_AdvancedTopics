#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 13:58:30 2025

@author: jstout
"""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

import os
import os.path as op
import sys
import mne
import re
import glob
import numpy as np
import pandas as pd
import logging
import munch 
import subprocess
import mne_bids
from mne_bids import get_head_mri_trans
from mne.beamformer import make_lcmv, apply_lcmv_epochs
from mne.bem import FIFF
import scipy as sp
from mne_bids import BIDSPath
import functools
from scipy.stats import zscore, trim_mean
from mne.preprocessing import maxwell_filter
from io import StringIO

# set commandline options
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-bids_root')
    parser.add_argument('-bids_id')
    
    args = parser.parse_args()
    bids_root = args.bids_root
    bids_id = args.bids_id

'''  TESTING Variables
bids_root = '/fast2/BIDS'
bids_id = 'ON02811'
raw_fname = op.join(bids_root, f'sub-{bids_id}', 'ses-1','meg', f'sub-{bids_id}_ses-1_task-rest_run-01_meg.ds')
bad_ch_names = ['MLO42-1609', 'MZO03-1609']

'''

# define some variables
fmin = 0.5
fmax = 100
sfreq = 1000
epoch_len = 4.0
n_jobs=20

# parameters for rejecting bad epochs
magthresh = 5000e-15
flatmagthresh = 10e-15
flatgradthresh = 10e-13
std_thresh = 15

# beamformer parameters 
beam_reg = 0.01

# data layout
deriv_dir = op.join(bids_root, 'derivatives')
subjects_dir = op.join(deriv_dir, 'freesurfer', 'subjects')
project_dir = op.join(deriv_dir, 'MEG_adv_topics_conn')
fs_subject = 'sub-'+bids_id
rest_taskname = 'rest'

# setup logging
global log_dir
logger = logging.getLogger()
logger.setLevel(logging.INFO)
buffer_logstream = StringIO('')
ch = logging.StreamHandler(stream=buffer_logstream)
logger.addHandler(ch)

# Function to retrieve the subject/session specific logger

def get_subj_logger(subjid, session, task, run, log_dir=None):
     '''Return the subject specific logger.
     This is particularly useful in the multiprocessing where logging is not
     necessarily in order'''
     fmt = '%(asctime)s :: %(levelname)s :: %(message)s'
     sub_ses = f'{subjid}_ses_{session}_task_{task}_run_{run}'
     subj_logger = logging.getLogger(sub_ses)
     if subj_logger.handlers != []: # if not first time requested, use the file handler already defined
         tmp_ = [type(i) for i in subj_logger.handlers ]
         if logging.FileHandler in tmp_:
             return subj_logger
     else: # first time requested, add the file handler
         fileHandle = logging.FileHandler(f'{log_dir}/{subjid}_ses-{session}_task-{task}_run-{run}_log.txt')
         fileHandle.setLevel(logging.INFO)
         fileHandle.setFormatter(logging.Formatter(fmt)) 
         subj_logger.addHandler(fileHandle)
         subj_logger.info('Initializing subject level enigma log')
     return subj_logger   



#%%
raw_fname = op.join(bids_root, f'sub-{bids_id}', 'ses-01','meg', f'sub-{bids_id}_ses-01_task-rest_run-01_meg.ds')
raw = mne.io.read_raw_ctf(raw_fname, preload=True, system_clock='ignore')

raw.notch_filter([60,120,180], n_jobs=n_jobs)
raw.filter(fmin, fmax, n_jobs=n_jobs)

# raw.save(
    

epo =



#%% MRI section
bids_path = BIDSPath(root=bids_root, subject=bids_id, datatype='meg',
                     task=rest_taskname, session ='01', run = '01')
anat_bids_path = BIDSPath(root=bids_root, subject=bids_id, datatype='anat',
                          extension='.nii.gz', acquisition = 'mprage', suffix = 'T1w', session = '01')

deriv_path = bids_path.copy().update(root=deriv_dir, check=False)
deriv_path.directory.mkdir(exist_ok=True, parents=True)

raw_fname = bids_path.copy().update(run = '01', session = '01')
bem_fname = deriv_path.copy().update(suffix='bem', extension='.fif')
fwd_fname = deriv_path.copy().update(suffix='fwd', extension='.fif')
src_fname = deriv_path.copy().update(suffix='src', extension='.fif')
trans_fname = deriv_path.copy().update(suffix='trans',extension='.fif')
raw = mne.io.read_raw_ctf(raw_fname.fpath, system_clock = 'ignore', clean_names =True)

# subjects_dir = mne_bids.read.get_subjects_dir()
fs_subject = 'sub-'+bids_path.subject
if not bem_fname.fpath.exists():
    mne.bem.make_watershed_bem(fs_subject, subjects_dir=subjects_dir, overwrite=True)
    bem = mne.make_bem_model(fs_subject, subjects_dir=f'{subjects_dir}', 
                             conductivity=[0.3])
    bem_sol = mne.make_bem_solution(bem)
    
    mne.write_bem_solution(bem_fname, bem_sol, overwrite=True)
else:
    bem_sol = mne.read_bem_solution(bem_fname)
    
if not src_fname.fpath.exists():
    src = mne.setup_source_space(fs_subject, spacing='oct6', add_dist='patch',
                         subjects_dir=subjects_dir)
    src.save(src_fname.fpath, overwrite=True)
else:
    src = mne.read_source_spaces(src_fname.fpath)

if not trans_fname.fpath.exists():
    trans = mne_bids.read.get_head_mri_trans(bids_path, extra_params=dict(system_clock='ignore'),
                                        t1_bids_path=anat_bids_path, fs_subject=fs_subject, 
                                        fs_subjects_dir=subjects_dir)
    mne.write_trans(trans_fname.fpath, trans, overwrite=True)
else:
    trans = mne.read_trans(trans_fname.fpath)
if fwd_fname.fpath.exists():
    fwd = mne.read_forward_solution(fwd_fname)
else:
    fwd = mne.make_forward_solution(raw.info, trans, src, bem_sol, eeg=False, 
                                    n_jobs=n_jobs)
    mne.write_forward_solution(fwd_fname.fpath, fwd, overwrite=True)



