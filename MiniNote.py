# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:02:07 2024

@author: Alamentine
"""
from typing import Optional
from tkinter import filedialog
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import os
import sys

class Note(tk.Tk):
   
    def __init__(self):
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        
        super().__init__()
        self.overrideredirect(True)
        self.geometry("250x200+1665+835")
        self.configure(bg="#1a1a1e")
        self.wm_attributes('-alpha', 0.9)
        self.text = tk.Text()
        self.header = tk.Label()
        #print(resource_path('test'))
        photo = tk.PhotoImage(file = resource_path('images/close.png'))
        cicon = photo.subsample(28,28)
        photo = tk.PhotoImage(file = resource_path('images/new.png'))
        nicon = photo.subsample(28,28)
        photo = tk.PhotoImage(file = resource_path('images/saveSwirl.png'))
        sicon = photo.subsample(25,25)
        photo = tk.PhotoImage(file = resource_path('images/open.png'))
        oicon = photo.subsample(28,28)
        closeButt = tk.Button(self.header, image= cicon, bg="#1a1a1e", fg="white", borderwidth=0, command = self.close)
        closeButt.image = cicon
        newButt = tk.Button(self.header, image= nicon, bg="#1a1a1e", fg="white", command = self.new)
        newButt.image = nicon
        saveButt = tk.Button(self.header, image= sicon, bg="#1a1a1e", fg="white", borderwidth=0, command = self.save)
        saveButt.image = sicon
        loadButt = tk.Button(self.header, image= oicon, bg="#1a1a1e", fg="white", command = self.load)
        loadButt.image= oicon

        self.text.config(bg="#1a1a1e", fg="white", insertbackground= "white", borderwidth=0, font=("Helvetica", 14))
        self.header.config(bg="#1a1a1e", fg="white")
        
        #newButt.pack(side="left")
        #loadButt.pack(side="left")
        saveButt.pack(side="left",  padx=6)
        closeButt.pack(side="right", padx=6)
        self.header.pack(expand = True, fill = tk.X, pady =6)
        self.text.pack(expand=True, fill=tk.BOTH, padx =10)
        
        
        self.header.bind("<ButtonPress-1>", self.start_move)
        self.header.bind("<ButtonRelease-1>", self.stop_move)
        self.header.bind("<B1-Motion>", self.do_move)
        
        self.grip = ttk.Sizegrip(self.text)
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        self.grip.bind("<B1-Motion>", self.OnMotion)
        
        # The `current_file` attribute contains the path of the
        # file that is being edited or `None` if the file has
        # not been saved yet.
        self.current_file: Optional[Path] = None
        # File types that will show in the open and save
        # file dialogs.
        self.filetypes: tuple[tuple[str, str], ...] = (
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        )
        self.autoLoad()
        

        
    def OnMotion(self, event):
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        self.geometry("%sx%s" % ((x1-x0),(y1-y0)))
        return
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        
    def set_current_file(self, current_file: Path) -> None:
        self.current_file = current_file
        self.title(self.current_file.name + " - Notepad")

    
    def close(self):
        self.destroy()
        
    def new(self):
        self.text.delete("1.0", tk.END)
        self.current_file = None
    

    def save(self) -> None:
        #if self.current_file is None:
         #   self.save_as()
         #   return
        self.save_current_file()

    def save_as(self) -> None:
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=self.filetypes
        )
        # Do nothing if the user closed or cancelled the dialog.
        if not filename:
            return
        self.set_current_file(Path(filename))
        self.save_current_file()
    
    def save_current_file(self) -> None:
        if self.current_file is None:
            return
        self.current_file.write_text(self.text.get("1.0", tk.END), "utf8")

    
    def load(self):
        filename = filedialog.askopenfilename(filetypes=self.filetypes)
        if not filename:
            return
        # Remove previous text and load the new one.
        self.text.delete("1.0", tk.END)
        file = Path(filename)
        self.text.insert("1.0", file.read_text("utf8"))
        # Reset text state when a new file is opened.
        self.text.edit_modified(False)
        self.set_current_file(file)
        
    def autoLoad(self):
        # Remove previous text and load the new one.  Have check if file exists, if not create file
        self.text.delete("1.0", tk.END)
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        filename = os.path.join(base_path, "Note.txt")
        file = Path(filename)
        self.text.insert("1.0", file.read_text("utf8"))
        # Reset text state when a new file is opened.
        self.text.edit_modified(False)
        self.set_current_file(file)
        



note = Note()
note.mainloop()
