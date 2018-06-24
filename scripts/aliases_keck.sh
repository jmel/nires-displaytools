#!/bin/bash

setenv NIRES_SCRIPTS /home/nireseng/projects/nires-displaytools/scripts
setenv NIRES_PYTHON /home/nireseng/projects/nires-displaytools/nires/displaytools
setenv TEMPDIR /tmp/nires
setenv DATADIR /s/sdata1500/nires4/2018jun24
mkdir $TMPDIR

# ds9 display scripts
alias dp "$NIRES_PYTHON/dp.py --d $DATADIR"
alias dpv "dp v"
alias dps "dp s"

# alias quicklook scripts
alias bp "$NIRES_PYTHON/bp.py --d $DATADIR"
alias bpv "bp v"
alias bps "bp s"

# pdiff scripts
alias pdiff "$NIRES_PYTHON/pdiff.py --d $DATADIR"
alias pdiffv "pdiff v"
alias pdiffs "pdiff s"

# ds9 display level scripts
alias lindisp $NIRES_PYTHON/lindisp.py
alias lindispv "lindisp v"
alias lindisps "lindisp s"

# ds9 cursor scrips
alias cu "$NIRES_PYTHON/cu.py --d $TEMPDIR"
alias cucent $NIRES_SCRIPTS/cucent.sh
alias cudel $NIRES_SCRIPTS/cudel.sh
alias cuslit $NIRES_SCRIPTS/cuslit.sh
