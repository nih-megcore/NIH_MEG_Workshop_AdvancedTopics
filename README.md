# NIH_MEG_Workshop_AdvancedTopics

[Calendar](#Calendar) <br>
[Biowulf Setup](#BiowulfInfo) <br>
[Install](#Install) <br>


<a id="Calendar"></a>
## Day 1 (05/02/2025)  - FAES ROOM 6 – B1C208
### Connectivity and Decoding
| Time  | Topic | Presenter |
| :---- | ---- | ---- |
| 9:00 - 9:15 | Computer Setup etc |
| 9:15 - 9:30 | Course Intro + Souce Localization (for connectivity) | Jeff |
| 9:30 - 10:30 | Connectivity Background | Lucrezia |
| 10:30 - 11:30 | Connectivity Code | |
| 11:30 - 12:30 | Lunch  
| 12:30 - 1:30  |  Decoding Background  |  Lina | 
| 1:45 - 2:30   |  Decoding Applications  |  Shruti, Alexis, Sebastian | 
| 2:30 - 4:00   |  Decoding Code  |  | 




<a id="BiowulfInfo"></a>
# Computer Setup
Copy the following lines into your terminal.
This will copy the code/notebooks and data into your local folder.  
```
sinteractive --mem=32G --cpus-per-task=12 --tunnel  #Wait for this to start
```

```
module use --append /data/MEGmodules/modulefiles  #You can add this to your .bashrc for convenience
module load meg_workshop/2025adv.1
```
```
get_code   #Copy the code to your current directory
get_data   #Copy and untar the data to your /data/${USER}/meg_data_workshop
```
```
cd /data/${USER}/NIH_MEG_Workshop_AdvancedTopics
jupyter notebook --no-browser --port $PORT1
```

<a id="Install"></a>
# Install Code (on your own system)
Install using make: <br>
`make install_env`
<br>
Install from conda environment.yml file:<br>
`conda env create --name envname --file=environments.yml`



