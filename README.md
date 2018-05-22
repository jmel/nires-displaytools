# NIRES Display Tools
We have built a series of command-line tools to display and interact with
NIRES data in ds9. The primary goal of these tools is to facilitate ease
of use of the instrument when observing at Keck.

## Deploy to a virtual environment
1. mkdir ~/virtualenv
2. cd ~/virtualenv
3. virtualenv -p python3 nires
4. source ~/virtualenv/nires/bin/activate
6. cd <PATH_TO_NIRES_DISPLAYTOOLS>
7. python setup.py install
8. source scripts/aliases.sh
9. cd to data directory and run nires displaytool commands