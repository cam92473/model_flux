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
        #print("xdata ",self.xdata)
        #print("ydata ",self.ydata)

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
           
        #print("\nxdatanew final: ",self.xdata_new)
        #print("\nydatanew final: ",self.ydata_new)
  

        self.xcont = pd.DataFrame()
        self.yinterp = pd.DataFrame()        
        self.area = []
        self.normalized = pd.DataFrame()
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
        
        #print("xcont: ",self.xcont)
        #print("yinterp: ",self.yinterp)
        #print("area: ",self.area)
        #print("NORM: ",self.normalized)

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
            print("xmin ", float(self.xdata.iat[0,i]-self.plusx[i]))
            print("xmax ", float(self.xdata.iat[self.xdata.iloc[:,i].last_valid_index(),i])+self.plusx[i])
            print("ymax ", max(self.ydata.iloc[:,i])+self.plusy[i])
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