#!/bin/bash

export NIRES_SCRIPTS=/Users/jlmelbourne/Projects/nires-displaytools/scripts
export NIRES_PYTHON=/Users/jlmelbourne/Projects/nires-displaytools/nires/displaytools

# ds9 display scripts
alias dp=$NIRES_PYTHON/dp.py
alias dpv="dp v"
alias dps="dp s"
alias dpcv="dp v c"
alias dpcs="dp s c"

# pdiff scripts
alias pdiff=$NIRES_PYTHON/pdiff.py
alias pdiffv="pdiff v"
alias pdiffs="pdiff s"

# ds9 display level scripts
alias lindisp=$NIRES_PYTHON/lindisp.py
alias lindispv="lindisp v"
alias lindisps="lindisp s"

# ds9 cursor scrips
alias cu=$NIRES_PYTHON/cu.py
alias cucent=$NIRES_SCRIPTS/cucent.sh
alias cudel=$NIRES_SCRIPTS/cudel.sh
alias cuslit=$NIRES_SCRIPTS/cuslit.sh
