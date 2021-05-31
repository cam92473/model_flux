import tkinter as tk


class Extinction(tk.Frame):
    def __init__(self,tab1,c1,c2,c4,c5,x0,c3,gamma,O3,O2,O1,k_IR,R_V):
        tk.Frame.__init__(self,master=tab1)
        self.c5 = c5
        self.R_V = R_V
        from calculations.extfunctions import ExtinctionFunctions
        self.extinctionfunctions = ExtinctionFunctions(c1,c2,c4,c5,x0,c3,gamma,O3,O2,O1,k_IR,R_V)

    def build_axes(self):
        import numpy as np
        from astropy.io import fits

        with fits.open("fits_library/ckm05/ckm05_3500.fits") as hdul:
            indata_nm = hdul[1].data["WAVELENGTH"]

        y_vals=[]

        for wvlngth in indata_nm:
            if wvlngth > 1000:
                y_vals.append(self.extinctionfunctions.ir_model(1000 / wvlngth))
            elif wvlngth <= 1000 and wvlngth > 270:
                y_vals.append(self.extinctionfunctions.opt_model(1000 / wvlngth))
            elif wvlngth <= 270 and wvlngth > 1000/self.c5:
                y_vals.append(self.extinctionfunctions.uv_lng_model(1000 / wvlngth))
            elif wvlngth <= 1000/self.c5:
                y_vals.append(self.extinctionfunctions.uv_srt_model(1000 / wvlngth))

        x_axis = (1000/indata_nm)
        y_axis = np.array(y_vals)
        grapharray_unsrt = np.column_stack((x_axis,y_axis))
        self.grapharray_xsrt = grapharray_unsrt[np.argsort(grapharray_unsrt[:, 0])]

    def plot_wavelengths(self,array):
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')
        fig = Figure(figsize=(4.2,3.5))
        abc = fig.add_subplot(111)
        abc.scatter(array[:,0],array[:,1])

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack()
        canvas.draw()


class Interpo():
    def __init__(self,grav,temp,metal,interp):
        self.grav = grav
        self.temp = temp
        self.metal = metal
        self.interp = interp

    def run(self):
        from calculations.vertices import get_corners
        from calculations.interpolate import Interpolator
        grav_lo,grav_hi,temp_lo,temp_hi,metal_lo,metal_hi,interp_par = get_corners(self.grav,self.temp,self.metal,self.interp)
        interpolator = Interpolator(self.grav,self.temp,self.metal,grav_lo,grav_hi,temp_lo,temp_hi,metal_lo,metal_hi,interp_par)
        interpolator.interpolate()
        self.final_wave_list = interpolator.final_wave_list
        

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=0)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def open_popup(outslider):
    popup = Popup(outslider)

