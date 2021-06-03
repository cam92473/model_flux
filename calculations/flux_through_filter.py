import tkinter as tk

class FTF(tk.Frame):
    def __init__(self,tab3,ext_ys,R_V,final_wave_list,theta_r,ebv,filter,xcont,normalized2,f110wlist,F148Wlist,f160wlist,f275wlist,f336wlist,f475wlist,f814wlist,N219Mlist,N279Nlist,F172Mlist,F169Mlist):
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
        self.f110wlist = f110wlist
        self.F148Wlist = F148Wlist
        self.f160wlist = f160wlist
        self.f275wlist = f275wlist
        self.f336wlist = f336wlist
        self.f475wlist = f475wlist
        self.f814wlist = f814wlist
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
        import numpy as np
        self.Rsp = self.normalized2.loc[:,self.filter]
        self.Rsp = self.Rsp.dropna()

    def sum_over_wavelengths(self):
        
        if self.filter == "f110w":
            self.appropwaves =  self.f110wlist
        elif self.filter == "F148W":
            self.appropwaves =  self.F148Wlist
        elif self.filter == "f160w":
            self.appropwaves =  self.f160wlist
        elif self.filter == "f275w":
            self.appropwaves =  self.f275wlist
        elif self.filter == "f336w":
            self.appropwaves =  self.f336wlist
        elif self.filter == "f475w":
            self.appropwaves =  self.f475wlist
        elif self.filter == "f814w":
            self.appropwaves =  self.f814wlist
        elif self.filter == "N219M":
            self.appropwaves =  self.N219Mlist
        elif self.filter == "N279N":
            self.appropwaves =  self.N279Nlist
        elif self.filter == "F172M":
            self.appropwaves =  self.F172Mlist    
        elif self.filter == "F169M":
            self.appropwaves =  self.F169Mlist
        

        self.areaelements = []
        self.f_list_approp = []
        self.prodfunc=[]

        from astropy.io import fits
        import numpy as np
        with fits.open("fits_library/ckm05/ckm05_3500.fits") as hdul:
            indata_ang = hdul[1].data["WAVELENGTH"]
            indata_nm = np.array([round(i/10,4) for i in indata_ang])

        
        for j in range(len(indata_nm)):
            if indata_nm[j] >= self.appropwaves[0] and indata_nm[j] <= self.appropwaves[-1]:
                self.f_list_approp.append(self.f_list[j])
        #print("self.appropwaves\n",self.appropwaves)


        for lam in range(len(self.appropwaves)):
            self.prodfunc.append(self.f_list_approp[lam]*self.Rsp[lam])

        for lam in range(len(self.appropwaves)-1):
            #print("self.f_list[lam+startind]\n",self.f_list[lam+startind])
            #print("self.Rsp[lam]\n",self.Rsp[lam])
            #print("self.f_list[lam+1+startind]\n",self.f_list[lam+1+startind])
            #print("self.Rsp[lam+1]\n",self.Rsp[lam+1])
            #print("self.f_list[lam+startind]*self.Rsp[lam]+self.f_list[lam+1+startind]*self.Rsp[lam+1])/2\n",(self.f_list[lam+startind]*self.Rsp[lam]+self.f_list[lam+1+startind]*self.Rsp[lam+1])/2)
            #print("(self.appropwaves[lam+1]-self.appropwaves[lam])\n",self.appropwaves[lam+1]-self.appropwaves[lam])
            #print("ALL {}\n".format(lam),(self.f_list[lam+startind]*self.Rsp[lam]+self.f_list[lam+1+startind]*self.Rsp[lam+1])/2*(self.appropwaves[lam+1]-self.appropwaves[lam]))
            self.areaelements.append((self.f_list_approp[lam]*self.Rsp[lam]+self.f_list_approp[lam+1]*self.Rsp[lam+1])/2*(self.appropwaves[lam+1]-self.appropwaves[lam]))
        self.Igral = sum(self.areaelements)
        #print(self.Igral)

