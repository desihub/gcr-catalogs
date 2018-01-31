import numpy as np

def isBGS(r):
   bands={}
   bands["r"] = r
   return selec_target_type("BGS", bands)

def isLRG(g,r,z,W1):
   bands={}
   bands["g"]=g
   bands["r"]=r
   bands["z"]=z
   bands["W1"]=W1
   return selec_target_type("LRG", bands)
      

def isELG(g,r,z,W1):
   bands={}
   bands["g"]=g
   bands["r"]=r
   bands["z"]=z
   bands["W1"]=W1
   return selec_target_type("ELG", bands)

def isQSO(g,r,z,W1,W2):
   bands={}
   bands["g"]=g
   bands["r"]=r
   bands["z"]=z
   bands["W1"]=W1
   bands["W2"]=W2
   return selec_target_type("QSO", bands)



def selec_target_type(galtype, bands):
   if galtype == "BGS":
   #need r
      r = bands['r']
      mask = r < 19.45
   elif galtype == "LRG":
  #need g,r,z,w1#
      g,r,z,w1 = [bands[i] for i in ["g","r","z","W1"]]
      mask = ((z-w1)-0.7*(r-z) > -0.6) & ((z-w1)-0.7*(r-z) < 1.0) & (z<20.4)&(z>18)&(r-z>0.8)&(r-z<2.5)& (z-2*(r-z-1.2)>17.4) &(z-2*(r-z-1.2)<19.45)&(((r-z)>1.2)|((g-r)>1.7))
   elif galtype == "ELG":
  #need g,r,z,w1

      g,r,z,w1 = [bands[i] for i in ["g","r","z",'W1']]
      mask = ((z-w1)-0.7*(r-z) > -0.6) & ((z-w1)-0.7*(r-z) < 1.0) & (z<20.4)&(z>18)&(r-z>0.8)&(r-z<2.5)& (z-2*(r-z-1.2)>17.4) &(z-2*(r-z-1.2)<19.45)&(((r-z)>1.2)|((g-r)>1.7))
      mask = (r<23.4)&(r-z>0.3)&(r-z<1.6)&((1.15*(r-z)-0.15)>(g-r))&(1.6-1.2*(r-z)>(g-r))
   elif galtype == "QSO":
  #need g r z w1 w2
      g,r,z,w1,w2 = [bands[i] for i in ["g","r","z","W1","W2"]]
      gflux = 10**((22.5-g)/2.5)
      rflux = 10**((22.5-r)/2.5)
      zflux = 10**((22.5-z)/2.5)
      w1flux = 10**((22.5-w1)/2.5)
      w2flux = 10**((22.5-w2)/2.5)
      wflux = 0.75*w1+0.25*w2
      grzflux =  (gflux + 0.8*rflux + 0.5*zflux) / 2.3
      grzmag = 22.5-2.5*np.log10(grzflux)
      wmag = 22.5-2.5*np.log10(wflux)
      mask = (r<22.7)&(grzmag>17.0)&((g-r) < 1.3)&((r-z) > -0.3)&((r-z) < 1.1)&((grzmag-wmag)>(g-z-1.0))&(w1-w2>-0.4)
   else:
      return None
   return mask

