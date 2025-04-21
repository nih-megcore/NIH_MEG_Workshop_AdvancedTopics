
#>>>> https://stackoverflow.com/questions/53382383/makefile-cant-use-conda-activate
# Need to specify bash in order for conda activate to work.
SHELL=/bin/bash
# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate 
# <<<<

install_env:
	mamba create --override-channels --channel=conda-forge --name=nih_meg_workshop_adv pip 'python==3.12' 'mne==1.9'  -y
	($(CONDA_ACTIVATE) nih_meg_workshop_adv ; pip install -e .)
install_biowulf:
	mamba create --override-channels --channel=conda-forge -p=/data/MEGmodules/modules/meg_workshop_2025adv pip 'python==3.12' 'mne==1.9'  -y
	($(CONDA_ACTIVATE) /data/MEGmodules/modules/meg_workshop_2025adv ; pip install -e .)
