import numpy as np

def isBGS(r):
   mask = r < 19.45
   return mask

def isLRG(g,r,z,w1):

   gflux = 10**((22.5 - data['mag_g_des']) / 2.5)
   rflux = 10**((22.5 - data['mag_r_des']) / 2.5)
   zflux = 10**((22.5 - data['mag_z_des']) / 2.5)
   w1flux = 10**((22.5 - data['mag_true_W1_wise']) / 2.5)

   primary = np.ones_like(rflux, dtype='?')
   ggood = np.ones_like(gflux, dtype='?')

   mask = primary.copy()
   mask &= (zflux > 10**(0.4*(22.5-20.4))) # z<20.4
   mask &= (zflux < 10**(0.4*(22.5-18))) # z>18
   mask &= (zflux < 10**(0.4*2.5)*rflux) # r-z<2.5
   mask &= (zflux > 10**(0.4*0.8)*rflux) # r-z>0.8


   with np.errstate(over='ignore'):
      mask &= ( (w1flux*rflux**complex(0.7)).real > 
               ((zflux**complex(1.7))*10**(-0.4*0.6)).real  )
      mask &= ( (w1flux*rflux**complex(0.7)).real < 
               ((zflux**complex(1.7))*10**(0.4*1.0)).real )

      mask &= (zflux**3 > 10**(0.4*(22.5+2.4-19.45))*rflux**2)
      mask &= (zflux**3 < 10**(0.4*(22.5+2.4-17.4))*rflux**2)


      mask &= np.logical_or((zflux > 10**(0.4*1.2)*rflux), (ggood & (rflux>10**(0.4*1.7)*gflux)))

   return mask
      

def isELG(g,r,z):

   gflux = 10**((22.5 - data['mag_g_des']) / 2.5)
   rflux = 10**((22.5 - data['mag_r_des']) / 2.5)
   zflux = 10**((22.5 - data['mag_z_des']) / 2.5)

   primary = np.ones_like(gflux, dtype='?')
   mask = primary.copy()
   mask &= rflux > 10**((22.5-23.4)/2.5)                       # r<23.4
   mask &= zflux > rflux * 10**(0.3/2.5)                       # (r-z)>0.3
   mask &= zflux < rflux * 10**(1.6/2.5)                       # (r-z)<1.6

   # Clip to avoid warnings from negative numbers raised to fractional powers.
   rflux = rflux.clip(0)
   zflux = zflux.clip(0)
   mask &= rflux**2.15 < gflux * zflux**1.15 * 10**(-0.15/2.5) # (g-r)<1.15(r-z)-0.15
   mask &= zflux**1.2 < gflux * rflux**0.2 * 10**(1.6/2.5)     # (g-r)<1.6-1.2(r-z)

   return mask

def isQSO(g,r,z,w1,w2):
   gflux = 10**((22.5-g)/2.5)
   rflux = 10**((22.5-r)/2.5)
   zflux = 10**((22.5-z)/2.5)
   w1flux = 10**((22.5-w1)/2.5)
   w2flux = 10**((22.5-w2)/2.5)

   wflux = 0.75* w1flux + 0.25*w2flux
   grzflux = (gflux + 0.8*rflux + 0.5*zflux) / 2.3

   mask = np.ones(len(gflux), dtype='?')
   mask &= rflux > 10**((22.5-22.7)/2.5)    # r<22.7
   mask &= grzflux < 10**((22.5-17)/2.5)    # grz>17
   mask &= rflux < gflux * 10**(1.3/2.5)    # (g-r)<1.3
   mask &= zflux > rflux * 10**(-0.3/2.5)   # (r-z)>-0.3
   mask &= zflux < rflux * 10**(1.1/2.5)    # (r-z)<1.1

   mask &= w2flux > w1flux * 10**(-0.4/2.5) # (W1-W2)>-0.4
   mask &= wflux * gflux > zflux * grzflux * 10**(-1.0/2.5) # (grz-W)>(g-z)-1.0

   # Harder cut on stellar contamination
   mainseq = rflux > gflux * 10**(0.20/2.5)

   # Clip to avoid warnings from negative numbers raised to fractional powers.
   rflux = rflux.clip(0)
   zflux = zflux.clip(0)
   mainseq &= rflux**(1+1.5) > gflux * zflux**1.5 * 10**((-0.100+0.175)/2.5)
   mainseq &= rflux**(1+1.5) < gflux * zflux**1.5 * 10**((+0.100+0.175)/2.5)
   mainseq &= w2flux < w1flux * 10**(0.3/2.5)
   mask &= ~mainseq

   return mask



