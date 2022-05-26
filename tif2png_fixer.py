import os
from datetime import datetime, timedelta
import re
from tkinter import * 
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
import threading
folder_names= os.listdir(r"C:\files")
sql_re = "\`|\´|\"|\'"



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#master == root
class Gui():

    def __init__(self, master, minsize, maxsize):
        self.master = master;
        self.master.title("Jeeves TIF2PNG Fixer")
        self.master.iconbitmap(resource_path("ICON.ico"))
        self.master.minsize(minsize[0], minsize[1])
        self.master.maxsize(maxsize[0], maxsize[1])
        self.master.style = Style()
        self.text = Entry(master, width=60)
        self.title = Label(master, text="Jeeves TIF2PNG Fixer", font=("Courier", 20))
        self.title.place(x=300, y=50, anchor="center")
        self.master.style.configure('TButton', font = 
               ('calibri', 20, 'bold'), 
                foreground = 'black')
        vcmd = (master.register(self.validate),'%S')        
        self.text.place(x=200, y=200, anchor="center")
        self.button1 = Button(master, text = '🖿',style = 'TButton', command = lambda: self.get_foldername())
        self.folder_label = Label(master, text="Location of tif2png text files")
        self.folder_label.place(x=200, y=160, anchor="center")
        self.button1.place(x=540, y=200, width=45, height=40, anchor="center")
        self.button2 = Button(master, text = 'Find Files with Errors',style = 'TButton', command = lambda: self.remove_sql_strings())
        self.button2.place(x=300, y=300, anchor="center")
        self.text_daysback = Entry(master, width=10, validate='all', validatecommand=vcmd)
        self.text_daysback.place(x=450, y=200, anchor="center")
        self.daysback_label = Label(master, text="days back to check")
        self.daysback_label.place(x=450, y=160, anchor="center")
        self.actions = Actions()
        self.days_back = str()


        self.text_daysback.insert(0, "7")


    def get_foldername(self):
        self.text.insert(0, "")
        folder = self.actions.open_folder()
        print(self.actions.folder)
        self.text.insert(0, folder)

    def validate(self, S):
        if S in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return True
        else:
            return False


    def remove_sql_strings(self):
        self.actions.days_back = self.text_daysback.get()
        info = self.actions.check_text_files()
        print(info)
        if len(info) == 0:
            messagebox.showinfo(title="No errors found", message="No txtfiles needed to be changed")
        else:
            question = messagebox.askquestion(title="Files with errors found", message=str(len(info)) +" files were changed. Moved the old pre-fixedf files to a new folder. Open this folder?")
            if question == "yes":
                print("eeee")
                os.system(f'start {os.path.realpath(self.actions.new_folder_old)}')
            

class Actions():
    def __init__(self, folder="C:\\", days_back=7):
        self.folder = folder
        self.days_back = days_back
        self.new_folder_old = folder
    
    def open_folder(self):
        folder = filedialog.askdirectory()
        self.folder = folder.replace('/', "\\")
        return self.folder


    def check_text_files(self):
        text_folder = os.listdir(self.folder)
        folder_exists = os.path.isdir(self.folder + "\\" + "old_fixed_files")
        if folder_exists is False:
            self.new_folder_old = os.mkdir(self.folder + "\\" + "old_fixed_files")
        else:
            self.new_folder_old = self.folder + "\\" + "old_fixed_files"
        files_changes = list()
        for txtfile in text_folder:
            if txtfile.endswith(".txt"):
                txt_last_modified_epoch = os.path.getmtime(self.folder + "\\" + txtfile)
                txt_last_modified_normal = datetime.fromtimestamp(txt_last_modified_epoch).strftime('%Y-%m-%d')
                days_to_check = datetime.now() - timedelta(days=int(self.days_back))
                if days_to_check.strftime('%Y-%m-%d') <= txt_last_modified_normal:
                    tif2png_read = open(self.folder + "\\" + txtfile, "r")
                    file_contents = tif2png_read.read()
                    tif2png_re = re.sub("\`|\´|\"|\'|\?", '', file_contents)
                    if file_contents != tif2png_re:
                        files_changes.append(self.folder + "\\" + txtfile)
                        tif2png_re_write = open(self.folder + "\\" + txtfile, "w")
                        tif2png_old_write = open(self.new_folder_old + "\\" + "OLD-" + txtfile, "w")
                        tif2png_old_write.write(file_contents)
                        tif2png_re_write.write(tif2png_re)
                        
        return files_changes    


def open_folder():
    file_path = filedialog.askdirectory()
    print(file_path)


def main():
    folder_names= os.listdir(r"C:\files")
    window = Tk()
    gui_class = Gui(window, [600,400], [600, 400])
    window.mainloop()
    #GUI(folder_names, days_back)
main()
    

