import tkinter as tk

from matplotlib.pyplot import subplot

class Filter(tk.Frame):
    def __init__(self,tab2):
        tk.Frame.__init__(self,master=tab2)
        self.filternamelist = ["F110W","F148W","F160W","F275W","F336W","F475W","F814W","N219M","N279N","F172M","F169M"]
        self.divedistlist = [.001,.01,.001,1,1,1,1,.01,.001,.001,.001]
        self.plusx = [200,10,100,100,100,150,300,10,2,4,5]
        self.plusy = [.1,2,.1,.02,.05,.05,.05,2,3,2,3]
        self.newplusy = [.0005,.002,.0005,.0005,.0005,.0001,.0001,.005,.01,.01,.01]
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
        self.xdata = self.xdata.assign(F110W_wavelength=dflist[0].iloc[:,0],F148W_wavelength=dflist[1].iloc[:,0],F160W_wavelength=dflist[2].iloc[:,0],F275W_wavelength=dflist[3].iloc[:,0],F336W_wavelength=dflist[4].iloc[:,0],F475W_wavelength=dflist[5].iloc[:,0],F814W_wavelength=dflist[6].iloc[:,0],N219M_wavelength=dflist[7].iloc[:,0],N279N_wavelength=dflist[8].iloc[:,0],F172M_wavelength=dflist[9].iloc[:,0],F169M_wavelength=dflist[10].iloc[:,0])
        self.ydata = self.ydata.assign(F110W_throughput=dflist[0].iloc[:,1],F148W_eff_area=dflist[1].iloc[:,1],F160W_throughput=dflist[2].iloc[:,1],F275W_throughput=dflist[3].iloc[:,1],F336W_throughput=dflist[4].iloc[:,1],F475W_throughput=dflist[5].iloc[:,1],F814W_throughput=dflist[6].iloc[:,1],N219M_eff_area=dflist[7].iloc[:,1],N279N_eff_area=dflist[8].iloc[:,1],F172M_eff_area=dflist[9].iloc[:,1],F169M_eff_area=dflist[10].iloc[:,1])
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
        self.xcont = self.xcont.assign(F110Wcontwlngth = np.linspace(self.xdata_new.iat[0,0],self.xdata_new.iat[self.xdata_new.iloc[:,0].last_valid_index(),0],1000))
        self.xcont = self.xcont.assign(F148Wcontwlngth = np.linspace(self.xdata_new.iat[0,1],self.xdata_new.iat[self.xdata_new.iloc[:,1].last_valid_index(),1],1000))
        self.xcont = self.xcont.assign(F160Wcontwlngth = np.linspace(self.xdata_new.iat[0,2],self.xdata_new.iat[self.xdata_new.iloc[:,2].last_valid_index(),2],1000))
        self.xcont = self.xcont.assign(F275Wcontwlngth = np.linspace(self.xdata_new.iat[0,3],self.xdata_new.iat[self.xdata_new.iloc[:,3].last_valid_index(),3],1000))
        self.xcont = self.xcont.assign(F336Wcontwlngth = np.linspace(self.xdata_new.iat[0,4],self.xdata_new.iat[self.xdata_new.iloc[:,4].last_valid_index(),4],1000))
        self.xcont = self.xcont.assign(F475Wcontwlngth = np.linspace(self.xdata_new.iat[0,5],self.xdata_new.iat[self.xdata_new.iloc[:,5].last_valid_index(),5],1000))
        self.xcont = self.xcont.assign(F814Wcontwlngth = np.linspace(self.xdata_new.iat[0,6],self.xdata_new.iat[self.xdata_new.iloc[:,6].last_valid_index(),6],1000))
        self.xcont = self.xcont.assign(N219Mcontwlngth = np.linspace(self.xdata_new.iat[0,7],self.xdata_new.iat[self.xdata_new.iloc[:,7].last_valid_index(),7],1000))
        self.xcont = self.xcont.assign(N279Ncontwlngth = np.linspace(self.xdata_new.iat[0,8],self.xdata_new.iat[self.xdata_new.iloc[:,8].last_valid_index(),8],1000))
        self.xcont = self.xcont.assign(F172Mcontwlngth = np.linspace(self.xdata_new.iat[0,9],self.xdata_new.iat[self.xdata_new.iloc[:,9].last_valid_index(),9],1000))
        self.xcont = self.xcont.assign(F169Mcontwlngth = np.linspace(self.xdata_new.iat[0,10],self.xdata_new.iat[self.xdata_new.iloc[:,10].last_valid_index(),10],1000))

        self.F110Wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,0] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,0].last_valid_index(),0]:
                self.F110Wlist.append(wv)
        #print("F110Wlist ",F110Wlist)
        self.F148Wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,1] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,1].last_valid_index(),1]:
                self.F148Wlist.append(wv)
        #print("F148Wlist ",F148Wlist)
        self.F160Wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,2] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,2].last_valid_index(),2]:
                self.F160Wlist.append(wv)
        #print("F160Wlist ",F160Wlist)
        self.F275Wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,3] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,3].last_valid_index(),3]:
                self.F275Wlist.append(wv)
        #print("F275Wlist ",F275Wlist)
        self.F336Wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,4] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,4].last_valid_index(),4]:
                self.F336Wlist.append(wv)
        #print("F336Wlist ",F336Wlist)        
        self.F475Wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,5] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,5].last_valid_index(),5]:
                self.F475Wlist.append(wv)
        #print("F475Wlist ",F475Wlist)
        self.F814Wlist = []
        for wv in self.indata_nm:
            if wv > self.xdata_new.iloc[0,6] and wv < self.xdata_new.iloc[self.xdata_new.iloc[:,6].last_valid_index(),6]:
                self.F814Wlist.append(wv)
        #print("F814Wlist ",F814Wlist)
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
        
        self.yinterp = self.yinterp.assign(F110Winterp = np.interp(self.xcont.iloc[:,0],self.xdata_new.iloc[:,0],self.ydata_new.iloc[:,0]))
        self.yinterp = self.yinterp.assign(F148Winterp = np.interp(self.xcont.iloc[:,1],self.xdata_new.iloc[:,1],self.ydata_new.iloc[:,1]))
        self.yinterp = self.yinterp.assign(F160Winterp = np.interp(self.xcont.iloc[:,2],self.xdata_new.iloc[:,2],self.ydata_new.iloc[:,2]))
        self.yinterp = self.yinterp.assign(F275Winterp = np.interp(self.xcont.iloc[:,3],self.xdata_new.iloc[:,3],self.ydata_new.iloc[:,3]))
        self.yinterp = self.yinterp.assign(F336Winterp = np.interp(self.xcont.iloc[:,4],self.xdata_new.iloc[:,4],self.ydata_new.iloc[:,4]))
        self.yinterp = self.yinterp.assign(F475Winterp = np.interp(self.xcont.iloc[:,5],self.xdata_new.iloc[:,5],self.ydata_new.iloc[:,5]))
        self.yinterp = self.yinterp.assign(F814Winterp = np.interp(self.xcont.iloc[:,6],self.xdata_new.iloc[:,6],self.ydata_new.iloc[:,6]))
        self.yinterp = self.yinterp.assign(N219Minterp = np.interp(self.xcont.iloc[:,7],self.xdata_new.iloc[:,7],self.ydata_new.iloc[:,7]))
        self.yinterp = self.yinterp.assign(N279Ninterp = np.interp(self.xcont.iloc[:,8],self.xdata_new.iloc[:,8],self.ydata_new.iloc[:,8]))
        self.yinterp = self.yinterp.assign(F172Minterp = np.interp(self.xcont.iloc[:,9],self.xdata_new.iloc[:,9],self.ydata_new.iloc[:,9]))
        self.yinterp = self.yinterp.assign(F169Minterp = np.interp(self.xcont.iloc[:,10],self.xdata_new.iloc[:,10],self.ydata_new.iloc[:,10]))

        F148Wnans = []
        for n in range(len(self.F110Wlist)-len(self.F148Wlist)):
            F148Wnans.append(np.nan) 
        F160Wnans = []
        for n in range(len(self.F110Wlist)-len(self.F160Wlist)):
            F160Wnans.append(np.nan) 
        F275Wnans = []
        for n in range(len(self.F110Wlist)-len(self.F275Wlist)):
            F275Wnans.append(np.nan) 
        F336Wnans = []
        for n in range(len(self.F110Wlist)-len(self.F336Wlist)):
            F336Wnans.append(np.nan) 
        F475Wnans = []
        for n in range(len(self.F110Wlist)-len(self.F475Wlist)):
            F475Wnans.append(np.nan) 
        F814Wnans = []
        for n in range(len(self.F110Wlist)-len(self.F814Wlist)):
            F814Wnans.append(np.nan) 
        N219Mnans = []
        for n in range(len(self.F110Wlist)-len(self.N219Mlist)):
            N219Mnans.append(np.nan) 
        N279Nnans = []
        for n in range(len(self.F110Wlist)-len(self.N279Nlist)):
            N279Nnans.append(np.nan) 
        F172Mnans = []
        for n in range(len(self.F110Wlist)-len(self.F172Mlist)):
            F172Mnans.append(np.nan)
        F169Mnans = []
        for n in range(len(self.F110Wlist)-len(self.F169Mlist)):
            F169Mnans.append(np.nan) 

        self.yinterp2 = self.yinterp2.assign(F110Winterp = np.interp(self.F110Wlist,self.xdata_new.iloc[:,0],self.ydata_new.iloc[:,0]))
        self.yinterp2 = self.yinterp2.assign(F148Winterp = np.append(np.interp(self.F148Wlist,self.xdata_new.iloc[:,1],self.ydata_new.iloc[:,1]),F148Wnans))
        self.yinterp2 = self.yinterp2.assign(F160Winterp = np.append(np.interp(self.F160Wlist,self.xdata_new.iloc[:,2],self.ydata_new.iloc[:,2]),F160Wnans))
        self.yinterp2 = self.yinterp2.assign(F275Winterp = np.append(np.interp(self.F275Wlist,self.xdata_new.iloc[:,3],self.ydata_new.iloc[:,3]),F275Wnans))
        self.yinterp2 = self.yinterp2.assign(F336Winterp = np.append(np.interp(self.F336Wlist,self.xdata_new.iloc[:,4],self.ydata_new.iloc[:,4]),F336Wnans))
        self.yinterp2 = self.yinterp2.assign(F475Winterp = np.append(np.interp(self.F475Wlist,self.xdata_new.iloc[:,5],self.ydata_new.iloc[:,5]),F475Wnans))
        self.yinterp2 = self.yinterp2.assign(F814Winterp = np.append(np.interp(self.F814Wlist,self.xdata_new.iloc[:,6],self.ydata_new.iloc[:,6]),F814Wnans))
        self.yinterp2 = self.yinterp2.assign(N219Minterp = np.append(np.interp(self.N219Mlist,self.xdata_new.iloc[:,7],self.ydata_new.iloc[:,7]),N219Mnans))
        self.yinterp2 = self.yinterp2.assign(N279Ninterp = np.append(np.interp(self.N279Nlist,self.xdata_new.iloc[:,8],self.ydata_new.iloc[:,8]),N279Nnans))
        self.yinterp2 = self.yinterp2.assign(F172Minterp = np.append(np.interp(self.F172Mlist,self.xdata_new.iloc[:,9],self.ydata_new.iloc[:,9]),F172Mnans))
        self.yinterp2 = self.yinterp2.assign(F169Minterp = np.append(np.interp(self.F169Mlist,self.xdata_new.iloc[:,10],self.ydata_new.iloc[:,10]),F169Mnans))

        for i in range(11):
            self.area.append(integrate.trapz(self.yinterp.iloc[:,i],self.xcont.iloc[:,i]))

        self.normalized = self.normalized.assign(F110Wnormal = self.yinterp.iloc[:,0]/self.area[0])
        self.normalized = self.normalized.assign(F148Wnormal = self.yinterp.iloc[:,1]/self.area[1])
        self.normalized = self.normalized.assign(F160Wnormal = self.yinterp.iloc[:,2]/self.area[2])
        self.normalized = self.normalized.assign(F275Wnormal = self.yinterp.iloc[:,3]/self.area[3])
        self.normalized = self.normalized.assign(F336Wnormal = self.yinterp.iloc[:,4]/self.area[4])
        self.normalized = self.normalized.assign(F475Wnormal = self.yinterp.iloc[:,5]/self.area[5])
        self.normalized = self.normalized.assign(F814Wnormal = self.yinterp.iloc[:,6]/self.area[6])
        self.normalized = self.normalized.assign(N219Mnormal = self.yinterp.iloc[:,7]/self.area[7])
        self.normalized = self.normalized.assign(N279Nnormal = self.yinterp.iloc[:,8]/self.area[8])
        self.normalized = self.normalized.assign(F172Mnormal = self.yinterp.iloc[:,9]/self.area[9])
        self.normalized = self.normalized.assign(F169Mnormal = self.yinterp.iloc[:,10]/self.area[10])

        self.normalized2 = self.normalized2.assign(F110W = self.yinterp2.iloc[:,0]/self.area[0])
        self.normalized2 = self.normalized2.assign(F148W = self.yinterp2.iloc[:,1]/self.area[1])
        self.normalized2 = self.normalized2.assign(F160W = self.yinterp2.iloc[:,2]/self.area[2])
        self.normalized2 = self.normalized2.assign(F275W = self.yinterp2.iloc[:,3]/self.area[3])
        self.normalized2 = self.normalized2.assign(F336W = self.yinterp2.iloc[:,4]/self.area[4])
        self.normalized2 = self.normalized2.assign(F475W = self.yinterp2.iloc[:,5]/self.area[5])
        self.normalized2 = self.normalized2.assign(F814W = self.yinterp2.iloc[:,6]/self.area[6])
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

    def make_scat(self):
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')

        fig = Figure(figsize=(17,14))

        for i,axno in enumerate([2,3,4,6,7,8,9,11,12,13,14]):
            ax = fig.add_subplot(5,5,axno)   
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

        for i,axno in enumerate([2,3,4,6,7,8,9,11,12,13,14]):
            ax = fig.add_subplot(5,5,axno)   
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

        for i,axno in enumerate([2,3,4,6,7,8,9,11,12,13,14]):
            ax = fig.add_subplot(5,5,axno)   
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