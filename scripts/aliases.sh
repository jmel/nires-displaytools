#!/bin/bash

export NIRES_SCRIPTS=/Users/jlmelbourne/Projects/nires-displaytools/scripts
export NIRES_PYTHON=/Users/jlmelbourne/Projects/nires-displaytools/nires/displaytools
export DATADIR=/Users/jlmelbourne/NIRES/data

# ds9 display scripts
alias dp="$NIRES_PYTHON/dp.py --d $DATADIR"
alias dpv="dp v"
alias dps="dp s --d $DATADIR"

# alias quicklook scripts
alias ql=$NIRES_PYTHON/quicklook.py
alias bp="$NIRES_PYTHON/bp.py --d $DATADIR"
alias bpv="bp v"
alias bps="bp s"

# pdiff scripts
alias pdiff="$NIRES_PYTHON/pdiff.py --d $DATADIR"
alias pdiffv="pdiff v"
alias pdiffs="pdiff s"

# ds9 display level scripts
alias lindisp=$NIRES_PYTHON/lindisp.py
alias lindispv="lindisp v"
alias lindisps="lindisp s"

# ds9 cursor scrips
alias cu="$NIRES_PYTHON/cu.py --d $DATADIR"
alias cucent=$NIRES_SCRIPTS/cucent.sh
alias cudel=$NIRES_SCRIPTS/cudel.sh
alias cuslit=$NIRES_SCRIPTS/cuslit.sh
