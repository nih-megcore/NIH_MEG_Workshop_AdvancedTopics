#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 13:58:30 2025

@author: jstout
"""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# some of this import may not be necessary - pulled from another file
import os
import os.path as op
import sys
import mne
import re
import glob
import numpy as np
import pandas as pd
import logging
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
import pandas as pd

# set commandline options
if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-bids_root')
    parser.add_argument('-bids_id')
    parser.add_argument('-batch_hv2', default=False, action='store_true')
    parser.add_argument('-fmin',help='Low frequency cutoff for highpass filter', 
                        default=None, type=float)
    parser.add_argument('-fmax',help='High frequency cutoff for lowpass filter', 
                        default=None, type=float)
    parser.add_argument('-reg', help='Beamformer regularization', 
                        default=0.05, type=float)
    
    
    args = parser.parse_args()
    bids_root = args.bids_root
    bids_id = args.bids_id
    batch2 = args.batch_hv2
    fmin=args.fmin
    fmax=args.fmax
    beam_reg = args.reg
    os.chdir(bids_root)

'''  TESTING Variables
bids_root = '/fast2/BIDS'
bids_id = 'ON02811'
raw_fname = op.join(bids_root, f'sub-{bids_id}', 'ses-1','meg', f'sub-{bids_id}_ses-1_task-rest_run-01_meg.ds')
fmin=15
fmax=35
beam_reg=0.01
'''

# define some variables
sfreq = 600
epoch_len = 5.0
n_jobs=8

# parameters for rejecting bad epochs
magthresh = 5000e-15
flatmagthresh = 10e-15
flatgradthresh = 10e-13
std_thresh = 15


# data layout
deriv_dir = op.join(bids_root, 'derivatives')
subjects_dir = op.join(deriv_dir, 'freesurfer', 'subjects')
project_dir = op.join(deriv_dir, 'MEG_adv_topics_conn')
fs_subject = 'sub-'+bids_id
rest_taskname = 'rest'

if (fmin!=None) and (fmax!=None):
    output_dir = op.join(deriv_dir, 'beamformer_testing', f'beam_f{fmin}-{fmax}_reg-{beam_reg}')
else:
    output_dir = op.join(deriv_dir, 'beamformer_testing', f'beam_reg-{beam_reg}')
if not op.exists(output_dir): os.makedirs(output_dir)

def _handle_csv_list(entry):
    if type(entry)!=str:
        return None 
    if '[' in entry:
        _tmp = entry.replace('[','').replace(']','').replace("'","").replace(' ','').split(',')
        return _tmp
    else: 
        return [entry]

def append_bad_ch_annot(raw, subjid):
    '''Load the QA dataframe and get the bad channels
    Load the subject specific BAD_segments csv file and write to the raw annotations'''
    # topdir = '~/src/NIH_MEG_Workshop_AdvancedTopics'
    topdir = op.dirname(op.dirname(__file__)) 
    score_dframe = pd.read_csv(f'{topdir}/Day1_connectivity/artifact_scoring.csv', sep='\t')
    score_dframe.rename({'Unnamed: 0': 'fname'}, axis=1, inplace=True)
    
    #Assign the subjids from the filename after cleanup
    tmp_ = score_dframe.fname.str.split('/', expand=True)[0].values
    tmp_ = [i.strip().replace("'","") for i in tmp_]    
    score_dframe.subjid = tmp_
    
    #Drop duplicates
    score_dframe = score_dframe.loc[~score_dframe.subjid.duplicated()]
    _subjid = 'sub-'+subjid
    _query = f'subjid=="{_subjid}"'
    row = score_dframe.query(_query) 
    print(row.badchans.values[0])
    _val = _handle_csv_list(row.badchans.values[0])
    print(_val)
    if _val==None:
        pass
    elif _val.__len__() > 1:
        raw.info['bads'] = _val
    elif not row.badchans.isna().values[0]:
        if row.badchans.values[0]=='0':
            pass  #just to make this function work
        else:
            raw.info['bads'] = _val
        
    #Load the bad semgents info     
    dframe_fname = op.join(os.getcwd(), 'BAD_segments', f'sub-{subjid}_bad.csv')
    if op.exists(dframe_fname):
        dframe = pd.read_csv(dframe_fname)
        annot = mne.Annotations(onset=dframe.onset.values,
                               duration=dframe.duration.values, 
                               description=dframe.description.values,
                               )
        raw.set_annotations(annot)
    else:
        print(f'There is not a csv file for this subject {subjid}')
    return raw


#%%
if op.exists(f'sub-{bids_id}/ses-01'):
    raw_fname = op.join(bids_root, f'sub-{bids_id}', 'ses-01','meg', f'sub-{bids_id}_ses-01_task-rest_run-01_meg.ds')
elif  op.exists(f'sub-{bids_id}/ses-1'):
    raw_fname = op.join(bids_root, f'sub-{bids_id}', 'ses-1','meg', f'sub-{bids_id}_ses-1_task-rest_run-01_meg.ds')
    assert op.exists(raw_fname)
raw = mne.io.read_raw_ctf(raw_fname, preload=True, system_clock='ignore', 
                          clean_names=True)

raw = append_bad_ch_annot(raw, bids_id)


raw.resample(sfreq, n_jobs=n_jobs)
raw.notch_filter([60,120,180], n_jobs=n_jobs)
raw.filter(0.5, None, n_jobs=n_jobs)  #Set wideband filter for epoch drops based on amplitude

tmax = epoch_len    
evts = mne.make_fixed_length_events(raw, duration=epoch_len)
reject_dict = dict(mag=5e-12)
epochs = mne.Epochs(raw, evts, reject=reject_dict, #flat=flat_dict,
                preload=True, baseline=None, tmin=0, tmax=tmax)

if (fmin!=None) and (fmax!=None):
    epochs.filter(fmin, fmax, n_jobs=n_jobs)


data_cov = mne.compute_covariance(epochs, method='empirical') 






#%% MRI section
bids_path = BIDSPath(root=bids_root, subject=bids_id, datatype='meg',
                     task=rest_taskname, session ='01', run = '01')

mri_search = glob.glob(f'sub-{bids_id}*/**/*T1w.nii.gz', recursive=True) #+glob.glob(f'sub-{bids_id}*/**/*ses-1_T1w.nii.gz', recursive=True)
mri_search = mri_search[0]
anat_bids_path = mne_bids.get_bids_path_from_fname(mri_search)

raw_fname = bids_path.copy() 
if not raw_fname.fpath.exists():
    bids_path = BIDSPath(root=bids_root, subject=bids_id, datatype='meg',
                         task=rest_taskname, session ='1', run = '01')
    raw_fname = bids_path.copy() 

print(anat_bids_path.fpath)
assert raw_fname.fpath.exists()
if not anat_bids_path.fpath.exists():
    anat_bids_path.update(acquisition=None)
assert anat_bids_path.fpath.exists()


deriv_path = bids_path.copy().update(root=project_dir, check=False)
deriv_path.directory.mkdir(exist_ok=True, parents=True)

#raw_fname = bids_path.copy().update(run = '01', session = '01')
bem_fname = deriv_path.copy().update(suffix='bem', extension='.fif')
fwd_fname = deriv_path.copy().update(suffix='fwd', extension='.fif')
src_fname = deriv_path.copy().update(suffix='src', extension='.fif')
trans_fname = deriv_path.copy().update(suffix='trans',extension='.fif')
# raw = mne.io.read_raw_ctf(raw_fname.fpath, system_clock = 'ignore', clean_names =True)


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
    fwd = mne.make_forward_solution(epochs.info, trans, src, bem_sol, eeg=False, 
                                    n_jobs=n_jobs)
    mne.write_forward_solution(fwd_fname.fpath, fwd, overwrite=True)


#%% Beamformer section

# epochs.pick_types(meg=True, ref_meg=False)

filters = make_lcmv(epochs.info, fwd, data_cov, #noise_cov=noise_cov, 
                    reg=beam_reg, pick_ori='max-power') #rank=epo_rank, pick_ori='max-power') 

stcs = apply_lcmv_epochs(epochs=epochs, filters=filters, return_generator=False)  


#%% Extract PCA of the consistent oriented vertices

from mne.fixes import _safe_svd
import numpy as np

# Mod of the pca flip from mne v1.5 - No flip used
def _pca(data):
    U, s, V = _safe_svd(data, full_matrices=False)
    # use average power in label for scaling
    scale = np.linalg.norm(s) / np.sqrt(len(data))
    return scale * V[0]

def get_label_vertex_idxs(label, stc):
    if label.hemi=='lh':
        hemi_idx=0
        hemi_offset = 0
    else:
        hemi_idx=1
        hemi_offset = len(stc.vertices[0])
    label_stc_vertices = label.get_vertices_used(stc.vertices[hemi_idx])
    label_vert_idxs = np.searchsorted(stc.vertices[hemi_idx], label_stc_vertices)
    return label_vert_idxs
    

def get_full_label_ts(label, stcs):
    '''Returns a continuous dataset of the stcs data from the label'''
    label_vert_idxs = get_label_vertex_idxs(label, stcs[0])
    
    #Extract the label vertex data into a list from the stcs
    _tmp = [stcs[i].data[label_vert_idxs,:] for i in range(len(stcs))]
    #Concatenate to get a timeseries of Vertices X epoTime   (epoTime is concatenation along epochs and time)
    label_ts = np.concatenate(_tmp, axis=1) 
    return label_ts

def flip_verts(label, stcs):
    '''Compute the label vertices flips based on correlations with 1st PCA.
    '''
    label_vert_data = get_full_label_ts(label, stcs)
    label_pca = _pca(label_vert_data)
    
    # Identify the in-phase data to determine the flips
    _tmp = np.dot(label_pca, label_vert_data.T)
    flips = _tmp<0
    label_vert_data[flips,:] *= -1
    return label_vert_data


def _compute_label_ts(label, stcs):
    label_vert_data = flip_verts(label,stcs)

    #Get the final PCA after performing the flips
    label_data = _pca(label_vert_data)

    #Reshape the pca back into epochs
    epo_label_pca = label_data.reshape([len(stcs), stcs[0].shape[-1]])
    
    return epo_label_pca

def extract_label_ts(labels, stcs):
    label_dat=[]
    for label in labels:
        print(label.name)
        label_dat.append(_compute_label_ts(label, stcs))
    return np.stack(label_dat)



#%% Get the parcels

labels = mne.read_labels_from_annot(
    fs_subject, "aparc", subjects_dir=subjects_dir
)

#Re-order labels to be lhemi then rhemi
labels = labels[::2] + labels[1::2]

# def get_centroid_idx(label=None, stc=None, hemi=None):
#     '''
#     Return the numpy index of the centroid corresponding to the center of mass
#     '''
#     if hemi=='lh':
#         hemi_idx=0
#         hemi_offset = 0
#     else:
#         hemi_idx=1
#         hemi_offset = len(stc.vertices[0])
#     _used_verts = label.get_vertices_used(stc.vertices[hemi_idx])
#     #Get the center of mass from the used label vertices - returns freesurfer vertex
#     COM_idx = label.center_of_mass(restrict_vertices=_used_verts, subjects_dir=subjects_dir)
#     #Get the numpy index of this vertex
#     np_idx = np.where(stc.vertices[hemi_idx]==COM_idx)[0][0]
#     np_idx += hemi_offset
#     return np_idx


# template_stc = stcs[0]
# label_idxs = {i.name:None for i in labels}
# for label in labels:
#     COM = label.center_of_mass(restrict_vertices=True, subjects_dir=subjects_dir)
#     label_idxs[label.name] = get_centroid_idx(label=label, stc=template_stc, hemi=label.hemi)
    

# # import copy
# # test_stc = copy.deepcopy(stcs[0])
# # test_stc._data=np.zeros(test_stc._data.shape)
# # for idx in label_idxs.values():
# #     test_stc._data[idx,:]=5


# # test_stc._data[4011,:]=5
# # test_stc._data[4745,:]=5
# #  'precuneus-lh': 4011,
# #  'precuneus-rh': 4745,

#%%  Convert STC matrix into centroid ROI matrix
# roi_len=len(labels)
# roi_idx_vector = list(label_idxs.values())
# #Initialize matrix   Epochs X ROI X Time
# roi_matrix = np.zeros([len(stcs), roi_len, template_stc.shape[-1]])
# for epo_idx, stc in enumerate(stcs):
#     roi_matrix[epo_idx, :, :] = stc._data[roi_idx_vector, :]



    
# np.save(f'{output_dir}/sub-{bids_id}.npy', roi_matrix)    
# labelnames = [i.name for i in labels]
# label_fname = f'{output_dir}/sub-{bids_id}_label_ids.txt'
# with open(label_fname, 'w+') as f:
#     for idx,i in enumerate(labels):
#         f.write(f'{i.name}\n')
#         print(idx)
# print('\n\n')
# print('!!!!!!!!! FINISHED !!!!!!!!!!!!!!!!')
# print('\n\n')

#%% From 

label_mat = extract_label_ts(labels, stcs)
label_mat = np.swapaxes(label_mat, 0, 1) # Connectivity expects Epochs x Label x Time
    
np.save(f'{output_dir}/sub-{bids_id}.npy', label_mat)    
labelnames = [i.name for i in labels]
label_fname = f'{output_dir}/sub-{bids_id}_label_ids.txt'
with open(label_fname, 'w+') as f:
    for idx,i in enumerate(labels):
        f.write(f'{i.name}\n')
        print(idx)
print('\n\n')
print('!!!!!!!!! FINISHED !!!!!!!!!!!!!!!!')
print('\n\n')

