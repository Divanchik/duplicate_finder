# from numpy.core.fromnumeric import var
from imfunc import assemble, scanner, sko, average_hash, phash
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
# from tkinter.ttk import *
APP_WIDTH = 1000
APP_HEIGHT = 550


# главное окно
root = Tk()
root.title('Duplicate finder')
root.resizable(False, False)
root.geometry('{}x{}+{}+{}'.format(APP_WIDTH, APP_HEIGHT, (root.winfo_screenwidth() -
              APP_WIDTH)//2, (root.winfo_screenheight() - APP_HEIGHT)//2))


# переменные
target_base = "Путь к изображению"
folder_base = "Путь к папке"
target_path = StringVar(value="")
folder_path = StringVar(value="")

format = {}
format['.PNG'] = BooleanVar(value=True)
format['.JPEG'] = BooleanVar(value=True)

modelist = [sko, average_hash, phash]
mode = IntVar(value=0)
modedist = IntVar(value=0)
files = []

scan_rec = BooleanVar(value=False)

menu_main = Menu(root)                 # главное меню
menu_file = Menu(menu_main, tearoff=0) # меню "Файл"

menu_file.add_command(label="Открыть...")
menu_file.add_command(label="Сохранить...")
menu_file.add_command(label="Выход")

menu_main.add_cascade(label="Файл", menu=menu_file)
menu_main.add_command(label="О программе")


# фреймы
frm_actions = Frame(root, relief=RAISED)
frm_options = LabelFrame(root, relief=GROOVE, text="Настройки")
frm_files = Frame(root, relief=FLAT)


# действия
btn_scan = Button(frm_actions, text="Сканировать")
btn_delete = Button(frm_actions, text="Удалить")


# настройки
lbl_folder = Label(frm_options, text=folder_base, justify=LEFT, anchor=W)
btn_bfolder = Button(frm_options, text="Открыть")
lbl_target = Label(frm_options, text=target_base, justify=LEFT, anchor=W)
btn_btarget = Button(frm_options, text="Открыть")
lbl_format = Label(frm_options, text="Расширение:", justify=LEFT, anchor=W)
cbt_jpeg = Checkbutton(frm_options, text="*.JPEG",
                       variable=format[".JPEG"], onvalue=True, offvalue=False)
cbt_png = Checkbutton(frm_options, text="*.PNG",
                      variable=format[".PNG"], onvalue=True, offvalue=False)

lbl_method = Label(frm_options, text="Метод сравнения:", justify=LEFT, anchor=W)
rbt_sko = Radiobutton(frm_options, text="СКО", variable=mode, value=0)
rbt_ahash = Radiobutton(frm_options, text="Average hash", variable=mode, value=1)
rbt_phash = Radiobutton(frm_options, text="Perceptive hash", variable=mode, value=2)
scl_dist = Scale(frm_options, orient=HORIZONTAL, from_=0, to=20, variable=modedist, showvalue=True)
cbt_rec = Checkbutton(frm_options, text="Сканировать рекурсивно", justify=LEFT, anchor=W, variable=scan_rec, onvalue=True, offvalue=False)


# файлы
list_files = Listbox(frm_files, bd=0, bg='white',
                     fg='black', justify='left', width=100)
scr_files = Scrollbar(frm_files, command=list_files.yview)
list_files.config(yscrollcommand=scr_files.set)

def get_folder():
    folder_path.set(askdirectory(title="Выберите папку для сканирования"))
    lbl_folder.config(text=folder_base + ":\n" + folder_path.get())

def get_target():
    ft = (
        ('PNG', '*.png'),
        ('JPG', '*.jpg'),
        ('JPEG', '*.jpeg'),
        ('All files', '*.*')
    )
    target_path.set(askopenfilename(title="Выберите изображение образец", filetypes=ft))
    lbl_target.config(text=target_base + ":\n" + target_path.get())
def find_all():
    global files
    formats = []
    if format[".PNG"]:
        formats.append('.png')
    if format[".JPEG"]:
        formats.append('.jpeg')
        formats.append('.jpg')
        formats.append('.JPG')
    a = scanner(target_path.get(), folder_path.get(), formats)
    files = a.find(modelist[mode.get()], modedist.get(), scan_rec.get())
    list_files.delete(0, list_files.size()-1)
    for i in files:
        list_files.insert(END, assemble(i[0], i[1], 100))
    if len(files)==0:
        showinfo(title="Информация", message="Похожих изображений не найдено!")
btn_bfolder.config(command=get_folder)
btn_btarget.config(command=get_target)
btn_scan.config(command=find_all)


# упаковка
root.config(menu=menu_main)

frm_actions.pack(side=TOP, fill=X)
frm_options.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
frm_files.pack(side=RIGHT,fill=Y, padx=5, pady=5, expand=1)

lbl_folder.pack(side=TOP, fill=X, padx=5, pady=5)
btn_bfolder.pack(side=TOP, padx=5, pady=5, anchor=E)
lbl_target.pack(side=TOP, fill=X, padx=5, pady=5)
btn_btarget.pack(side=TOP, padx=5, pady=5, anchor=E)

lbl_format.pack(side=TOP, fill=X, padx=5, pady=5)
cbt_jpeg.pack(side=TOP, padx=5, pady=5, anchor=W)
cbt_png.pack(side=TOP, padx=5, pady=5, anchor=W)

lbl_method.pack(side=TOP, fill=X, padx=5, pady=5)
rbt_sko.pack(side=TOP, padx=5, pady=5, anchor=W)
rbt_ahash.pack(side=TOP, padx=5, pady=5, anchor=W)
rbt_phash.pack(side=TOP, padx=5, pady=5, anchor=W)

scl_dist.pack(side=TOP, fill=X, padx=5, pady=5)
cbt_rec.pack(side=TOP, padx=5, pady=5, anchor=W)

scr_files.pack(side=RIGHT, fill=Y)
list_files.pack(side=LEFT, fill=BOTH)

btn_scan.pack(side=LEFT, padx=5, pady=5)
btn_delete.pack(side=LEFT, padx=5, pady=5)


# run the application
root.mainloop()
