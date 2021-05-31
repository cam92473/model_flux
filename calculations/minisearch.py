from astropy.io import fits
from calculations.strfunc import grav_out_str,temp_out_str,metal_out_str
import numpy as np


def findgridelements(metal_in):
    
    alltemplist=[3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500,6750,7000,7250,7500,7750,8000,8250,8500,8750,9000,9250,9500,9750,10000,10250,10500,10750,11000,11250,11500,11750,12000,12250,12500,12750,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000,24000,25000,26000,27000,28000,29000,30000,31000,32000,33000,34000,35000,36000,37000,38000,39000,40000,41000,42000,43000,44000,45000,46000,47000,48000,49000,50000]
    allgravlist = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
    tempgravarray = np.zeros((11,76))
    i=0
    for temp_in in alltemplist:
        with fits.open("fits_library/ck{}/ck{}_{}.fits".format(metal_out_str(metal_in), metal_out_str(metal_in),temp_out_str(temp_in))) as hdul:
            j=0
            for grav_in in allgravlist:
                spectrum = hdul[1].data["{}".format(grav_out_str(grav_in))]
                tempgravarray[j][i] = max(spectrum)
                j+=1
        i+=1
    return tempgravarray
            
