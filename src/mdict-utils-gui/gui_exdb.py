import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fdialog
from tkinter.messagebox import showinfo, showerror

import mdict_utils.reader as reader
import reader_ext


def run():
    app = App()
    app.mainloop()


def show_meta(mdx_file):
    try:
        meta = reader.meta(mdx_file)
        for k, v in meta.items():
            print('%s: "%s"' % (k.title(), v))
    except AssertionError:
        showerror(title='Error', message="mdx version not supported!")
        return


def get_db_filename(filepath):
    # 获取文件名
    filename_with_extension = os.path.basename(filepath)
    # 分离文件名和扩展名
    filename, file_extension = os.path.splitext(filename_with_extension)
    return filename + '.db'


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("360x140")
        self.title('Export MDX to SQLite3 DB')
        self.resizable(1, 0)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        self.mdx = tk.StringVar()
        self.output = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # mdx file
        file_label = ttk.Button(self, text="MDX file:", command=self.on_select_file)
        file_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        file_entry = ttk.Entry(self, textvariable=self.mdx)
        file_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)


        # output path
        output_label = ttk.Button(self, text="Output:", command=self.on_select_output)
        output_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        output_entry = ttk.Entry(self, textvariable=self.output)
        output_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        # process button
        export_button = ttk.Button(self, text="Export", command=self.on_export)
        export_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        hint_label = ttk.Label(self, text='[提示] 注意mdx版本! 支持v2.0')
        hint_label.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

    def on_export(self):
        mdx_file = self.mdx.get()
        if not mdx_file:
            print('[Error] mdx file not selected.')
            return
        output_file = self.output.get()
        if not output_file:
            print('[Error] output file not set.')
            return

        print(f"To export : {mdx_file}")
        try:
            reader_ext.unpack_to_db_huadict(output_file, mdx_file)
        except AssertionError as e:
            showerror(title='Error', message="mdx version not supported!")
            return
        print('...exported.')
        showinfo(title='Info', message=f"Exported to : {output_file}")

    def on_select_file(self):
        filetypes = (
            ('mdx files', '*.mdx'),
            ('All files', '*.*')
        )

        initialdir = '/'
        mdx_file = self.mdx.get()
        if mdx_file:
            initialdir = os.path.dirname(mdx_file)

        filename = fdialog.askopenfilename(
            title='Open a mdx file',
            initialdir=initialdir,
            filetypes=filetypes)

        print('To select mdx file ' + filename)
        if filename:
            self.mdx.set(filename)
            output_file = os.path.join(os.path.dirname(filename), get_db_filename(filename))
            self.output.set(output_file)
            show_meta(filename)
            print('----------')

    def on_select_output(self):
        filetypes = (
            ('SQLite3 DB files', '*.db'),
            ('All files', '*.*')
        )

        initialdir = '/'
        initialfile = 'output.db'
        mdx_file = self.mdx.get()
        if mdx_file:
            initialdir = os.path.dirname(mdx_file)
            initialfile = get_db_filename(mdx_file)

        filename = fdialog.asksaveasfilename(
            title='Save as DB file',
            initialdir=initialdir,
            initialfile=initialfile,
            filetypes=filetypes)

        print('To select output : ' + filename)
        if filename:
            self.output.set(filename)


if __name__ == "__main__":
    print('【注意】运行中请勿关闭命令行窗口！')
    run()
