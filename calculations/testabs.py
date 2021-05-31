import tkinter as tk
from tkinter import ttk
root = tk.Tk()
ntbook = ttk.Notebook(root)
ntbook.place(x=50,y=50)
tab1 = ttk.Frame(ntbook,width=1380,height=900)
tab2 = ttk.Frame(ntbook,width=1380,height=900)
tab1.pack()
tab2.pack()
ntbook.add(tab1,text="f_lambda")
ntbook.add(tab2,text="filters")


abc = tk.Label(tab1,text="hey").place(x=30,y=30)

root.mainloop()