class Popup(tk.Toplevel):
    def __init__(self,outslider):
        super().__init__()
        self.configure(bg="gray95")
        self.geometry("1900x400+0+300")
        self.outslider = outslider
        self.resolution()
        self.configure_tight_grid()
        self.create_display()

    def resolution(self):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    def configure_tight_grid(self):
        grid_rc = [[],[]]
        for f in range(11):
            grid_rc[0].append(5)
        for f in range(76):
            grid_rc[1].append(5)
        for row in range(len(grid_rc[0])):
            self.rowconfigure(row,minsize=grid_rc[0][row])
        for column in range(len(grid_rc[1])):
            self.columnconfigure(column,minsize=grid_rc[1][column])

    def get_image(self,filepath,dimx,dimy):
        from PIL import Image, ImageTk
        image = Image.open("{}".format(filepath))
        image_rsize = image.resize((dimx,dimy))
        image_rsize_conv = ImageTk.PhotoImage(image_rsize)
        return image_rsize_conv
   
    def create_display(self):
        from calculations.minisearch import findgridelements
        if self.outslider.get() == 0:
            self.title("Abundacy = {}".format(0.5))
            tempgravarray = findgridelements(0.5)
        elif self.outslider.get() == 1:
            self.title("Abundacy = {}".format(0.2))
            tempgravarray = findgridelements(0.2)
        elif self.outslider.get() == 2:
            self.title("Abundacy = {}".format(0))
            tempgravarray = findgridelements(0)
        elif self.outslider.get() == 3:
            self.title("Abundacy = {}".format(-0.5))
            tempgravarray = findgridelements(-0.5)
        elif self.outslider.get() == 4:
            self.title("Abundacy = {}".format(-1.0))
            tempgravarray = findgridelements(-1.0)
        elif self.outslider.get() == 5:
            self.title("Abundacy = {}".format(-1.5))
            tempgravarray = findgridelements(-1.5)
        elif self.outslider.get() == 6:
            self.title("Abundacy = {}".format(-2.0))
            tempgravarray = findgridelements(-2.0)
        elif self.outslider.get() == 7:
            self.title("Abundacy = {}".format(-2.5))
            tempgravarray = findgridelements(-2.5)   
        red = self.get_image("images/red.PNG",10,10)
        green = self.get_image("images/green.PNG",10,10)
        self.red = red
        self.green = green
        collist=["3.5","3.75","4","4.25","4.5","4.75","5","5.25","5.5","5.75","6","6.25","6.5","6.75","7","7.25","7.5","7.75","8","8.25","8.5","8.75","9","9.25","9.5","9.75","10","10.25","10.5","10.75","11","11.25","11.5","11.75","12","12.25","12.5","12.75","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50"]
        rowlist = ["0.0","0.5","1.0","1.5","2.0","2.5","3.0","3.5","4.0","4.5","5.0"]
        for column in range(76):
            uselessbucket = []
            uselessbucket.append(tk.Label(self, text="{}".format(collist[column]), borderwidth=0, highlightthickness=0).grid(row=49,column=column+3))
        for row in range(11):
            uselessbucket = []
            uselessbucket.append(tk.Label(self, text="{}".format(rowlist[row]), borderwidth=0, highlightthickness=0).grid(row=row+50,column=2))
        for row in range(11):
            uselessbucket = []
            for column in range(76):
                if tempgravarray[row][column] > 0:
                    uselessbucket.append(tk.Label(self, image=green, borderwidth=0, highlightthickness=0))
                else:
                    uselessbucket.append(tk.Label(self, image=red, borderwidth=0, highlightthickness=0))
                uselessbucket[column].grid(row=row+50,column=column+3,padx=7,pady=7)
                CreateToolTip(uselessbucket[column], text = '{}'.format(tempgravarray[row][column]))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Model Flux Calculator")
        self.geometry("1380x950+300+30")
        self.configure(bg="gray95")
        self.build_tabs()
        self.resolution()
        self.create_tab1()
        self.create_tab2()
        
        
    def create_tab1(self):
        self.configure_grid1(testlabels=False)
        self.build_cube_and_gadgets()
        self.build_entries_etc()
        self.build_wavebox()
        self.build_seperator()
        self.build_parameters()
        self.build_flambabox()

    def create_tab2(self):
        self.configure_grid2(testlabels=False)
        from calculations.filter_calib import Filter
        filterplot = Filter(self.tab2)
        filterplot.place(x=0,y=0)

        buttframe = tk.Frame(self.tab2)
        buttframe.place(x=40,y=40)
        scatbutton = tk.Button(buttframe,text="Original filter model data",font=("Arial",12),command=filterplot.make_scat,bg='white')
        scatbutton.pack(side=tk.TOP,ipadx=50,ipady=20)
        plotbutton = tk.Button(buttframe,text="Linearly interpolated",font=("Arial",12),command=filterplot.make_plot,bg='white')
        plotbutton.pack(ipadx=65,ipady=20)
        normbutton = tk.Button(buttframe,text="Normalized linearly interpolated",font=("Arial",12),command = filterplot.make_norm_plot,bg='white')
        normbutton.pack(side=tk.BOTTOM,ipadx=26,ipady=20)

    def build_tabs(self):
        from tkinter import ttk
        ntbook = ttk.Notebook(self)
        ntbook.place(x=0,y=0)
        self.tab1 = ttk.Frame(ntbook,width=1380,height=1500)
        self.tab2 = ttk.Frame(ntbook,width=2000,height=1500)
        self.tab1.pack()
        self.tab2.pack()
        ntbook.add(self.tab1,text="f_lambda")
        ntbook.add(self.tab2,text="filters")
        bgcanvas1 = tk.Canvas(self.tab1,bg="light steel blue",width=1380,height=1500).place(x=0,y=0)
        bgcanvas2 = tk.Canvas(self.tab2,bg="white",width=2000,height=1500).place(x=0,y=0)


    def resolution(self):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    def configure_grid1(self,testlabels=None):
        grid_rc_1 = [[100,100,100,100,100,100,100,100,100],[100,100,100,100,110,110,100,100,100,100,100,100,100,100,100,100]]
        for row in range(len(grid_rc_1[0])):
            self.tab1.rowconfigure(row,minsize=grid_rc_1[0][row])
        for column in range(len(grid_rc_1[1])):
            self.tab1.columnconfigure(column,minsize=grid_rc_1[1][column])
        if testlabels == True:
            testlabellist=[]
            for row in range(len(grid_rc_1[0])):
                for column in range(len(grid_rc_1[1])):
                    testlabellist.append(tk.Label(self.tab1,text="{},{}".format(row,column)).grid(row=row,column=column))
    
    def configure_grid2(self,testlabels=None):
        grid_rc_2 = [[100,100,100,100,100,100,100,100,100],[115,115,115,115,115,115,115,115,115,115,115,115,115,115]]
        for row in range(len(grid_rc_2[0])):
            self.tab2.rowconfigure(row,minsize=grid_rc_2[0][row])
        for column in range(len(grid_rc_2[1])):
            self.tab2.columnconfigure(column,minsize=grid_rc_2[1][column])
        if testlabels == True:
            testlabellist=[]
            for row in range(len(grid_rc_2[0])):
                for column in range(len(grid_rc_2[1])):
                    testlabellist.append(tk.Label(self.tab2,text="{},{}".format(row,column)).grid(row=row,column=column))

    def get_image(self,filepath,dimx,dimy):
        from PIL import Image, ImageTk
        image = Image.open("{}".format(filepath))
        image_rsize = image.resize((dimx,dimy))
        image_rsize_conv = ImageTk.PhotoImage(image_rsize)
        return image_rsize_conv

    def change_image(self,dummy):
        uselessbucket = []
        self.cubeimage.destroy()
        if self.outslider.get() == 0:
            uselessbucket.append(tk.Label(self.tab1,image=self.cubep05).place(x=140,y=100))
        elif self.outslider.get() == 1:
            uselessbucket.append(tk.Label(self.tab1,image=self.cubep02).place(x=140,y=100))
        elif self.outslider.get() == 2:
            uselessbucket.append(tk.Label(self.tab1,image=self.cubep00).place(x=140,y=100))
        elif self.outslider.get() == 3:
            uselessbucket.append(tk.Label(self.tab1,image=self.cubem05).place(x=140,y=100))
        elif self.outslider.get() == 4:
            uselessbucket.append(tk.Label(self.tab1,image=self.cubem10).place(x=140,y=100))
        elif self.outslider.get() == 5:
            uselessbucket.append(tk.Label(self.tab1,image=self.cubem15).place(x=140,y=100))
        elif self.outslider.get() == 6:
            uselessbucket.append(tk.Label(self.tab1,image=self.cubem20).place(x=140,y=100))
        elif self.outslider.get() == 7:
            uselessbucket.append(tk.Label(self.tab1,image=self.cubem25).place(x=140,y=100))


    def build_cube_and_gadgets(self):
        self.cubem25 = self.get_image("images/cubem25.PNG",340,300)
        self.cubem20 = self.get_image("images/cubem20.PNG",340,300)
        self.cubem15 = self.get_image("images/cubem15.PNG",340,300)
        self.cubem10 = self.get_image("images/cubem10.PNG",340,300)
        self.cubem05 = self.get_image("images/cubem05.PNG",340,300)
        self.cubep00 = self.get_image("images/cubep00.PNG",340,300)
        self.cubep02 = self.get_image("images/cubep02.PNG",340,300)
        self.cubep05 = self.get_image("images/cubep05.PNG",340,300)
        self.cubeimage = tk.Label(self.tab1,image=self.cubem25)
        self.cubeimage.place(x=140,y=100)
        sliderpack = tk.LabelFrame(self.tab1)
        sliderpack.place(x=82,y=102)
        self.outslider = tk.IntVar()
        cubeslider = tk.Scale(sliderpack,from_=0,to=7,length=290, orient=tk.VERTICAL,variable=self.outslider,showvalue = 0,command=self.change_image)
        cubeslider.pack(padx=0,side=tk.RIGHT)
        cubeslider.set(7)
        slidelabel0 = tk.Label(sliderpack,text="0.5",font=("Arial",9)).pack(padx = 2, pady=7)
        slidelabel1 = tk.Label(sliderpack,text="0.2",font=("Arial",9)).pack(padx = 2, pady=8)
        slidelabel2 = tk.Label(sliderpack,text="-0.0",font=("Arial",9)).pack(padx = 2, pady=8)
        slidelabel3 = tk.Label(sliderpack,text="-0.5",font=("Arial",9)).pack(padx = 2, pady=8)
        slidelabel4 = tk.Label(sliderpack,text="-1.0",font=("Arial",9)).pack(padx = 2, pady=8)
        slidelabel5 = tk.Label(sliderpack,text="-1.5",font=("Arial",9)).pack(padx = 2, pady=8)
        slidelabel6 = tk.Label(sliderpack,text="-2.0",font=("Arial",9)).pack(padx = 2, pady=8)
        slidelabel7 = tk.Label(sliderpack,text="-2.5",font=("Arial",9)).pack(padx = 2, pady=7)
        getgridbutton = tk.Button(self.tab1,text="View slice",font=("TkDefaultFont",12),command=lambda: open_popup(self.outslider),bd=3,padx=130,pady=7)
        getgridbutton.place(x=140,y=54)

    def build_entries_etc(self):
        frame12 = tk.Frame(self.tab1)
        frame12.place(x=670,y=50)
        frame22 = tk.Frame(self.tab1)
        frame22.place(x=670,y=150)
        frame32 = tk.Frame(self.tab1)
        frame32.place(x=670,y=250)
        frame14 = tk.Frame(self.tab1)
        frame14.place(x=670,y=350)
        apple = self.get_image("images/apple.png", 50, 50)
        self.apple = apple
        carbon = self.get_image("images/carbon_red.png", 50, 50)
        self.carbon = carbon
        thermom = self.get_image("images/thermometer.png", 50, 50)
        self.thermom = thermom
        graph = self.get_image("images/graph.PNG", 50, 50)
        self.graph = graph
        img_label1 = tk.Label(self.tab1, image=apple, borderwidth=0,bg="azure2").place(x=590,y=50)
        img_label2 = tk.Label(self.tab1, image=carbon, borderwidth=0,bg="azure2").place(x=590,y=155)
        img_label3 = tk.Label(self.tab1, image=thermom, borderwidth=0,bg="azure2").place(x=590,y=255)
        img_label4 = tk.Label(self.tab1, image=graph, borderwidth=0,bg="azure2").place(x=590,y=360)
        text_label1 = tk.Label(frame12, text="Log of surface gravity", bd=4, relief=tk.GROOVE, padx=10, bg="white").pack(padx=0,pady=0)
        text_label2 = tk.Label(frame22, text="Abundance ratio", bd=4, relief=tk.GROOVE, padx=23, bg="white").pack(padx=0,pady=0)
        text_label3 = tk.Label(frame32, text="Temperature", bd=4, relief=tk.GROOVE, padx=34, bg="white").pack(padx=0,pady=0)
        text_label4 = tk.Label(frame14, text="Interpolation method", bd=4, relief=tk.GROOVE, padx=10, pady=4,bg="white").pack(padx=0, pady=0)
        self.entrybox1 = tk.Entry(frame12, width=22, bd=4, relief=tk.SUNKEN)
        self.entrybox1.pack(padx=0, pady=0)
        text_label1b = tk.Label(frame12, text="(min: 0.0, max: 5.0)", padx=20, bg = "azure2").pack(padx=0, pady=0)
        self.entrybox2 = tk.Entry(frame22, width=22, bd=4, relief=tk.SUNKEN)
        self.entrybox2.pack(padx=0, pady=0)
        text_label1b = tk.Label(frame22, text="(min: -2.5, max: 0.5)", padx=18, bg="azure2").pack(padx=0,pady=0)
        self.entrybox3 = tk.Entry(frame32, width=22, bd=4, relief=tk.SUNKEN)
        self.entrybox3.pack(padx=0, pady=0)
        text_label1b = tk.Label(frame32, text="(min: 3500, max: 50000)", padx=9, bg="azure2").pack(padx=0,pady=0)
        self.selected_method = tk.StringVar()
        self.selected_method.set("                                 ")
        optionmenu = tk.OptionMenu(frame14, self.selected_method, "Nearest neighbour", "            Linear          ").pack()

    def build_wavebox(self):

        def send_input(self):
            from tkinter import messagebox
            try:
                user_grav = float(self.entrybox1.get())
                user_metal = float(self.entrybox2.get())
                user_temp = float(self.entrybox3.get())
                user_interp = self.selected_method.get()
            except:
                tk.messagebox.showinfo('Error', 'Please enter numbers')
            else:
                if user_grav < 0 or user_grav > 5:
                    tk.messagebox.showinfo('Error', 'Please enter a value from 0 to 5')
                elif user_metal < -2.5 or user_metal > 0.5:
                    tk.messagebox.showinfo('Error', 'Please enter a value from -2.5 to 0.5')
                elif user_temp < 3500 or user_temp > 50000:
                    tk.messagebox.showinfo('Error', 'Please enter a value from 3500 to 50000')
                elif user_interp == "                                 ":
                    tk.messagebox.showinfo('Error', 'Please select an interpolation method')
                else:
                    flag = False
                    temp_cliffs = [6250,7750,8500,9250,15000,20000,27000,32000,40000,50000]
                    grav_flats = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5]
                    for p in range(10):
                        if user_grav <= grav_flats[p]:
                            if user_temp >= temp_cliffs[p]:
                                tk.messagebox.showinfo('Error','This will return a spectrum where all fluxes are zero. Please select different values.')                                
                                flag = True
                        if user_grav <= 2.0 and user_temp >= 12000 and user_temp <= 13000:
                            tk.messagebox.showinfo('Error','This will return a spectrum where all fluxes are zero. Please select different values.')                                
                            flag = True
                    if flag == False:
                        interpo = Interpo(user_grav,user_temp,user_metal,user_interp)
                        interpo.run()
                        from calculations.writetotable import TableWriter
                        tablewriter = TableWriter(self.tab1,interpo.final_wave_list)
                        tablewriter.create_table_and_label()


        self.frame_wave = tk.Frame(self.tab1)
        self.frame_wave.place(x=920,y=65)
        gobutton = tk.Button(self.tab1, font = ("Arial",12), text="Get wavelengths", bd=4, relief=tk.RAISED, command = lambda:send_input(self), padx = 101, pady = 0)
        gobutton.place(x=920,y=30)
        self.wavebox_label = tk.Label(self.frame_wave, text="indexλ               λ                                 F_λ                                `", relief=tk.GROOVE, padx=3, bg="gray95")
        self.wavebox_label.pack(pady=0,anchor=tk.W)
        self.scrollbar = tk.Scrollbar(self.frame_wave)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.wavebox = tk.Listbox(self.frame_wave,bd=5,height=20,width=50,yscrollcommand=self.scrollbar.set)
        self.wavebox.pack(pady=0)
        self.scrollbar.configure(command=self.wavebox.yview)

    def build_parameters(self):

        def reset():
            plist=[-0.175,0.807,0.319,6.097,4.592,2.991,0.922,0.000,1.322,2.055,1.057,3.001]
            for n,p in enumerate(plist):
                self.entrybucket[n].delete(0,20)
                self.entrybucket[n].insert(0, str(p))
            extinction = Extinction(self.tab1,plist[0],plist[1],plist[2],plist[3],plist[4],plist[5],plist[6],plist[7],plist[8],plist[9],plist[10],plist[11])
            extinction.place(x=205,y=480)
            extinction.build_axes()
            extinction.plot_wavelengths(extinction.grapharray_xsrt)
            

        def check_and_go_params():
            try:
                c1=float(self.entrybucket[0].get())
                c2=float(self.entrybucket[1].get())
                c4=float(self.entrybucket[2].get())
                c5=float(self.entrybucket[3].get())
                x0=float(self.entrybucket[4].get())
                c3=float(self.entrybucket[5].get())
                gamma=float(self.entrybucket[6].get())
                O3=float(self.entrybucket[7].get())
                O2=float(self.entrybucket[8].get())
                O1=float(self.entrybucket[9].get())
                k_IR=float(self.entrybucket[10].get())
                R_V=float(self.entrybucket[11].get())
            except:
                from tkinter import messagebox
                tk.messagebox.showinfo('Error', 'Please reenter parameters.')
            else:
                extinction = Extinction(self.tab1,c1,c2,c4,c5,x0,c3,gamma,O3,O2,O1,k_IR,R_V)
                extinction.place(x=205,y=480)
                extinction.build_axes()
                extinction.plot_wavelengths(extinction.grapharray_xsrt)

        paradict={"c1":"-0.175","c2":"0.807","c4":"0.319","c5":"6.097","x0":"4.592","c3":"2.991","gamma":"0.922","O3":"0.000","O2":"1.322","O1":"2.055","k_IR":"1.057","R_V":"3.001"}
        framecomb = tk.Frame(self.tab1,bg="gray85")
        frameleft = tk.Frame(framecomb,bg="azure2")
        frameleft.pack(side=tk.LEFT)
        frameright = tk.Frame(framecomb,bg="azure2")
        frameright.pack(side=tk.RIGHT)
        framecomb.place(x=50,y=520)
        labelbucket =[]
        self.entrybucket =[]
        for n,key in enumerate(paradict):
            labelbucket.append(tk.Label(frameleft,font=("Arial",10),text = key,bg="azure2"))
            labelbucket[n].pack(pady=1)
            self.entrybucket.append(tk.Entry(frameright,font=("Arial",10),width=10))
            self.entrybucket[n].insert(0,paradict[key])
            self.entrybucket[n].pack(pady=2)
        toplabel = tk.Label(self.tab1,font=("Arial",12),text="Parameters",padx=20,pady=2,relief=tk.RIDGE,bd=2,bg='azure2').place(x=50,y=490)
        whiteframe = tk.Canvas(self.tab1,bg="white",height=350,width=420,bd=3,relief=tk.SUNKEN)
        whiteframe.place(x=200,y=475)
        extbutton = tk.Button(self.tab1,text="Extinction vs λ",font=("Arial",12),command=check_and_go_params,padx=60,pady=5)
        extbutton.place(x=207,y=840)
        resetbutton = tk.Button(self.tab1,text="Reset",font=("Arial",12),command=reset,padx=64,pady=5)
        resetbutton.place(x=443,y=840)
        
    def build_seperator(self):
        from tkinter import ttk
        seperator = ttk.Separator(self.tab1,orient="horizontal")
        seperator.grid(row=4,sticky=tk.W+tk.E,columnspan=15)

    def build_flambabox(self):

        def get_lambda(self):
            from tkinter import messagebox
            try:
                user_grav = float(self.entrybox1.get())
                user_metal = float(self.entrybox2.get())
                user_temp = float(self.entrybox3.get())
                user_interp = self.selected_method.get()
            except:
                tk.messagebox.showinfo('Error', 'Please enter numbers')
            else:
                if user_grav < 0 or user_grav > 5:
                    tk.messagebox.showinfo('Error', 'Please enter a value from 0 to 5')
                elif user_metal < -2.5 or user_metal > 0.5:
                    tk.messagebox.showinfo('Error', 'Please enter a value from -2.5 to 0.5')
                elif user_temp < 3500 or user_temp > 50000:
                    tk.messagebox.showinfo('Error', 'Please enter a value from 3500 to 50000')
                elif user_interp == "                                 ":
                    tk.messagebox.showinfo('Error', 'Please select an interpolation method')
                else:
                    flag = False
                    temp_cliffs = [6250,7750,8500,9250,15000,20000,27000,32000,40000,50000]
                    grav_flats = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5]
                    for p in range(10):
                        if user_grav <= grav_flats[p]:
                            if user_temp >= temp_cliffs[p]:
                                tk.messagebox.showinfo('Error','This will return a spectrum where all fluxes are zero. Please select different values.')                                
                                flag = True
                        if user_grav <= 2.0 and user_temp >= 12000 and user_temp <= 13000:
                            tk.messagebox.showinfo('Error','This will return a spectrum where all fluxes are zero. Please select different values.')                                
                            flag = True
                    if flag == False:
                        try:
                            c1=float(self.entrybucket[0].get())
                            c2=float(self.entrybucket[1].get())
                            c4=float(self.entrybucket[2].get())
                            c5=float(self.entrybucket[3].get())
                            x0=float(self.entrybucket[4].get())
                            c3=float(self.entrybucket[5].get())
                            gamma=float(self.entrybucket[6].get())
                            O3=float(self.entrybucket[7].get())
                            O2=float(self.entrybucket[8].get())
                            O1=float(self.entrybucket[9].get())
                            k_IR=float(self.entrybucket[10].get())
                            R_V=float(self.entrybucket[11].get())
                        except:
                            from tkinter import messagebox
                            tk.messagebox.showinfo('Error', 'Please reenter parameters.')
                        else:
                            extinction = Extinction(self.tab1,c1,c2,c4,c5,x0,c3,gamma,O3,O2,O1,k_IR,R_V)
                            extinction.build_axes()
                            interpo = Interpo(user_grav,user_temp,user_metal,user_interp)
                            interpo.run()
                            from calculations.writetotable import TableWriter
                            tablewriter = TableWriter(self.tab1,interpo.final_wave_list)
                            tablewriter.create_table_and_label2(extinction.grapharray_xsrt,extinction.R_V)

        self.frame_lambda = tk.Frame(self.tab1)
        self.frame_lambda.place(x=720,y=510)
        lambdabutton = tk.Button(self.tab1, font = ("Arial",12), text="Get f_lambda", bd=4, relief=tk.RAISED, command = lambda:get_lambda(self), padx = 50, pady = 0)
        lambdabutton.place(x=924,y=476)
        self.lambdabox_label = tk.Label(self.frame_lambda, text="indexλ       λ                 F_λ                   k(λ-V)                                                    f_λ                                                                     `", relief=tk.GROOVE, padx=3, bg="gray95")
        self.lambdabox_label.pack(pady=0,anchor=tk.W)
        self.scrollbar2 = tk.Scrollbar(self.frame_lambda)
        self.scrollbar2.pack(side=tk.RIGHT,fill=tk.Y)
        self.lambdabox = tk.Listbox(self.frame_lambda,bd=5,height=20,width=95,yscrollcommand=self.scrollbar2.set)
        self.lambdabox.pack(pady=0)
        self.scrollbar2.configure(command=self.wavebox.yview)

app = App()
app.mainloop()
