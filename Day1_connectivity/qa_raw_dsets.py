#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 15:53:42 2025

@author: jstout
"""

sub-ON03748

import glob
import mne
import pandas as pd

dsets = ['sub-ON02747/ses-01/meg/sub-ON02747_ses-01_task-rest_run-01_meg.ds',
 'sub-ON02811/ses-01/meg/sub-ON02811_ses-01_task-rest_run-01_meg.ds',
 'sub-ON02811/ses-01/meg/sub-ON02811_ses-01_task-rest_run-02_meg.ds',
 'sub-ON03748/ses-01/meg/sub-ON03748_ses-01_task-rest_run-01_meg.ds',
 'sub-ON05311/ses-01/meg/sub-ON05311_ses-01_task-rest_run-01_meg.ds',
 'sub-ON05530/ses-01/meg/sub-ON05530_ses-01_task-rest_run-01_meg.ds',
 'sub-ON06910/ses-01/meg/sub-ON06910_ses-01_task-rest_run-01_meg.ds',
 'sub-ON08392/ses-01/meg/sub-ON08392_ses-01_task-rest_run-01_meg.ds',
 'sub-ON08643/ses-01/meg/sub-ON08643_ses-01_task-rest_run-01_meg.ds',
 'sub-ON08710/ses-1/meg/sub-ON08710_ses-1_task-rest_run-01_meg.ds',
 'sub-ON08792/ses-01/meg/sub-ON08792_ses-01_task-rest_run-01_meg.ds',
 'sub-ON09540/ses-1/meg/sub-ON09540_ses-1_task-rest_run-01_meg.ds',
 'sub-ON09760/ses-1/meg/sub-ON09760_ses-1_task-rest_run-01_meg.ds',
 'sub-ON09766/ses-1/meg/sub-ON09766_ses-1_task-rest_run-01_meg.ds',
 'sub-ON10965/ses-01/meg/sub-ON10965_ses-01_task-rest_run-01_meg.ds',
 'sub-ON11394/ses-01/meg/sub-ON11394_ses-01_task-rest_run-01_meg.ds',
 'sub-ON12688/ses-01/meg/sub-ON12688_ses-01_task-rest_run-01_meg.ds',
 'sub-ON13545/ses-01/meg/sub-ON13545_ses-01_task-rest_run-01_meg.ds',
 'sub-ON13986/ses-01/meg/sub-ON13986_ses-01_task-rest_run-01_meg.ds',
 'sub-ON21976/ses-01/meg/sub-ON21976_ses-01_task-rest_run-01_meg.ds',
 'sub-ON22671/ses-01/meg/sub-ON22671_ses-01_task-rest_run-01_meg.ds',
 'sub-ON23483/ses-01/meg/sub-ON23483_ses-01_task-rest_run-01_meg.ds',
 'sub-ON25658/ses-01/meg/sub-ON25658_ses-01_task-rest_run-01_meg.ds',
 'sub-ON25939/ses-01/meg/sub-ON25939_ses-01_task-rest_run-01_meg.ds',
 'sub-ON26105/ses-1/meg/sub-ON26105_ses-1_task-rest_run-01_meg.ds',
 'sub-ON26309/ses-01/meg/sub-ON26309_ses-01_task-rest_run-01_meg.ds',
 'sub-ON28693/ses-01/meg/sub-ON28693_ses-01_task-rest_run-01_meg.ds',
 'sub-ON33221/ses-1/meg/sub-ON33221_ses-1_task-rest_run-01_meg.ds',
 'sub-ON33827/ses-01/meg/sub-ON33827_ses-01_task-rest_run-01_meg.ds',
 'sub-ON39099/ses-01/meg/sub-ON39099_ses-01_task-rest_run-01_meg.ds',
 'sub-ON40397/ses-01/meg/sub-ON40397_ses-01_task-rest_run-01_meg.ds',
 'sub-ON41090/ses-01/meg/sub-ON41090_ses-01_task-rest_run-01_meg.ds',
 'sub-ON42107/ses-01/meg/sub-ON42107_ses-01_task-rest_run-01_meg.ds',
 'sub-ON43016/ses-01/meg/sub-ON43016_ses-01_task-rest_run-01_meg.ds',
 'sub-ON43210/ses-1/meg/sub-ON43210_ses-1_task-rest_run-01_meg.ds',
 'sub-ON43585/ses-01/meg/sub-ON43585_ses-01_task-rest_run-01_meg.ds',
 'sub-ON47254/ses-01/meg/sub-ON47254_ses-01_task-rest_run-01_meg.ds',
 'sub-ON48555/ses-01/meg/sub-ON48555_ses-01_task-rest_run-01_meg.ds',
 'sub-ON48925/ses-01/meg/sub-ON48925_ses-01_task-rest_run-01_meg.ds',
 'sub-ON49080/ses-01/meg/sub-ON49080_ses-01_task-rest_run-01_meg.ds',
 'sub-ON50015/ses-01/meg/sub-ON50015_ses-01_task-rest_run-01_meg.ds',
 'sub-ON51111/ses-1/meg/sub-ON51111_ses-1_task-rest_run-01_meg.ds',
 'sub-ON52083/ses-01/meg/sub-ON52083_ses-01_task-rest_run-01_meg.ds',
 'sub-ON52220/ses-1/meg/sub-ON52220_ses-1_task-rest_run-01_meg.ds',
 'sub-ON52662/ses-01/meg/sub-ON52662_ses-01_task-rest_run-01_meg.ds',
 'sub-ON54268/ses-01/meg/sub-ON54268_ses-01_task-rest_run-01_meg.ds',
 'sub-ON56044/ses-01/meg/sub-ON56044_ses-01_task-rest_run-01_meg.ds',
 'sub-ON56250/ses-01/meg/sub-ON56250_ses-01_task-rest_run-01_meg.ds',
 'sub-ON61373/ses-01/meg/sub-ON61373_ses-01_task-rest_run-01_meg.ds',
 'sub-ON62003/ses-01/meg/sub-ON62003_ses-01_task-rest_run-01_meg.ds',
 'sub-ON62200/ses-1/meg/sub-ON62200_ses-1_task-rest_run-01_meg.ds',
 'sub-ON63221/ses-1/meg/sub-ON63221_ses-1_task-rest_run-01_meg.ds',
 'sub-ON63734/ses-01/meg/sub-ON63734_ses-01_task-rest_run-01_meg.ds',
 'sub-ON66199/ses-01/meg/sub-ON66199_ses-01_task-rest_run-01_meg.ds',
 'sub-ON67270/ses-01/meg/sub-ON67270_ses-01_task-rest_run-01_meg.ds',
 'sub-ON68840/ses-01/meg/sub-ON68840_ses-01_task-rest_run-01_meg.ds',
 'sub-ON69163/ses-01/meg/sub-ON69163_ses-01_task-rest_run-01_meg.ds',
 'sub-ON70467/ses-01/meg/sub-ON70467_ses-01_task-rest_run-01_meg.ds',
 'sub-ON72082/ses-01/meg/sub-ON72082_ses-01_task-rest_run-01_meg.ds',
 'sub-ON72409/ses-01/meg/sub-ON72409_ses-01_task-rest_run-01_meg.ds',
 'sub-ON73200/ses-1/meg/sub-ON73200_ses-1_task-rest_run-01_meg.ds',
 'sub-ON73969/ses-01/meg/sub-ON73969_ses-01_task-rest_run-01_meg.ds',
 'sub-ON75100/ses-1/meg/sub-ON75100_ses-1_task-rest_run-01_meg.ds',
 'sub-ON76144/ses-1/meg/sub-ON76144_ses-1_task-rest_run-01_meg.ds',
 'sub-ON76320/ses-1/meg/sub-ON76320_ses-1_task-rest_run-01_meg.ds',
 'sub-ON76525/ses-1/meg/sub-ON76525_ses-1_task-rest_run-01_meg.ds',
 'sub-ON76625/ses-1/meg/sub-ON76625_ses-1_task-rest_run-01_meg.ds',
 'sub-ON77753/ses-1/meg/sub-ON77753_ses-1_task-rest_run-01_meg.ds',
 'sub-ON80038/ses-01/meg/sub-ON80038_ses-01_task-rest_run-01_meg.ds',
 'sub-ON81734/ses-01/meg/sub-ON81734_ses-01_task-rest_run-01_meg.ds',
 'sub-ON82386/ses-01/meg/sub-ON82386_ses-01_task-rest_run-01_meg.ds',
 'sub-ON83320/ses-1/meg/sub-ON83320_ses-1_task-rest_run-01_meg.ds',
 'sub-ON84201/ses-1/meg/sub-ON84201_ses-1_task-rest_run-01_meg.ds',
 'sub-ON84651/ses-01/meg/sub-ON84651_ses-01_task-rest_run-01_meg.ds',
 'sub-ON84896/ses-01/meg/sub-ON84896_ses-01_task-rest_run-01_meg.ds',
 'sub-ON85010/ses-1/meg/sub-ON85010_ses-1_task-rest_run-01_meg.ds',
 'sub-ON85301/ses-1/meg/sub-ON85301_ses-1_task-rest_run-01_meg.ds',
 'sub-ON85305/ses-01/meg/sub-ON85305_ses-01_task-rest_run-01_meg.ds',
 'sub-ON85400/ses-1/meg/sub-ON85400_ses-1_task-rest_run-01_meg.ds',
 'sub-ON85514/ses-1/meg/sub-ON85514_ses-1_task-rest_run-01_meg.ds',
 'sub-ON85616/ses-01/meg/sub-ON85616_ses-01_task-rest_run-01_meg.ds',
 'sub-ON86202/ses-01/meg/sub-ON86202_ses-01_task-rest_run-01_meg.ds',
 'sub-ON87304/ses-1/meg/sub-ON87304_ses-1_task-rest_run-01_meg.ds',
 'sub-ON87304/ses-1/meg/sub-ON87304_ses-1_task-rest_run-02_meg.ds',
 'sub-ON87550/ses-1/meg/sub-ON87550_ses-1_task-rest_run-01_meg.ds',
 'sub-ON87616/ses-1/meg/sub-ON87616_ses-1_task-rest_run-01_meg.ds',
 'sub-ON87631/ses-1/meg/sub-ON87631_ses-1_task-rest_run-01_meg.ds',
 'sub-ON87642/ses-1/meg/sub-ON87642_ses-1_task-rest_run-01_meg.ds',
 'sub-ON87655/ses-1/meg/sub-ON87655_ses-1_task-rest_run-01_meg.ds',
 'sub-ON87743/ses-1/meg/sub-ON87743_ses-1_task-rest_run-01_meg.ds',
 'sub-ON87777/ses-1/meg/sub-ON87777_ses-1_task-rest_run-01_meg.ds',
 'sub-ON88614/ses-01/meg/sub-ON88614_ses-01_task-rest_run-01_meg.ds',
 'sub-ON88700/ses-1/meg/sub-ON88700_ses-1_task-rest_run-01_meg.ds',
 'sub-ON88753/ses-1/meg/sub-ON88753_ses-1_task-rest_run-01_meg.ds',
 'sub-ON88762/ses-1/meg/sub-ON88762_ses-1_task-rest_run-01_meg.ds',
 'sub-ON89045/ses-01/meg/sub-ON89045_ses-01_task-rest_run-01_meg.ds',
 'sub-ON89474/ses-01/meg/sub-ON89474_ses-01_task-rest_run-01_meg.ds',
 'sub-ON89475/ses-01/meg/sub-ON89475_ses-01_task-rest_run-01_meg.ds',
 'sub-ON91906/ses-01/meg/sub-ON91906_ses-01_task-rest_run-01_meg.ds',
 'sub-ON92220/ses-1/meg/sub-ON92220_ses-1_task-rest_run-01_meg.ds',
 'sub-ON93222/ses-1/meg/sub-ON93222_ses-1_task-rest_run-01_meg.ds',
 'sub-ON93426/ses-01/meg/sub-ON93426_ses-01_task-rest_run-01_meg.ds',
 'sub-ON94110/ses-1/meg/sub-ON94110_ses-1_task-rest_run-01_meg.ds',
 'sub-ON94131/ses-1/meg/sub-ON94131_ses-1_task-rest_run-01_meg.ds',
 'sub-ON94856/ses-01/meg/sub-ON94856_ses-01_task-rest_run-01_meg.ds',
 'sub-ON95003/ses-01/meg/sub-ON95003_ses-01_task-rest_run-01_meg.ds',
 'sub-ON95422/ses-01/meg/sub-ON95422_ses-01_task-rest_run-01_meg.ds',
 'sub-ON95520/ses-1/meg/sub-ON95520_ses-1_task-rest_run-01_meg.ds',
 'sub-ON95742/ses-01/meg/sub-ON95742_ses-01_task-rest_run-01_meg.ds',
 'sub-ON96252/ses-1/meg/sub-ON96252_ses-1_task-rest_run-01_meg.ds',
 'sub-ON96353/ses-1/meg/sub-ON96353_ses-1_task-rest_run-01_meg.ds',
 'sub-ON96510/ses-1/meg/sub-ON96510_ses-1_task-rest_run-01_meg.ds',
 'sub-ON96555/ses-1/meg/sub-ON96555_ses-1_task-rest_run-01_meg.ds',
 'sub-ON97503/ses-1/meg/sub-ON97503_ses-1_task-rest_run-01_meg.ds',
 'sub-ON97504/ses-01/meg/sub-ON97504_ses-01_task-rest_run-01_meg.ds',
 'sub-ON97654/ses-1/meg/sub-ON97654_ses-1_task-rest_run-01_meg.ds',
 'sub-ON97765/ses-1/meg/sub-ON97765_ses-1_task-rest_run-01_meg.ds',
 'sub-ON98130/ses-1/meg/sub-ON98130_ses-1_task-rest_run-01_meg.ds',
 'sub-ON98362/ses-1/meg/sub-ON98362_ses-1_task-rest_run-01_meg.ds',
 'sub-ON98502/ses-1/meg/sub-ON98502_ses-1_task-rest_run-01_meg.ds',
 'sub-ON98602/ses-1/meg/sub-ON98602_ses-1_task-rest_run-01_meg.ds',
 'sub-ON98664/ses-1/meg/sub-ON98664_ses-1_task-rest_run-01_meg.ds',
 'sub-ON98745/ses-1/meg/sub-ON98745_ses-1_task-rest_run-01_meg.ds',
 'sub-ON98826/ses-1/meg/sub-ON98826_ses-1_task-rest_run-01_meg.ds',
 'sub-ON99547/ses-1/meg/sub-ON99547_ses-1_task-rest_run-01_meg.ds',
 'sub-ON99620/ses-01/meg/sub-ON99620_ses-01_task-rest_run-01_meg.ds',
 'sub-ON99633/ses-1/meg/sub-ON99633_ses-1_task-rest_run-01_meg.ds',
 'sub-ON99881/ses-1/meg/sub-ON99881_ses-1_task-rest_run-01_meg.ds',
 'sub-ON99943/ses-1/meg/sub-ON99943_ses-1_task-rest_run-01_meg.ds']


def assess_annotations(raw_var, subjid):
    if len(raw_var.annotations)>0:
        dframe = pd.DataFrame(raw_var.annotations)
        dframe.to_csv(f'./BAD_segments/{subjid}_bad.csv')

def plot_dsets(dset):
    subjid = dset.split('/')[0]
    raw = mne.io.read_raw_ctf(dset, clean_names=True, system_clock='ignore', 
                              preload=True)
    if raw.compensation_grade != 3:
        raw.apply_gradient_compensation(3)
    raw.pick_types(meg='mag')
    raw.filter(0.5, None, n_jobs=20)
    raw.notch_filter([60,120,180], n_jobs=20)
    raw.plot(n_channels=40, block=True)  
    _ = input('Hit anything to continue')
    print(f'{subjid} : {raw.info["bads"]} : BAD {len(raw.annotations)}')
    _ = input('Hit anything to continue')
    assess_annotations(raw, subjid)
    
    
# processed = ['sub-ON02747/ses-01/meg/sub-ON02747_ses-01_task-rest_run-01_meg.ds',
#  'sub-ON02811/ses-01/meg/sub-ON02811_ses-01_task-rest_run-01_meg.ds',
#  'sub-ON02811/ses-01/meg/sub-ON02811_ses-01_task-rest_run-02_meg.ds']


for i in dsets:
    if i in processed:
        continue
    plot_dsets(i)
    processed.append(i)
    

#%% Recover annotations

dframe = pd.read_csv(dframe_fname)
annot = mne.Annotations(onset=dframe.onset.values,
                       duration=dframe.duration.values, 
                       description=dframe.description.values,
                       )
raw.set_annotations(annot)
 = 
                





    


