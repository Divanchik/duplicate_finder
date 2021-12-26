from imfunc import scanner, sko, average_hash, phash, hist, tqdm
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
APP_WIDTH = 1000
APP_HEIGHT = 700


# главное окно
root = Tk()
root.title('Duplicate finder')
root.geometry('{}x{}+{}+{}'.format(APP_WIDTH, APP_HEIGHT, (root.winfo_screenwidth() - APP_WIDTH)//2, (root.winfo_screenheight() - APP_HEIGHT)//2))


# переменные
label_target = "Путь к изображению"
label_folder = "Путь к папке"
path_target = StringVar(value="")
path_folder = StringVar(value="")

format = {}
format['.PNG'] = BooleanVar(value=True)
format['.JPEG'] = BooleanVar(value=True)

resimg = 0

mode = [sko, average_hash, phash, hist]
mode_index = IntVar(value=0)
distance = IntVar(value=0)
files = []
is_recursive = BooleanVar(value=True)


# фреймы
frm_actions = Frame(root, relief=FLAT)
frm_options = LabelFrame(root, relief=GROOVE, text="Настройки")
frm_files = Frame(root, relief=FLAT)
frm_demo = Frame(root, relief=RAISED)


# действия
btn_scan = Button(frm_actions, text="Сканировать")
btn_show = Button(frm_actions, text="Показать")


# настройки
lbl_folder = Label(frm_options, text=label_folder, justify=LEFT, anchor=W)
btn_folder = Button(frm_options, text="Открыть")
lbl_target = Label(frm_options, text=label_target, justify=LEFT, anchor=W)
btn_target = Button(frm_options, text="Открыть")

lbl_format = Label(frm_options, text="Расширение:", justify=LEFT, anchor=W)
cbt_jpeg = Checkbutton(frm_options, text="*.JPEG", variable=format[".JPEG"], onvalue=True, offvalue=False)
cbt_png = Checkbutton(frm_options, text="*.PNG", variable=format[".PNG"], onvalue=True, offvalue=False)

lbl_mode = Label(frm_options, text="Метод сравнения:", justify=LEFT, anchor=W)
rbt_sko = Radiobutton(frm_options, text="СКО", variable=mode_index, value=0)
rbt_ahash = Radiobutton(frm_options, text="Средний хэш", variable=mode_index, value=1)
rbt_phash = Radiobutton(frm_options, text="Перцептивный хэш", variable=mode_index, value=2)
rbt_hist = Radiobutton(frm_options, text="Гистограмма", variable=mode_index, value=3)

lbl_dist = Label(frm_options, text="Максимальное расстояние:", justify=LEFT, anchor=W)
scl_dist = Scale(frm_options, orient=HORIZONTAL, from_=0, to=20, variable=distance, showvalue=True)
cbt_rec = Checkbutton(frm_options, text="Рекурсивное сканирование", justify=LEFT, anchor=W, variable=is_recursive, onvalue=True, offvalue=False)


# файлы
list_files = Listbox(frm_files, bd=0, bg='white', fg='black', justify='left', width=50, selectmode=BROWSE)
scr_files = Scrollbar(frm_files, command=list_files.yview)
list_files.config(yscrollcommand=scr_files.set)

# демо
lbl_img = Label(frm_demo)

def get_folder():
    path_folder.set(askdirectory(title="Выберите папку для сканирования"))
    lbl_folder.config(text=label_folder + ":\n" + path_folder.get())

def get_target():
    ft = (
        ('PNG', '*.png'),
        ('JPG', '*.jpg'),
        ('JPEG', '*.jpeg'),
        ('All files', '*.*')
    )
    path_target.set(askopenfilename(title="Выберите изображение образец", filetypes=ft))
    lbl_target.config(text=label_target + ":\n" + path_target.get())

def find_all():
    global files
    formats = []
    if format[".PNG"]:
        formats.append('.png')
        formats.append('.PNG')
    if format[".JPEG"]:
        formats.append('.jpeg')
        formats.append('.JPEG')
        formats.append('.jpg')
        formats.append('.JPG')
    a = scanner(path_target.get(), path_folder.get(), formats)
    files = a.find(mode[mode_index.get()], distance.get(), is_recursive.get())
    list_files.delete(0, list_files.size()-1)
    for i in tqdm(range(len(files)-1), desc="Сортировка", ncols=100):
        for j in range(len(files)-2):
            if files[j]['rate'] > files[j+1]['rate']:
                files[j], files[j+1] = files[j+1], files[j]
    for i in files:
        list_files.insert(END, i['name']+" "*(50-len(i['rate'])-len(i['name']))+i['rate'])
    showinfo(title="Информация", message="{} изображений найдено!".format(len(files)))

def show_selected():
    global resimg
    maxsize = 500
    try:
        ind = list_files.curselection()[0]
        img = Image.open(files[ind]['path'])
        resize_ratio = maxsize/max(img.size)
        newsize = (int(img.width*resize_ratio), int(img.height*resize_ratio))
        print(img.size, "->", newsize)
        resimg = ImageTk.PhotoImage(img.resize(newsize))
        lbl_img.config(image=resimg)
    except IndexError:
        print("Ничего не выбрано!")

btn_folder.config(command=get_folder)
btn_target.config(command=get_target)
btn_scan.config(command=find_all)
btn_show.config(command=show_selected)


# упаковка
frm_actions.pack(side=BOTTOM, fill=X)
frm_options.pack(side=LEFT, fill=Y, padx=5, pady=5)
frm_files.pack(side=LEFT, fill=Y, padx=5, pady=5)
frm_demo.pack(side=LEFT, fill=Y, padx=5, pady=5, expand=1)

lbl_img.pack(expand=1)

lbl_folder.pack(side=TOP, fill=X, padx=5, pady=5)
btn_folder.pack(side=TOP, padx=5, pady=5, anchor=E)
lbl_target.pack(side=TOP, fill=X, padx=5, pady=5)
btn_target.pack(side=TOP, padx=5, pady=5, anchor=E)

lbl_format.pack(side=TOP, fill=X, padx=5, pady=5)
cbt_jpeg.pack(side=TOP, padx=5, pady=5, anchor=W)
cbt_png.pack(side=TOP, padx=5, pady=5, anchor=W)

lbl_mode.pack(side=TOP, fill=X, padx=5, pady=5)
rbt_sko.pack(side=TOP, padx=5, pady=5, anchor=W)
rbt_ahash.pack(side=TOP, padx=5, pady=5, anchor=W)
rbt_phash.pack(side=TOP, padx=5, pady=5, anchor=W)
rbt_hist.pack(side=TOP, padx=5, pady=5, anchor=W)

lbl_dist.pack(side=TOP, fill=X, padx=5, pady=5)
scl_dist.pack(side=TOP, fill=X, padx=5, pady=5)
cbt_rec.pack(side=TOP, padx=5, pady=5, anchor=W)

scr_files.pack(side=RIGHT, fill=Y)
list_files.pack(side=LEFT, fill=BOTH)

btn_scan.pack(side=LEFT, padx=5, pady=5)
btn_show.pack(side=RIGHT, padx=5, pady=5)


# run the application
root.mainloop()
