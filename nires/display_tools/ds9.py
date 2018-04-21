import shlex
import subprocess
import time
import logging as lg
from nires.settings import XPAPATH


class Ds9:
    """
    The ds9 class provides wrappers around the unix commands xpaget
    and xpaset. The class is smart enough to automatically detect
    a running ds9 and attach automatically displayed images to it
    """
    title = None

    def __init__(self, title):
        ''' ds9 construction init checks to see if a ds9 called title
        is currently running. If not, a new ds9 instance is created with
        that title'''
        self.title = title
        cmd = shlex.split("{}/xpaset -p {} scale zscale".format(XPAPATH, title))  # set the path from the globals.py

        retcode = subprocess.call(cmd)

        if retcode == 1:
            subprocess.Popen(["ds9", "-title", self.title])
            time.sleep(5)
            if self.title == "Spectrograph":
                self.xpaset("width 1250")
                self.xpaset("height 700")
                self.xpaset("scale zscale")
                self.xpaset("colorbar NO")
                self.xpaset("zoom 0.58 0.58")
            if self.title == "Viewer":
                self.xpaset("width 560")
                self.xpaset("height 512")
                self.xpaset("scale zscale")
                self.xpaset("colorbar NO")
                self.xpaset("zoom 0.5 0.5")               

    def xpaget(self, cmd):
        '''xpaget is a convenience function around unix xpaget'''
        cmd = shlex.split(XPAPATH +"xpaget %s %s" % (self.title, cmd))
        retcode = subprocess.call(cmd)

    def xpapipe(self, cmd, pipein):
        ''' xpapipe is a convenience wrapper around echo pipein | xpaset ...'''
        
        cmd = shlex.split(XPAPATH +"xpaset %s %s" % (self.title, cmd))
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write(pipein)
        p.stdin.flush()
        # print p.communicate()


    def xpaset(self, cmd):
        '''xpaget is a convenience function around unix xpaset'''
                
        xpacmd = XPAPATH +"xpaset -p %s %s" % (self.title, cmd)
        lg.debug(xpacmd)

        cmd = shlex.split(xpacmd)
        retcode = subprocess.call(cmd)
        lg.debug("retcode = %s" % retcode) 


    def frameno(self, frame):
        '''frameno sets the ds9 frame number to [frame]'''
        self.xpaset("frame %i" %frame)

    def open(self, fname, frame):
        '''open opens a fits file [fname] into frame [frame]'''
        ''' added commands that creates, resizes and enables options that are needed for that particular image. ds9setup not required'''
        self.regSave()
        self.frameno(frame)
        self.xpaset("file %s" % fname)
        self.regOpen()

    def wavedisp(self):
        # Changed path names to recognise the regions file'''
        self.xpaset("regions delete all")
        self.xpaset("regions wavelength.reg") #set path from globals.py

    def emissiondisp(self):
        self.xpaset("regions delete all")
        self.xpaset("regions " + globals.codepath + "calibrations/tspec_wavelength.reg")        
        self.xpaset("regions " +globals.codepath +"calibrations/z_emission.reg")

    def zdisp(self):
        self.xpaset("regions delete all")
        self.xpaset("regions " + globals.codepath + "calibrations/tspec_wavelength.reg")
        self.xpaset("regions " + globals.codepath + "calibrations/zregion.reg")

    def cuDisp(self,x,y,size=15,group="foo1",label='1',color="white"):
        font="helvetica 16 normal"
        s="regions command '{box %d %d %d %d # color=%s tag=%s width=2 font=\"%s\" text=\"%s\"}'" \
            % (x,y,size,size,color,group,font,label)
        self.xpaset(s)

    def cuLabel(self,x,y,label="1",group="group1",color="white"):
        font="helvetica 16 normal"
        s="regions command '{text %d %d # color=%s tag=%s width=2 font=\"%s\" text=\"%s\" }'" % (x,y,color,group,font,label)
        self.xpaset(s)

    def cuDel(self,group):
        if group=='all':
                        s="regions delete all" 
        else:
            s="regions group %s delete" % (group)
        self.xpaset(s)

#added a wavelength delete function
    def wavDel(self):
        self.xpaset("regions delete all")

    def cuCent(self,group):
        s="regions group %s select" % (group)
        self.xpaset(s)
        s="regions centroid radius 5 iterations 5"
        self.xpaset(s)
        s="regions selectnone"
        self.xpaset(s)

    def cuInfo(self,group):
        s="regions group %s select" % (group)
        self.xpaset(s)
        self.xpaset("regions getinfo")

    def regSave(self):
        self.xpaset("regions save " + self.title + ".reg")

    def regOpen(self):
        self.xpaset("regions " + self.title + ".reg")

    def lindisp(self,dmin,dmax):
        self.xpaset('scale linear')
        s='scale limits %d %d' % (dmin,dmax)
        self.xpaset(s)
