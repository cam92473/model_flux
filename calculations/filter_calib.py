import tkinter as tk

from matplotlib.pyplot import subplot

class Filter(tk.Frame):
    def __init__(self,tab2):
        tk.Frame.__init__(self,master=tab2)
        self.filternamelist = ["f110w","F148W","f160w","f275w","f336w","f475w","f814w","N219M","N279N","F172M","F169M"]
        self.divedistlist = [.001,.01,.001,.01,.01,.01,.01,.01,.001,.001,.001]
        self.plusx = [200,10,100,10,10,15,30,10,2,4,5]
        self.plusy = [.1,2,.1,.02,.05,.05,.05,2,3,2,3]
        self.newplusy = [.0005,.002,.005,.005,.005,.001,.0001,.005,.01,.01,.01]
        from astropy.io import fits
        import numpy as np
        with fits.open("fits_library/ckm05/ckm05_3500.fits") as hdul:
            indata_ang = hdul[1].data["WAVELENGTH"]
            self.indata_nm = np.array([round(i/10,4) for i in indata_ang])
        self.getdata()
        self.interp_and_norm()

    def getdata(self):
        import pandas as pd
        self.xdata = pd.DataFrame()
        self.ydata = pd.DataFrame()
        dflist=[]
        for i in range(11):
            dflist.append(pd.read_csv("11filters/{}.csv".format(self.filternamelist[i]),skiprows=5,delimiter=","))
        self.xdata = self.xdata.assign(f110w_wavelength=dflist[0].iloc[:,0],F148W_wavelength=dflist[1].iloc[:,0],f160w_wavelength=dflist[2].iloc[:,0],f275w_wavelength=dflist[3].iloc[:,0],f336w_wavelength=dflist[4].iloc[:,0],f475w_wavelength=dflist[5].iloc[:,0],f814w_wavelength=dflist[6].iloc[:,0],N219M_wavelength=dflist[7].iloc[:,0],N279N_wavelength=dflist[8].iloc[:,0],F172M_wavelength=dflist[9].iloc[:,0],F169M_wavelength=dflist[10].iloc[:,0])
        self.ydata = self.ydata.assign(f110w_throughput=dflist[0].iloc[:,1],F148W_eff_area=dflist[1].iloc[:,1],f160w_throughput=dflist[2].iloc[:,1],f275w_throughput=dflist[3].iloc[:,1],f336w_throughput=dflist[4].iloc[:,1],f475w_throughput=dflist[5].iloc[:,1],f814w_throughput=dflist[6].iloc[:,1],N219M_eff_area=dflist[7].iloc[:,1],N279N_eff_area=dflist[8].iloc[:,1],F172M_eff_area=dflist[9].iloc[:,1],F169M_eff_area=dflist[10].iloc[:,1])
        #print("xdata \n",self.xdata)
        #print("ydata \n",self.ydata)

    def interp_and_norm(self):
        import pandas as pd
        import numpy as np
        from scipy import integrate
        self.xdata_new = self.xdata
        self.xdata_new.loc[-1] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
        self.xdata_new.loc[135] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
        self.xdata_new.index = self.xdata_new.index + 1
        self.xdata_new = self.xdata_new.sort_index()
 
        self.ydata_new = self.ydata
        self.ydata_new.loc[-1] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
        self.ydata_new.loc[135] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
        self.ydata_new.index = self.ydata_new.index + 1
        self.ydata_new = self.ydata_new.sort_index()

        for i in range(11):
            self.xdata_new.iat[0,i] = self.xdata_new.iat[1,i]-self.divedistlist[i]
            self.xdata_new.iat[self.xdata_new.iloc[:,i].last_valid_index()+1,i] = self.xdata_new.iat[self.xdata_new.iloc[:,i].last_valid_index(),i]+self.divedistlist[i]
            
        for i in range(11):
            self.ydata_new.iat[0,i] = 0
            self.ydata_new.iat[self.ydata_new.iloc[:,i].last_valid_index()+1,i] = 0
           
        #print("xdatanew final: \n",self.xdata_new)
        #print("ydatanew final: \n",self.ydata_new)
  

        self.xcont = pd.DataFrame()
        self.yinterp = pd.DataFrame()
        self.yinterp2 = pd.DataFrame()          
        self.area = []
        self.normalized = pd.DataFrame()
        self.normalized2 = pd.DataFrame()
        self.xcont = self.xcont.assign(f110wcontwlngth = np.linspace(self.xdata_new.iat[0,0],self.xdata_new.iat[self.xdata_new.iloc[:,0].last_valid_index(),0],1000))
        self.xcont = self.xcont.assign(F148Wcontwlngth = np.linspace(self.xdata_new.iat[0,1],self.xdata_new.iat[self.xdata_new.iloc[:,1].last_valid_index(),1],1000))
        self.xcont = self.xcont.assign(f160wcontwlngth = np.linspace(self.xdata_new.iat[0,2],self.xdata_new.iat[self.xdata_new.iloc[:,2].last_valid_index(),2],1000))
        self.xcont = self.xcont.assign(f275wcontwlngth = np.linspace(self.xdata_new.iat[0,3],self.xdata_new.iat[self.xdata_new.iloc[:,3].last_valid_index(),3],1000))
        self.xcont = self.xcont.assign(f336wcontwlngth = np.linspace(self.xdata_new.iat[0,4],self.xdata_new.iat[self.xdata_new.iloc[:,4].last_valid_index(),4],1000))
        self.xcont = self.xcont.assign(f475wcontwlngth = np.linspace(self.xdata_new.iat[0,5],self.xdata_new.iat[self.xdata_new.iloc[:,5].last_valid_index(),5],1000))
        self.xcont = self.xcont.assign(f814wcontwlngth = np.linspace(self.xdata_new.iat[0,6],self.xdata_new.iat[self.xdata_new.iloc[:,6].last_valid_index(),6],1000))
        self.xcont = self.xcont.assign(N219Mcontwlngth = np.linspace(self.xdata_new.iat[0,7],self.xdata_new.iat[self.xdata_new.iloc[:,7].last_valid_index(),7],1000))
        self.xcont = self.xcont.assign(N279Ncontwlngth = np.linspace(self.xdata_new.iat[0,8],self.xdata_new.iat[self.xdata_new.iloc[:,8].last_valid_index(),8],1000))
        self.xcont = self.xcont.assign(F172Mcontwlngth = np.linspace(self.xdata_new.iat[0,9],self.xdata_new.iat[self.xdata_new.iloc[:,9].last_valid_index(),9],1000))
        self.xcont = self.xcont.assign(F169Mcontwlngth = np.linspace(self.xdata_new.iat[0,10],self.xdata_new.iat[self.xdata_new.iloc[:,10].last_valid_index(),10],1000))

        self.f110wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,0] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,0].last_valid_index(),0]:
                self.f110wlist.append(wv)
        #print("f110wlist ",f110wlist)
        self.F148Wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,1] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,1].last_valid_index(),1]:
                self.F148Wlist.append(wv)
        #print("F148Wlist ",F148Wlist)
        self.f160wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,2] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,2].last_valid_index(),2]:
                self.f160wlist.append(wv)
        #print("f160wlist ",f160wlist)
        self.f275wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,3] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,3].last_valid_index(),3]:
                self.f275wlist.append(wv)
        #print("f275wlist ",f275wlist)
        self.f336wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,4] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,4].last_valid_index(),4]:
                self.f336wlist.append(wv)
        #print("f336wlist ",f336wlist)        
        self.f475wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,5] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,5].last_valid_index(),5]:
                self.f475wlist.append(wv)
        #print("f475wlist ",f475wlist)
        self.f814wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,6] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,6].last_valid_index(),6]:
                self.f814wlist.append(wv)
        #print("f814wlist ",f814wlist)
        self.N219Mlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,7] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,7].last_valid_index(),7]:
                self.N219Mlist.append(wv)
        #print("N219Mlist ",N219Mlist)
        self.N279Nlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,8] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,8].last_valid_index(),8]:
                self.N279Nlist.append(wv)
        #print("N279Nlist ",N279Nlist)
        self.F172Mlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,9] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,9].last_valid_index(),9]:
                self.F172Mlist.append(wv)
        #print("F172Mlist ",F172Mlist)
        self.F169Mlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,10] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,10].last_valid_index(),10]:
                self.F169Mlist.append(wv)
        #print("F169Mlist ",F169Mlist)
        
        self.yinterp = self.yinterp.assign(f110winterp = np.interp(self.xcont.iloc[:,0],self.xdata_new.iloc[:,0],self.ydata_new.iloc[:,0]))
        self.yinterp = self.yinterp.assign(F148Winterp = np.interp(self.xcont.iloc[:,1],self.xdata_new.iloc[:,1],self.ydata_new.iloc[:,1]))
        self.yinterp = self.yinterp.assign(f160winterp = np.interp(self.xcont.iloc[:,2],self.xdata_new.iloc[:,2],self.ydata_new.iloc[:,2]))
        self.yinterp = self.yinterp.assign(f275winterp = np.interp(self.xcont.iloc[:,3],self.xdata_new.iloc[:,3],self.ydata_new.iloc[:,3]))
        self.yinterp = self.yinterp.assign(f336winterp = np.interp(self.xcont.iloc[:,4],self.xdata_new.iloc[:,4],self.ydata_new.iloc[:,4]))
        self.yinterp = self.yinterp.assign(f475winterp = np.interp(self.xcont.iloc[:,5],self.xdata_new.iloc[:,5],self.ydata_new.iloc[:,5]))
        self.yinterp = self.yinterp.assign(f814winterp = np.interp(self.xcont.iloc[:,6],self.xdata_new.iloc[:,6],self.ydata_new.iloc[:,6]))
        self.yinterp = self.yinterp.assign(N219Minterp = np.interp(self.xcont.iloc[:,7],self.xdata_new.iloc[:,7],self.ydata_new.iloc[:,7]))
        self.yinterp = self.yinterp.assign(N279Ninterp = np.interp(self.xcont.iloc[:,8],self.xdata_new.iloc[:,8],self.ydata_new.iloc[:,8]))
        self.yinterp = self.yinterp.assign(F172Minterp = np.interp(self.xcont.iloc[:,9],self.xdata_new.iloc[:,9],self.ydata_new.iloc[:,9]))
        self.yinterp = self.yinterp.assign(F169Minterp = np.interp(self.xcont.iloc[:,10],self.xdata_new.iloc[:,10],self.ydata_new.iloc[:,10]))

        F148Wnans = []
        for n in range(len(self.f110wlist)-len(self.F148Wlist)):
            F148Wnans.append(np.nan) 
        f160wnans = []
        for n in range(len(self.f110wlist)-len(self.f160wlist)):
            f160wnans.append(np.nan) 
        f275wnans = []
        for n in range(len(self.f110wlist)-len(self.f275wlist)):
            f275wnans.append(np.nan) 
        f336wnans = []
        for n in range(len(self.f110wlist)-len(self.f336wlist)):
            f336wnans.append(np.nan) 
        f475wnans = []
        for n in range(len(self.f110wlist)-len(self.f475wlist)):
            f475wnans.append(np.nan) 
        f814wnans = []
        for n in range(len(self.f110wlist)-len(self.f814wlist)):
            f814wnans.append(np.nan) 
        N219Mnans = []
        for n in range(len(self.f110wlist)-len(self.N219Mlist)):
            N219Mnans.append(np.nan) 
        N279Nnans = []
        for n in range(len(self.f110wlist)-len(self.N279Nlist)):
            N279Nnans.append(np.nan) 
        F172Mnans = []
        for n in range(len(self.f110wlist)-len(self.F172Mlist)):
            F172Mnans.append(np.nan)
        F169Mnans = []
        for n in range(len(self.f110wlist)-len(self.F169Mlist)):
            F169Mnans.append(np.nan) 

        self.yinterp2 = self.yinterp2.assign(f110winterp = np.interp(self.f110wlist,self.xdata_new.iloc[:,0],self.ydata_new.iloc[:,0]))
        self.yinterp2 = self.yinterp2.assign(F148Winterp = np.append(np.interp(self.F148Wlist,self.xdata_new.iloc[:,1],self.ydata_new.iloc[:,1]),F148Wnans))
        self.yinterp2 = self.yinterp2.assign(f160winterp = np.append(np.interp(self.f160wlist,self.xdata_new.iloc[:,2],self.ydata_new.iloc[:,2]),f160wnans))
        self.yinterp2 = self.yinterp2.assign(f275winterp = np.append(np.interp(self.f275wlist,self.xdata_new.iloc[:,3],self.ydata_new.iloc[:,3]),f275wnans))
        self.yinterp2 = self.yinterp2.assign(f336winterp = np.append(np.interp(self.f336wlist,self.xdata_new.iloc[:,4],self.ydata_new.iloc[:,4]),f336wnans))
        self.yinterp2 = self.yinterp2.assign(f475winterp = np.append(np.interp(self.f475wlist,self.xdata_new.iloc[:,5],self.ydata_new.iloc[:,5]),f475wnans))
        self.yinterp2 = self.yinterp2.assign(f814winterp = np.append(np.interp(self.f814wlist,self.xdata_new.iloc[:,6],self.ydata_new.iloc[:,6]),f814wnans))
        self.yinterp2 = self.yinterp2.assign(N219Minterp = np.append(np.interp(self.N219Mlist,self.xdata_new.iloc[:,7],self.ydata_new.iloc[:,7]),N219Mnans))
        self.yinterp2 = self.yinterp2.assign(N279Ninterp = np.append(np.interp(self.N279Nlist,self.xdata_new.iloc[:,8],self.ydata_new.iloc[:,8]),N279Nnans))
        self.yinterp2 = self.yinterp2.assign(F172Minterp = np.append(np.interp(self.F172Mlist,self.xdata_new.iloc[:,9],self.ydata_new.iloc[:,9]),F172Mnans))
        self.yinterp2 = self.yinterp2.assign(F169Minterp = np.append(np.interp(self.F169Mlist,self.xdata_new.iloc[:,10],self.ydata_new.iloc[:,10]),F169Mnans))

        for i in range(11):
            self.area.append(integrate.trapz(self.yinterp.iloc[:,i],self.xcont.iloc[:,i]))

        self.normalized = self.normalized.assign(f110wnormal = self.yinterp.iloc[:,0]/self.area[0])
        self.normalized = self.normalized.assign(F148Wnormal = self.yinterp.iloc[:,1]/self.area[1])
        self.normalized = self.normalized.assign(f160wnormal = self.yinterp.iloc[:,2]/self.area[2])
        self.normalized = self.normalized.assign(f275wnormal = self.yinterp.iloc[:,3]/self.area[3])
        self.normalized = self.normalized.assign(f336wnormal = self.yinterp.iloc[:,4]/self.area[4])
        self.normalized = self.normalized.assign(f475wnormal = self.yinterp.iloc[:,5]/self.area[5])
        self.normalized = self.normalized.assign(f814wnormal = self.yinterp.iloc[:,6]/self.area[6])
        self.normalized = self.normalized.assign(N219Mnormal = self.yinterp.iloc[:,7]/self.area[7])
        self.normalized = self.normalized.assign(N279Nnormal = self.yinterp.iloc[:,8]/self.area[8])
        self.normalized = self.normalized.assign(F172Mnormal = self.yinterp.iloc[:,9]/self.area[9])
        self.normalized = self.normalized.assign(F169Mnormal = self.yinterp.iloc[:,10]/self.area[10])

        self.normalized2 = self.normalized2.assign(f110w = self.yinterp2.iloc[:,0]/self.area[0])
        self.normalized2 = self.normalized2.assign(F148W = self.yinterp2.iloc[:,1]/self.area[1])
        self.normalized2 = self.normalized2.assign(f160w = self.yinterp2.iloc[:,2]/self.area[2])
        self.normalized2 = self.normalized2.assign(f275w = self.yinterp2.iloc[:,3]/self.area[3])
        self.normalized2 = self.normalized2.assign(f336w = self.yinterp2.iloc[:,4]/self.area[4])
        self.normalized2 = self.normalized2.assign(f475w = self.yinterp2.iloc[:,5]/self.area[5])
        self.normalized2 = self.normalized2.assign(f814w = self.yinterp2.iloc[:,6]/self.area[6])
        self.normalized2 = self.normalized2.assign(N219M = self.yinterp2.iloc[:,7]/self.area[7])
        self.normalized2 = self.normalized2.assign(N279N = self.yinterp2.iloc[:,8]/self.area[8])
        self.normalized2 = self.normalized2.assign(F172M = self.yinterp2.iloc[:,9]/self.area[9])
        self.normalized2 = self.normalized2.assign(F169M = self.yinterp2.iloc[:,10]/self.area[10])
        
        #print("xcont: \n",self.xcont)
        #print("yinterp: \n",self.yinterp)
        #print("yinterp2: \n",self.yinterp2)
        #print("area: \n",self.area)
        #print("NORM: \n",self.normalized)
        #print("NORM2: \n",self.normalized2)
    
    def build_ultimate(self):
        import pandas as pd
        import numpy as np

        F148Wcol = self.normalized2.iloc[:,1]
        for z1 in range(self.indata_nm.tolist().index(self.F148Wlist[0])):
            F148Wcol.loc[-1] = 0
            F148Wcol.index = F148Wcol.index + 1
            F148Wcol = F148Wcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.F148Wlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['F148W'])
            F148Wcol = F148Wcol.append(other.loc[0],ignore_index=True)

        F169Mcol = self.normalized2.iloc[:,10]
        for z1 in range(self.indata_nm.tolist().index(self.F169Mlist[0])):
            F169Mcol.loc[-1] = 0
            F169Mcol.index = F169Mcol.index + 1
            F169Mcol = F169Mcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.F169Mlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['F169M'])
            F169Mcol = F169Mcol.append(other.loc[0],ignore_index=True)

        F172Mcol = self.normalized2.iloc[:,9]
        for z1 in range(self.indata_nm.tolist().index(self.F172Mlist[0])):
            F172Mcol.loc[-1] = 0
            F172Mcol.index = F172Mcol.index + 1
            F172Mcol = F172Mcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.F172Mlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['F172M'])
            F172Mcol = F172Mcol.append(other.loc[0],ignore_index=True)

        N219Mcol = self.normalized2.iloc[:,7]
        for z1 in range(self.indata_nm.tolist().index(self.N219Mlist[0])):
            N219Mcol.loc[-1] = 0
            N219Mcol.index = N219Mcol.index + 1
            N219Mcol = N219Mcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.N219Mlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['N219M'])
            N219Mcol = N219Mcol.append(other.loc[0],ignore_index=True)

        N279Ncol = self.normalized2.iloc[:,8]
        for z1 in range(self.indata_nm.tolist().index(self.N279Nlist[0])):
            N279Ncol.loc[-1] = 0
            N279Ncol.index = N279Ncol.index + 1
            N279Ncol = N279Ncol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.N279Nlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['N279N'])
            N279Ncol = N279Ncol.append(other.loc[0],ignore_index=True)

        f275wcol = self.normalized2.iloc[:,3]
        for z1 in range(self.indata_nm.tolist().index(self.f275wlist[0])):
            f275wcol.loc[-1] = 0
            f275wcol.index = f275wcol.index + 1
            f275wcol = f275wcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.f275wlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['f275w'])
            f275wcol = f275wcol.append(other.loc[0],ignore_index=True)

        f336wcol = self.normalized2.iloc[:,4]
        for z1 in range(self.indata_nm.tolist().index(self.f336wlist[0])):
            f336wcol.loc[-1] = 0
            f336wcol.index = f336wcol.index + 1
            f336wcol = f336wcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.f336wlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['f336w'])
            f336wcol = f336wcol.append(other.loc[0],ignore_index=True)

        f475wcol = self.normalized2.iloc[:,5]
        for z1 in range(self.indata_nm.tolist().index(self.f475wlist[0])):
            f475wcol.loc[-1] = 0
            f475wcol.index = f475wcol.index + 1
            f475wcol = f475wcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.f475wlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['f475w'])
            f475wcol = f475wcol.append(other.loc[0],ignore_index=True)

        f814wcol = self.normalized2.iloc[:,6]
        for z1 in range(self.indata_nm.tolist().index(self.f814wlist[0])):
            f814wcol.loc[-1] = 0
            f814wcol.index = f814wcol.index + 1
            f814wcol = f814wcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.f814wlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['f814w'])
            f814wcol = f814wcol.append(other.loc[0],ignore_index=True)

        f110wcol = self.normalized2.iloc[:,0]
        for z1 in range(self.indata_nm.tolist().index(self.f110wlist[0])):
            f110wcol.loc[-1] = 0
            f110wcol.index = f110wcol.index + 1
            f110wcol = f110wcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.f110wlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['f110w'])
            f110wcol = f110wcol.append(other.loc[0],ignore_index=True)

        f160wcol = self.normalized2.iloc[:,2]
        for z1 in range(self.indata_nm.tolist().index(self.f160wlist[0])):
            f160wcol.loc[-1] = 0
            f160wcol.index = f160wcol.index + 1
            f160wcol = f160wcol.sort_index()
        for z2 in range(1220 - self.indata_nm.tolist().index(self.f160wlist[-1])):
            other = pd.DataFrame(np.array([0]),columns=['f160w'])
            f160wcol = f160wcol.append(other.loc[0],ignore_index=True)

        self.ultimate_normalized = pd.DataFrame()
        self.ultimate_normalized = self.ultimate_normalized.assign(Wavelength = self.indata_nm)
        self.ultimate_normalized = self.ultimate_normalized.assign(F148W = F148Wcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(F169M = F169Mcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(F172M = F172Mcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(N219M = N219Mcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(N279N = N279Ncol)
        self.ultimate_normalized = self.ultimate_normalized.assign(f275w = f275wcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(f336w = f336wcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(f475w = f475wcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(f814w = f814wcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(f110w = f110wcol)
        self.ultimate_normalized = self.ultimate_normalized.assign(f160w = f160wcol)

        #print(self.ultimate_normalized)
    


    def make_scat(self):
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')

        fig = Figure(figsize=(17,14))

        #oldgraphorder = f110w,F148W,f160w,f275w,f336w,f475w,f814w,N219M,N279N,F172M,F169M
        #wantedgraphorder = F148W,F169M,F172M,N219N,N279M,f275w,f336w,f475w,f814w,f110w,f160w
        plotnofilterno = {2:1,3:10,4:9,6:7,7:8,8:3,9:4,11:5,12:6,13:0,14:2}
        for key in plotnofilterno:
            i = plotnofilterno[key]
            ax = fig.add_subplot(5,5,key)   
            ax.set_title("{}".format(self.filternamelist[i]))
            ylabellist = ["throughput","effective area [cm$^2$]","throughput","throughput","throughput","throughput","throughput","effective area [cm$^2$]","effective area [cm$^2$]","effective area [cm$^2$]","effective area [cm$^2$]"]
            ax.set_xlabel("wavelength[nm]")
            ax.set_ylabel(r"{}".format(ylabellist[i]))
            #print("xmin ", float(self.xdata.iat[0,i]-self.plusx[i]))
            #print("xmax ", float(self.xdata.iat[self.xdata.iloc[:,i].last_valid_index(),i])+self.plusx[i])
            #print("ymax ", max(self.ydata.iloc[:,i])+self.plusy[i])
            #                ???                              float(self.xdata_new.iat[self.xdata_new.iloc[:,i].last_valid_index(),i])+self.plusx[i]
            ax.axis([float(self.xdata.iat[0,i]-self.plusx[i]),float(self.xdata_new.iat[self.xdata_new.iloc[:,i].last_valid_index(),i])+self.plusx[i],0,max(self.ydata.iloc[:,i])+self.plusy[i]])
            ax.scatter(self.xdata.iloc[:,i],self.ydata.iloc[:,i])

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row=5,column=5)
        canvas.draw()

    def make_plot(self):
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')

        fig = Figure(figsize=(17,14))

        #oldgraphorder = f110w,F148W,f160w,f275w,f336w,f475w,f814w,N219M,N279N,F172M,F169M
        #wantedgraphorder = F148W,F169M,F172M,N219M,N279N,f275w,f336w,f475w,f814w,f110w,f160w
        plotnofilterno = {2:1,3:10,4:9,6:7,7:8,8:3,9:4,11:5,12:6,13:0,14:2}
        for key in plotnofilterno:
            i = plotnofilterno[key]
            ax = fig.add_subplot(5,5,key)   
            ax.set_title("{}".format(self.filternamelist[i]))
            ylabellist = ["throughput","effective area [cm$^2$]","throughput","throughput","throughput","throughput","throughput","effective area [cm$^2$]","effective area [cm$^2$]","effective area [cm$^2$]","effective area [cm$^2$]"]
            ax.set_xlabel("wavelength[nm]")
            ax.set_ylabel(r"{}".format(ylabellist[i]))
            ax.axis([float(self.xdata_new.iat[0,i]-self.plusx[i]),float(self.xdata_new.iat[self.xdata_new.iloc[:,i].last_valid_index(),i])+self.plusx[i],0,max(self.ydata_new.iloc[:,i])+self.plusy[i]])
            ax.plot(self.xcont.iloc[:,i],self.yinterp.iloc[:,i])

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row=5,column=5)
        canvas.draw()

    def make_norm_plot(self):
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')

        fig = Figure(figsize=(17,14))

        #oldgraphorder = f110w,F148W,f160w,f275w,f336w,f475w,f814w,N219M,N279N,F172M,F169M
        #wantedgraphorder = F148W,F169M,F172M,N219N,N279M,f275w,f336w,f475w,f814w,f110w,f160w
        plotnofilterno = {2:1,3:10,4:9,6:7,7:8,8:3,9:4,11:5,12:6,13:0,14:2}
        for key in plotnofilterno:
            i = plotnofilterno[key]
            ax = fig.add_subplot(5,5,key)   
            ax.set_title("{}".format(self.filternamelist[i]))
            ylabellist = ["throughput","effective area [cm$^2$]","throughput","throughput","throughput","throughput","throughput","effective area [cm$^2$]","effective area [cm$^2$]","effective area [cm$^2$]","effective area [cm$^2$]"]
            ax.set_xlabel("wavelength[nm]")
            ax.set_ylabel(r"{}".format(ylabellist[i]))
            ax.axis([float(self.xdata_new.iat[0,i]-self.plusx[i]),float(self.xdata_new.iat[self.xdata_new.iloc[:,i].last_valid_index(),i])+self.plusx[i],0,max(self.normalized.iloc[:,i])+self.newplusy[i]])
            ax.plot(self.xcont.iloc[:,i],self.normalized.iloc[:,i])

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row=5,column=5)
        canvas.draw()