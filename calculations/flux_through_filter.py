import tkinter as tk

class FTF(tk.Frame):
    def __init__(self,tab3,ext_ys,R_V,final_wave_list,theta_r,ebv,filter,xcont,normalized2,F110Wlist,F148Wlist,F160Wlist,F275Wlist,F336Wlist,F475Wlist,F814Wlist,N219Mlist,N279Nlist,F172Mlist,F169Mlist):
        tk.Frame.__init__(self,master=tab3)
        import numpy as np
        self.ext_ys = np.flipud(ext_ys)
        self.R_V = R_V
        self.final_wave_list = final_wave_list
        self.theta_r = theta_r
        self.ebv = ebv
        self.filter = filter
        self.xcont = xcont
        self.normalized2 = normalized2
        self.F110Wlist = F110Wlist
        self.F148Wlist = F148Wlist
        self.F160Wlist = F160Wlist
        self.F275Wlist = F275Wlist
        self.F336Wlist = F336Wlist
        self.F475Wlist = F475Wlist
        self.F814Wlist = F814Wlist
        self.N219Mlist = N219Mlist
        self.N279Nlist = N279Nlist
        self.F172Mlist = F172Mlist
        self.F169Mlist = F169Mlist
        self.build_lowercase_f()
        self.get_Rsp()

    def build_lowercase_f(self):
        self.f_list = []
        #print("final wave list\n",self.final_wave_list)
        #print("ext ys\n",self.ext_ys)
        for i in range(1221):
            self.f_list.append(self.final_wave_list[i]*self.theta_r**2*10**((-0.4*self.ebv)*(self.ext_ys[i]+self.R_V)))
        #print("flist\n",self.f_list)

    def get_Rsp(self):
        self.Rsp = self.normalized2.loc[:,self.filter]

    def sum_over_wavelengths(self):
        
        if self.filter == "F110W":
            appropwaves =  self.F110Wlist
        elif self.filter == "F148W":
            appropwaves =  self.F148Wlist
        elif self.filter == "F160W":
            appropwaves =  self.F160list
        elif self.filter == "F275W":
            appropwaves =  self.F275Wlist
        elif self.filter == "F336W":
            appropwaves =  self.F336Wlist
        elif self.filter == "F475W":
            appropwaves =  self.F475Wlist
        elif self.filter == "F814W":
            appropwaves =  self.F814Wlist
        elif self.filter == "N219M":
            appropwaves =  self.N219Mlist
        elif self.filter == "N279N":
            appropwaves =  self.N279Nlist
        elif self.filter == "F169M":
            appropwaves =  self.F169Mlist

        #print("appropwaves\n",appropwaves)
        areaelements = []
        from astropy.io import fits
        import numpy as np
        with fits.open("fits_library/ckm05/ckm05_3500.fits") as hdul:
            indata_ang = hdul[1].data["WAVELENGTH"]
            indata_nm = np.array([round(i/10,4) for i in indata_ang]).tolist()
            #print("indata_nm\n",indata_nm)
        startind = indata_nm.index(appropwaves[0])
        #print("startind\n",startind)
        #print("start here\n",indata_nm[startind])
        for lam in range(len(appropwaves)-1):
            #print("self.f_list[lam+startind]\n",self.f_list[lam+startind])
            #print("self.Rsp[lam]\n",self.Rsp[lam])
            #print("self.f_list[lam+1+startind]\n",self.f_list[lam+1+startind])
            #print("self.Rsp[lam+1]\n",self.Rsp[lam+1])
            #print("self.f_list[lam+startind]*self.Rsp[lam]+self.f_list[lam+1+startind]*self.Rsp[lam+1])/2\n",(self.f_list[lam+startind]*self.Rsp[lam]+self.f_list[lam+1+startind]*self.Rsp[lam+1])/2)
            #print("(appropwaves[lam+1]-appropwaves[lam])\n",appropwaves[lam+1]-appropwaves[lam])
            #print("ALL {}\n".format(lam),(self.f_list[lam+startind]*self.Rsp[lam]+self.f_list[lam+1+startind]*self.Rsp[lam+1])/2*(appropwaves[lam+1]-appropwaves[lam]))
            areaelements.append((self.f_list[lam+startind]*self.Rsp[lam]+self.f_list[lam+1+startind]*self.Rsp[lam+1])/2*(appropwaves[lam+1]-appropwaves[lam]))
        self.Igral = sum(areaelements)
        #print(self.Igral)

