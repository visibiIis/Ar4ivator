from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox as mb
import os
import zipfile
import time
import threading

#
# .py --> .pyw to hide a console
#

class Main:
    def __init__(self):
        self.root = root
        root.title("Ar4ivator")
        root.geometry("350x260")
        root.resizable(False, False)
        root.configure(bg="#F7C9C1")

        self.base_dir = str()
        self.work_dir = str()

        # From Wrapper
        from_wrapper = Frame(root, bg="#F7C9C1")
        from_wrapper.pack(anchor=NW, padx=10, pady=5)

        Label(from_wrapper, text="Select 'osu!' directory:", font=("Helvetica", 11), bg="#F7C9C1").pack(anchor=NW)
        # From declaration
        from_composite = Frame(from_wrapper, bg="#F7C9C1")
        from_but = Button(from_composite, text="...", width=3, height=1, bg="#EDF7C1", command=self.setFrom)
        self.from_ent = Entry(from_composite, width=40, font=("Helvetica", 10))
        # From pack
        from_composite.pack(anchor=NW, pady=(5, 10))
        from_but.pack(side=LEFT, padx=(0, 7))
        self.from_ent.pack(side=LEFT, padx=(7, 0))

        # Save Wrapper
        save_wrapper = Frame(root, bg="#F7C9C1")
        save_wrapper.pack(anchor=NW, padx=10, pady=20)

        Label(save_wrapper, text="Select destination:", font=("Helvetica", 11), bg="#F7C9C1").pack(anchor=NW)
        # Save declaration
        save_composite = Frame(save_wrapper, bg='#F7C9C1')
        save_but = Button(save_composite, text="...", width=3, height=1, bg="#EDF7C1", command=self.setSave)
        self.save_ent = Entry(save_composite, width=40, font=("Helvetica", 10))
        # Save pack
        save_composite.pack(anchor=NW, pady=(5, 10))
        save_but.pack(side=LEFT, padx=(0, 7))
        self.save_ent.pack(side=LEFT, padx=(7, 0))

        self.ar4ive_but = Button(root, text="Ar4ive", font=("Helvetica", 16), height=2, width=15, bg="#C1CFF7",
                                 )
        self.ar4ive_but.pack()
        self.ar4ive_but.bind("<Button-1>", lambda x: threading.Thread(target=self.preAr4ive).start())

    @staticmethod  # try to open dialog window
    def opening():
        try:
            os.chdir(askdirectory())
        except OSError:
            return False

        return True

    # insert "from" path
    def setFrom(self):
        if not self.opening():
            return
        work_dir = os.getcwd()  # set work directory

        self.from_ent.delete(0, END)  # clear path field
        self.from_ent.insert(0, work_dir)  # insert path in path field

    # insert "save" path
    def setSave(self):
        if not self.opening():
            return
        base_dir = os.getcwd()  # set base directory

        self.save_ent.delete(0, END)  # clear path field
        self.save_ent.insert(0, base_dir)  # insert path in path field

    def preAr4ive(self):
        work_dir = self.from_ent.get()  # get paths from path fields
        base_dir = self.save_ent.get()  #

        # existence of entered dirs
        if not os.path.isdir(work_dir) or not os.path.isdir(base_dir):
            mb.showerror("Error", "Choose an existing directory!")
            return
        # existence of osu! in path; osu!.exe in dir; Songs in dir
        elif "\\osu!" not in work_dir or \
                not os.path.isfile(os.path.join(work_dir, "osu!.exe")) or \
                not os.path.isdir(os.path.join(work_dir, "Songs")):
            mb.showerror("Error", "Choose an 'osu!' directory!")
            return

        answer = mb.askyesno(title="Message", message="Start ar4iving?")
        if answer is False:
            return

        self.ar4ive_but.configure(text="in progress...")
        self.work_dir = work_dir
        self.base_dir = base_dir
        self.ar4ive()

    def ar4ive(self):
        work_dir = self.work_dir
        base_dir = self.base_dir

        work_dir = os.path.join(work_dir, "Songs")  # entering in Songs
        os.chdir(work_dir)  # change current work directory

        mega_zip = zipfile.ZipFile(base_dir + "/Songs.zip", "w", allowZip64=True)  # create a .zip file

        start_time = time.time()
        for path, dirs, files in os.walk(work_dir):  # get tuple (path, dirs[], files[])
            for file in files:
                # append .osz file to .zip file
                mega_zip.write(os.path.relpath(os.path.join(path, file), work_dir), compress_type=zipfile.ZIP_DEFLATED)

        print("Code was executed for {:.3} sec.".format(time.time() - start_time))
        self.ar4ive_but.configure(text="Ar4ive")
        mb.showinfo("Message", "Ar4iving completed!")

root = Tk()
home = Main()
root.mainloop()
