# NIH_MEG_Workshop_AdvancedTopics

[Calendar](#Calendar) <br>


<a id="Calendar"></a>
## Day 1 (05/02/2025)  - FAES ROOM 6 – B1C208
| Time  | Topic | Presenter |
| :---- | ---- | ---- |
| 9:00 - 9:10 | Bagel Config + Coffee Download + Computer Setup |
| ? | Course Intro | Jeff |
| ? | Connectivity Background | Lucrezia |
| 11:45 - 12:30 | Lunch  
| ?           |  Decoding Background  |  Lina | 
| 3:45 - 4:30 | [Lab 3 MRI Integration](https://github.com/nih-megcore/MEG_workshop_2023/blob/main/Day1/Lab3_MRI_processing.ipynb) |


# Computer Setup
Copy the following lines into your terminal.
This will copy the code/notebooks and data into your local folder.  
```
sinteractive --mem=16G --cpus-per-task=12 --gres=lscratch:10  #Wait for this to start
```

```
module use --append /data/MEGmodules/modulefiles  #You can add this to your .bashrc for convenience
module load meg_workshop_advp1

get_code   #Copy the code to your current directory
get_data   #Copy and untar the data to your /data/${USER}/meg_data_workshop

cd NIMH_MEG_workshop
jupyter lab
```
