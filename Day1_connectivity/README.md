# Intro to connectivity


# Source localization
Copy HV data Batch1 and Batch2 (+freesurfer) into /data/NIMH_scratch/MEG_tmp/NIH_WORKSHOP_ADV/BIDSv2 <br>

Inside each bids dir make an OUTPUTS directory <br>
Copy the BAD_SEGMENTS folder into each BIDSv# dir <br>

### Generate the swarm files
#Batch1
```
module load meg_workshop/2025_adv
cd /data/NIMH_scratch/MEG_tmp/BIDSv2
for i in $(find sub-* -name '*T1w.nii.gz'); do subjid=${i:4:7}; echo /data/MEGmodules/modules/meg_workshop_2025adv_extras/NIH_MEG_Workshop_AdvancedTopics/Day1_connectivity/source_localize.py -bids_root $(pwd) -bids_id $subjid >> swarm_source_localize.sh; done
swarm -f swarm_source_localize.sh -t 10 -g 20 --logdir=./logdir
```


#Batch2
```
module load meg_workshop/2025_adv
cd /data/NIMH_scratch/MEG_tmp/BIDSv2
for i in $(find sub-* -name '*T1w.nii.gz'); do subjid=${i:4:7}; echo /data/MEGmodules/modules/meg_workshop_2025adv_extras/NIH_MEG_Workshop_AdvancedTopics/Day1_connectivity/source_localize.py -bids_root $(pwd) -bids_id $subjid -batch_hv2 >> swarm_source_localize_batch2.sh; done
swarm -f swarm_source_localize_batch2.sh -t 10 -g 20 --logdir=./logdir
```

