import tkinter as tk

class TableWriter(tk.Frame):
    def __init__(self,tab1,final_wave_list):
        tk.Frame.__init__(self,master=tab1)
        self.final_wave_list = final_wave_list

    def create_table_and_label(self):
        import numpy as np
        from astropy.io import fits
        self.wavebox_label = tk.Label(self, text="indexλ               λ                                 F_λ                                `", relief=tk.GROOVE,padx=3, bg="gray95")
        self.wavebox_label.pack(pady=0,anchor=tk.W)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.wavebox = tk.Listbox(self,bd=5,height=20,width=50,yscrollcommand=self.scrollbar.set)
        self.wavebox.pack(pady=0)
        self.scrollbar.configure(command=self.wavebox.yview)

        with fits.open("fits_library/ckm05/ckm05_3500.fits") as hdul:
            wavelabels = hdul[1].data["WAVELENGTH"]
            for col in range(1221):
                self.wavebox.insert(tk.END, "{}                {}                    {}".format(col,str(wavelabels[col]),str(format(self.final_wave_list[col],'.4e'))))
        
        self.place(x=920,y=65)

    def create_table_and_label2(self,ext_array,R_V):
        import numpy as np
        from astropy.io import fits
        self.lambdabox_label = tk.Label(self, text="indexλ       λ                 F_λ                   k(λ-V)                                                    f_λ                                                                     `", relief=tk.GROOVE,padx=3, bg="gray95")
        self.lambdabox_label.pack(pady=0,anchor=tk.W)
        self.scrollbar2 = tk.Scrollbar(self)
        self.scrollbar2.pack(side=tk.RIGHT,fill=tk.Y)
        self.lambdabox = tk.Listbox(self,bd=5,height=20,width=95,yscrollcommand=self.scrollbar2.set)
        self.lambdabox.pack(pady=0)
        self.scrollbar2.configure(command=self.lambdabox.yview)
        ext_array = np.flipud(ext_array)
        with fits.open("fits_library/ckm05/ckm05_3500.fits") as hdul:
            wavelabels = hdul[1].data["WAVELENGTH"]
        f_lambda_array = []
        for ind in range(1221):
            f_lambda_array.append("({})*θ_r^2*10^(-0.4E(B-V)[{}+{}])".format(format(self.final_wave_list[ind],'.4e'),format(ext_array[ind,1],'.4e'),R_V))

        for col in range(1221):
            self.lambdabox.insert(tk.END, "{}       {}       {}       {}       {}".format(col,str(wavelabels[col]),str(format(self.final_wave_list[col],'.4e')),str(format(ext_array[col,1],'.4e')),f_lambda_array[col]))
        
        self.place(x=720,y=510)
