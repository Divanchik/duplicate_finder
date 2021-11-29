from tkinter import *

from numpy import exp

APP_WIDTH = 1000
APP_HEIGHT = 550

root = Tk()
root.title('Duplicate finder')
root.resizable(False, False)
root.geometry('{}x{}+{}+{}'.format(APP_WIDTH, APP_HEIGHT, (root.winfo_screenwidth() -
              APP_WIDTH)//2, (root.winfo_screenheight() - APP_HEIGHT)//2))

actions = Label(bg='yellow', text="actions")
options = Label(bg='orange', text="options")
files = Label(bg='lightgreen', text="files")

actions.pack(side=TOP, fill=X)
files.pack(side=RIGHT, fill=BOTH, padx=5, pady=5, expand=1)
options.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

root.mainloop()