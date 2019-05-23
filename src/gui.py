# -*- coding: utf-8 -*-

import os
from concurrent import futures
from tkinter import (
    BOTH, BOTTOM, END, LEFT, TOP, Button, Entry, Frame, Label, Scrollbar, Text,
    Tk, X, Y, filedialog, messagebox, ttk)

import config
from core import Core
from web import Web

class Gui(Frame):

    def log(self, value):
        self.text.configure(state="normal")
        self.text.insert(END, value + '\n')
        self.text.see(END)
        self.text.configure(state="disabled")

    def download(self):
        self.btn_download.configure(state="disabled")
        self.btn_download_txt.configure(state="disabled")
        username_text = self.entry_filename.get()
        if len(username_text) is 0 or len(username_text.split(','))!=3:
            messagebox.showinfo(
                title='Warning', message='Please input startpage and index with limit split by ,')
        else:
            usernames = username_text.split(',')
            self.core.root_path = self.root_path
            self.core.download_by_usernames(usernames, self.combobox_type.current())
        self.btn_download.configure(state="normal")
        self.btn_download_txt.configure(state="normal")

    def download_txt(self):
        self.btn_download.configure(state="disabled")
        self.btn_download_txt.configure(state="disabled")
        filename = os.path.normpath(filedialog.askopenfilename(
            filetypes=(('text files', '*.txt'), ("all files", "*.*"))))
        if filename is not '.':
            print("done:"+filename)
  
        self.btn_download.configure(state="normal")
        self.btn_download_txt.configure(state="normal")

    def browse_directory(self):
        dir = os.path.normpath(filedialog.askdirectory())
        if dir is not '':
            self.root_path = dir
            config.write_config('config.ini', 'Paths',
                                'root_path', self.root_path)
            self.entry_path.delete(0, END)
            self.entry_path.insert(0, self.root_path)
            self.core.root_path = self.root_path
            self.web.defaultDedirectory=self.root_path
        

    def createWidgets(self):
        frame_tool = Frame(self.window)
        frame_path = Frame(self.window)
        frame_log = Frame(self.window)
        self.lbl_username = Label(
            frame_tool, text='Start Page,EndPage,Limit,(split by ,):')
        self.entry_filename = Entry(frame_tool)
        self.btn_download = Button(
            frame_tool, text='Download', command=lambda: self.executor_ui.submit(self.download))
        self.btn_download_txt = Button(
            frame_tool, text='Download txt', command=lambda: self.executor_ui.submit(self.download_txt))
        self.lbl_type = Label(frame_path, text='Type:')
        self.combobox_type = ttk.Combobox(frame_path, state='readonly')
        self.combobox_type["values"] = ('all', 'image', 'torrent')
        self.combobox_type.current(0)
        self.lbl_path = Label(frame_path, text='Path:')
        self.entry_path = Entry(frame_path)
        self.entry_path.insert(END, self.root_path)
        self.btn_path_dialog = Button(
            frame_path, text="Browse", command=lambda: self.browse_directory())
        self.scrollbar = Scrollbar(frame_log)
        self.text = Text(frame_log)
        self.text.configure(state="disabled")
        self.lbl_status = Label(
            self.window, text='-10086')
        
        frame_tool.pack(side=TOP, fill=X)
        self.lbl_username.pack(side=LEFT)
        self.entry_filename.pack(side=LEFT, fill=X, expand=True)
        self.btn_download.pack(side=LEFT)
        self.btn_download_txt.pack(side=LEFT)
        frame_path.pack(side=TOP, fill=X)
        self.lbl_type.pack(side=LEFT)
        self.combobox_type.pack(side=LEFT)
        self.lbl_path.pack(side=LEFT)
        self.entry_path.pack(side=LEFT, fill=X, expand=True)
        self.btn_path_dialog.pack(side=LEFT)
        self.text.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=LEFT, fill=Y)
        frame_log.pack(side=TOP, fill=BOTH, expand=True)
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.text.focus()
        self.lbl_status.pack(side=LEFT, fill=X, expand=True)

    def __init__(self, version):
        self.core = Core(self.log)
        self.web = Web(self.log)
        master = Tk()
        Frame.__init__(self, master)
        master.title('AV Downloader ' + version)
        root_path_config = config.read_config(
            'config.ini', 'Paths', 'root_path')
        self.root_path = os.path.join(
            os.path.expanduser("~"), "downloads") if root_path_config is '' else root_path_config
        self.executor_ui = futures.ThreadPoolExecutor(1)
        self.window = master
        self.pack()
        self.createWidgets()
