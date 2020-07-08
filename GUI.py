from pathlib import Path
from tkinter import ttk
import tkinter.filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
import pandas as pd
import numpy as np
import os
import sys
from QBlade_processing import QBlade


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # 全体設定
        self.master.title(u"QBlade")
        self.master.columnconfigure(0, weight=1, uniform='group1')
        self.master.rowconfigure(0, weight=1, uniform='group1')

        self.frame_Graph = tkinter.Frame(self.master, width=300, height=300, bd=2, relief="ridge")
        self.frame_Graph.grid(row=0, column=0, rowspan=10, columnspan=10)

        self.data_list = tkinter.Frame(self.master)
        self.data_list.grid(row=10, column=0, columnspan=10, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))

        self.files_list = tkinter.Frame(self.master, height=300, bd=2, relief="ridge")
        self.files_list.grid(row=0, column=11, rowspan=10, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))

        self.frame_csv_list = tkinter.Frame(self.files_list, relief="ridge")
        self.frame_csv_list.grid(row=0, column=0,
                                 sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))

        self.frame_plot_data = tkinter.Frame(self.files_list, relief="ridge")
        self.frame_plot_data.grid(row=5, column=0,
                                  sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))

        self.config = tkinter.Frame(self.master, width=300, height=300, bd=2)
        self.config.grid(row=11, column=1)

        self.frame_lim = tkinter.Frame(self.config, width=300, height=300, bd=2, relief="ridge")
        self.frame_lim.grid(row=1, column=2)

        self.frame_data = tkinter.Frame(self.master, bd=2, relief="ridge")
        self.frame_data.grid(row=11, column=11)
        # Variables for Graph
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(111, projection='polar')
        self.fig.gca().set_aspect('equal', adjustable='box')  # グラフ領域の調整
        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111)
        # Variables for Menu
        self.grid_interval_x = tkinter.DoubleVar(value=30)
        self.grid_interval_y = tkinter.DoubleVar(value=1000)
        self.enableGrid = tkinter.BooleanVar()
        # Variables for Tab and Canvas
        self.nb = ttk.Notebook(self.frame_Graph)
        self.descartes_tab = tkinter.Frame(self.nb)
        self.polar_tab = tkinter.Frame(self.nb)
        self.Canvas2 = FigureCanvasTkAgg(self.fig2, master=self.descartes_tab)
        self.Canvas = FigureCanvasTkAgg(self.fig, master=self.polar_tab)
        # Variables for text-box
        self.dir_path = tkinter.StringVar()
        self.file_name = tkinter.StringVar()
        self.Entry_select_directory = ttk.Entry(self.frame_csv_list, textvariable=self.dir_path, state="readonly")
        self.Entry_csv_path = ttk.Entry(self.frame_csv_list, textvariable=self.file_name, state="readonly")
        self.plot_data_name = tkinter.StringVar()
        self.Entry_plot_data = ttk.Entry(self.frame_plot_data, textvariable=self.plot_data_name, state="readonly")
        # Variables for statistics
        self.x_min = tkinter.DoubleVar()
        self.x_max = tkinter.DoubleVar()
        self.x_minimum = ttk.Entry(self.frame_lim, width=30, textvariable=self.x_min)  # テキストボックスの生成
        self.x_maximum = ttk.Entry(self.frame_lim, width=30, textvariable=self.x_max)  # テキストボックスの生成

        self.y_min = tkinter.DoubleVar()
        self.y_max = tkinter.DoubleVar()
        self.y_minimum = ttk.Entry(self.frame_lim, width=30, textvariable=self.y_min)  # テキストボックスの生成
        self.y_maximum = ttk.Entry(self.frame_lim, width=30, textvariable=self.y_max)  # テキストボックスの生成
        self.y_mag = tkinter.DoubleVar()
        self.y_magnification = ttk.Entry(self.frame_lim, width=30, textvariable=self.y_mag)  # テキストボックスの生成
        self.y_move = tkinter.DoubleVar()
        self.y_movement = ttk.Entry(self.frame_lim, width=30, textvariable=self.y_move)  # テキストボックスの生成

        self.d_min = tkinter.IntVar()
        self.d_max = tkinter.IntVar()
        self.d_mean = tkinter.IntVar()
        self.data_minimum = ttk.Entry(self.frame_data, width=30, textvariable=self.d_min, state="readonly")
        self.data_maximum = ttk.Entry(self.frame_data, width=30, textvariable=self.d_max, state="readonly")
        self.data_mean = ttk.Entry(self.frame_data, width=30, textvariable=self.d_mean, state="readonly")
        # Variables for Grid Label
        self.Label_selected_data = ttk.Label(self.frame_plot_data, text="選択中 : ", anchor=tkinter.W)
        self.Label_working_dir = ttk.Label(self.frame_csv_list, text="作業フォルダ: ", anchor=tkinter.W)
        self.Label_selected_csv = ttk.Label(self.frame_csv_list, text="選択中 : ", anchor=tkinter.W)
        self.Label_x_min = ttk.Label(self.frame_lim, text="x最小値")
        self.Label_x_max = ttk.Label(self.frame_lim, text="x最大値")
        self.Label_y_min = ttk.Label(self.frame_lim, text="y最小値")
        self.Label_y_max = ttk.Label(self.frame_lim, text="y最大値")
        self.Label_magnification = ttk.Label(self.frame_lim, text="倍率")
        self.Label_y_move = ttk.Label(self.frame_lim, text="y方向移動")
        self.Label_data_min = ttk.Label(self.frame_data, text="最小値")
        self.Label_data_max = ttk.Label(self.frame_data, text="最大値")
        self.Label_data_mean = ttk.Label(self.frame_data, text="一周平均値")
        # Variables for List box
        self.csv_list = tkinter.StringVar(value=[])
        self.listbox_csv_list = tkinter.Listbox(self.frame_csv_list,
                                                listvariable=self.csv_list,
                                                height=12,
                                                width=60)
        self.plot_data_list = tkinter.StringVar(value=[])
        self.listbox_plot_data_list = tkinter.Listbox(self.frame_plot_data,
                                                      listvariable=self.plot_data_list,
                                                      height=11,
                                                      width=60)
        # Variables for Button
        self.ReDrawButton = ttk.Button(self.frame_data, text="描画", width=15,
                                       command=partial(self.DrawCanvas,
                                                       self.Canvas, self.Canvas2,
                                                       self.ax1, self.ax2))  # ボタンの生成
        self.button_header = ttk.Button(self.frame_plot_data, text="読み込み", command=self.set_header)
        self.button_refer_file = ttk.Button(self.frame_plot_data, text="ファイル選択", command=self.refer_file)
        self.button_refer_dir = ttk.Button(self.frame_csv_list, text="フォルダ選択", command=self.refer_dir)
        # Variables for Scrollbar
        self.scrollbar_v2 = ttk.Scrollbar(self.frame_csv_list, command=self.listbox_csv_list.yview)
        self.scrollbar_h2 = ttk.Scrollbar(self.frame_csv_list, command=self.listbox_csv_list.xview, orient='h')
        self.scrollbar_v = ttk.Scrollbar(self.frame_plot_data, command=self.listbox_plot_data_list.yview)
        self.scrollbar_h = ttk.Scrollbar(self.frame_plot_data, command=self.listbox_plot_data_list.xview, orient='h')
        self.status_var = tkinter.StringVar()
        self.status = ttk.Label(self.master, textvariable=self.status_var, relief=tkinter.SUNKEN, anchor=tkinter.W)

        # Create each function
        self.create_menu()
        self.create_tab()
        self.create_canvas()
        self.create_textbox()
        self.create_statistics()
        self.create_grid_label()
        self.create_list_box()
        self.create_button()
        self.create_scrollbar()

    def create_menu(self):
        # メニューの生成
        menu = tkinter.Menu(self.master)
        self.master.config(menu=menu)
        menu_file = tkinter.Menu(self.master, tearoff=0)
        menu_setting = tkinter.Menu(self.master, tearoff=0)
        # メニューに親メニュー（ファイル）を作成する
        menu.add_cascade(label='ファイル', menu=menu_file)
        menu.add_cascade(label='設定', menu=menu_setting)
        # 親メニューに子メニュー（開く・閉じる）を追加する
        menu_file.add_command(label='ファイルを開く', command=self.refer_file, accelerator='Ctrl+O')
        self.master.bind_all("<Control-o>", self.refer_file)
        menu_file.add_command(label='フォルダを開く', command=self.refer_dir, accelerator='Ctrl+Shift+O')
        self.master.bind_all("<Control-O>", self.open_folder)
        menu_file.add_command(label='グラフを保存する', command=self.save, accelerator='Ctrl+S')
        self.master.bind_all("<Control-s>", self.save)
        menu_file.add_separator()
        menu_file.add_command(label='終了する', command=self.Quit, accelerator='Ctrl+Q')
        self.master.bind_all("<Control-q>", self.Quit)

        self.enableGrid.set(True)  # グリッドの無効/有効の初期値
        menu_setting.add_command(label='グラフ設定', command=self.graph_setting)

    def create_tab(self):
        # ノートブック&タブの生成
        self.nb.add(self.polar_tab, text='極形式グラフ', padding=3)
        self.nb.add(self.descartes_tab, text='直交座標系グラフ', padding=3)
        self.nb.grid(row=0, column=0, sticky=(tkinter.E, tkinter.W,))

    def create_canvas(self):
        # キャンバスの生成
        self.Canvas.get_tk_widget().grid(row=1, column=1)
        self.Canvas.get_tk_widget().columnconfigure(0, weight=1)
        self.Canvas.get_tk_widget().rowconfigure(0, weight=1)

        self.Canvas2.get_tk_widget().grid(row=1, column=1)
        self.Canvas2.get_tk_widget().columnconfigure(0, weight=1)
        self.Canvas2.get_tk_widget().rowconfigure(0, weight=1)

    def create_textbox(self):
        self.Entry_select_directory.grid(row=1, column=2, columnspan=8, sticky=(tkinter.E, tkinter.W))
        self.Entry_csv_path.grid(row=2, column=2, columnspan=9, sticky=(tkinter.E, tkinter.W))
        self.Entry_plot_data.grid(row=1, column=2, columnspan=8, sticky=(tkinter.E, tkinter.W))

    def create_statistics(self):
        self.x_min.set(0)  # Todo: config作りたい
        self.x_max.set(360)
        self.x_minimum.grid(row=1, column=2, padx=10, pady=10)
        self.x_maximum.grid(row=2, column=2, padx=10, pady=10)

        self.y_min.set(0)
        self.y_max.set(500)
        self.y_mag.set(1)
        self.y_move.set(0)
        self.y_minimum.grid(row=1, column=4, padx=10, pady=4)
        self.y_maximum.grid(row=2, column=4, padx=10, pady=4)
        self.y_magnification.grid(row=3, column=4, padx=10, pady=2)
        self.y_movement.grid(row=4, column=4, padx=10, pady=2)

        self.data_minimum.grid(row=1, column=2, padx=10, pady=10, columnspan=2)
        self.data_maximum.grid(row=2, column=2, padx=10, pady=10, columnspan=2)
        self.data_mean.grid(row=3, column=2, padx=10, pady=10, columnspan=2)

    def create_grid_label(self):
        # ラベルに関する諸々の設定
        self.Label_selected_data.grid(row=1, column=1, sticky=tkinter.E)
        self.Label_working_dir.grid(row=1, column=1, sticky=tkinter.E)
        self.Label_selected_csv.grid(row=2, column=1, sticky=tkinter.E)
        self.Label_x_min.grid(row=1, column=1, sticky=tkinter.E)
        self.Label_x_max.grid(row=2, column=1, sticky=tkinter.E)
        self.Label_y_min.grid(row=1, column=3, sticky=tkinter.E)
        self.Label_y_max.grid(row=2, column=3, sticky=tkinter.E)
        self.Label_magnification.grid(row=3, column=3, sticky=tkinter.E)
        self.Label_y_move.grid(row=4, column=3, sticky=tkinter.E)
        self.Label_data_min.grid(row=1, column=1, sticky=tkinter.E)
        self.Label_data_max.grid(row=2, column=1, sticky=tkinter.E)
        self.Label_data_mean.grid(row=3, column=1, sticky=tkinter.E)

    def create_list_box(self):
        # LIST BOXの設定
        self.listbox_csv_list.grid(row=3,
                                   column=1,
                                   columnspan=10,
                                   sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
        self.listbox_csv_list.bind("<<ListboxSelect>>", self.get_csvlist_select_file)
        self.listbox_csv_list.columnconfigure(0, weight=1)
        self.listbox_csv_list.rowconfigure(0, weight=1)
        self.listbox_plot_data_list.grid(row=2,
                                         column=1,
                                         columnspan=10,
                                         sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
        self.listbox_plot_data_list.bind("<<ListboxSelect>>", self.get_csvlist_selected)

    def create_button(self):
        # ボタンに関する諸々の設定
        self.ReDrawButton.grid(row=2, column=5, columnspan=2, pady=10)
        self.button_header.grid(row=0, column=1, columnspan=10, sticky=(tkinter.W, tkinter.E, tkinter.S))
        self.button_refer_file.grid(row=1, column=10, sticky=tkinter.E)
        self.button_refer_dir.grid(row=1, column=10, sticky=tkinter.E)

    def create_scrollbar(self):
        self.scrollbar_v2.grid(row=3, column=11, sticky=(tkinter.N, tkinter.S, tkinter.W))
        self.scrollbar_h2.grid(row=4, column=1, columnspan=10, sticky=(tkinter.E, tkinter.W, tkinter.N))
        self.listbox_csv_list['yscrollcommand'] = self.scrollbar_v2.set
        self.listbox_csv_list['xscrollcommand'] = self.scrollbar_h2.set

        self.scrollbar_v.grid(row=2, column=11, sticky=(tkinter.N, tkinter.S, tkinter.W))
        self.scrollbar_h.grid(row=3, column=1, columnspan=10, sticky=(tkinter.E, tkinter.W, tkinter.N))
        self.listbox_plot_data_list['yscrollcommand'] = self.scrollbar_v.set
        self.listbox_plot_data_list['xscrollcommand'] = self.scrollbar_h.set

        self.status_var.set("Choose .csv data file")
        self.status.grid(row=20, column=0, columnspan=20, sticky=(tkinter.W, tkinter.E, tkinter.S))

    def Quit(self, *event):
        self.master.quit()
        self.master.destroy()
        sys.exit(0)
        # plt.close()

    def open_file(self, *event):
        pass

    def open_folder(self, *event):
        pass

    def DrawCanvas(self, canvas, canvas2, ax, ax_2, colors="gray"):
        value = self.Entry_select_directory.get() + "\\" + self.Entry_csv_path.get()

        if value != '\\' and self.plot_data_name.get() != '':
            qb = QBlade(0, 0, 0, value, value)
            ax.cla()  # 前の描画データの消去
            ax_2.cla()

            csv = qb.initialize()
            x, _d_mean, _d_min, _d_max = qb.mean_plot(csv.loc[:, pd.IndexSlice[self.plot_data_name.get(), 'Degree']],
                                                      csv.loc[:,
                                                      pd.IndexSlice[self.plot_data_name.get(), 'Momentary_Torque']])
            self.d_max.set(_d_max)
            self.d_min.set(_d_min)
            self.d_mean.set(_d_mean)
            ax.plot(np.deg2rad(list(x.index)), x['mean']*self.y_mag.get()+self.y_move.get())
            # ax.plot(np.deg2rad(list(x.index)), x['median'])
            ax_2.plot(x.index, x['mean']*self.y_mag.get()+self.y_move.get())
            # ax_2.plot(x.index, x['median'])
            x_min = self.x_min.get()
            x_max = self.x_max.get()
            y_min = self.y_min.get()
            y_max = self.y_max.get()
            ax.set_ylim([y_min, y_max])
            ax_2.set_xlim([x_min, x_max])
            ax_2.set_ylim([y_min, y_max])
            ax_2.set_xticks(np.arange(0, x_max + 1, 30))

            if self.enableGrid.get():
                major_ticks = np.arange(x_min, x_max + self.grid_interval_x.get(), self.grid_interval_x.get())
                ax_2.set_xticks(major_ticks)
                major_ticks = np.arange(y_min, y_max + self.grid_interval_y.get(), self.grid_interval_y.get())
                ax_2.set_yticks(major_ticks)
                ax_2.grid(which='major')
            else:

                ax_2.grid(False)

            canvas.draw()  # キャンバスの描画
            canvas2.draw()  # キャンバスの描画
            self.status_var.set('"{}" has been drawn'.format(self.plot_data_name.get()))

    def button_selected(self, k):
        if k == -1:
            if len(self.listbox_plot_data_list.curselection()) == 0:
                return
            index = self.listbox_plot_data_list.curselection()[0]
            print(self.listbox_plot_data_list.get(index))
        else:
            if len(k) == 0:
                return
            index = k[0]
            return self.listbox_plot_data_list.get(index)

    def set_header(self):
        self.listbox_plot_data_list.delete(0, tkinter.END)
        value = self.Entry_select_directory.get() + "\\" + self.Entry_csv_path.get()
        if value != '':
            qb = QBlade(0, 0, 0, value, value)
            h = qb.define_header()
            for i in h:
                self.listbox_plot_data_list.insert('end', i)

    def refer_file(self, *event):
        fTyp = [("", "csv")]
        if self.Entry_select_directory.get() == '':
            iDir = os.path.abspath(os.path.dirname(__file__))
        else:
            iDir = self.Entry_select_directory.get()
        selection = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if selection == '':
            return
        self.dir_path.set(os.path.dirname(selection))
        self.file_name.set(os.path.basename(selection))
        self.set_header()
        if self.listbox_plot_data_list.size() != 0:
            self.status_var.set("Select Plot Data")
        else:
            self.status_var.set("Choose .csv data file")

    def refer_dir(self, *event):
        if self.Entry_select_directory.get() == '':
            idir = os.path.abspath(os.path.dirname(__file__))
        else:
            idir = self.Entry_select_directory.get()
        fld = tkinter.filedialog.askdirectory(initialdir=idir)
        if fld == '':
            return
        self.dir_path.set(fld)
        p = Path(fld)
        self.listbox_csv_list.delete(0, tkinter.END)
        for file in list(p.glob("*.csv")):
            self.listbox_csv_list.insert('end', file)
        print(os.path.basename(list(p.glob("*.csv"))[0]))

        pass

    def save(self, *event):
        try:
            idir = os.path.abspath(self.dir_path.get())
            folder_path = tkinter.filedialog.asksaveasfilename(defaultextension=".PNG", initialdir=idir,
                                                               title="Save as")
            if self.nb.index(self.nb.select()) == 0:
                self.fig.savefig(folder_path, format='png', dpi=350, transparent=True)
            elif self.nb.index(self.nb.select()) == 1:
                self.fig2.savefig(folder_path, format='png', dpi=350, transparent=True)
            self.status_var.set("Save done.")
        except:
            import traceback

            traceback.print_exc()
            self.status_var.set("Error occurred")

    def graph_setting(self):
        SettingWindow = None
        try:
            def enable_grid_show():
                partial(self.DrawCanvas, self.Canvas, self.Canvas2, self.ax1, self.ax2)()
                print("{} Grid".format("enable" if self.enableGrid.get() else "disable"))

            def apply_grid_interval_x():
                _grid_interval_x = grid_interval_entry_x.get()
                self.grid_interval_x.set(_grid_interval_x)
                partial(self.DrawCanvas, self.Canvas, self.Canvas2, self.ax1, self.ax2)()
                print("Grid interval set to {}".format(_grid_interval_x))

            def apply_grid_interval_y():
                _grid_interval_y = grid_interval_entry_y.get()
                self.grid_interval_y.set(_grid_interval_y)
                partial(self.DrawCanvas, self.Canvas, self.Canvas2, self.ax1, self.ax2)()
                print("Grid interval set to {}".format(_grid_interval_y))

            if SettingWindow is None or not SettingWindow.winfo_exists():
                SettingWindow = tkinter.Toplevel(self.master)
                SettingWindow.title(u"直交座標系の設定")
                SettingWindow.minsize(300, 150)
                SettingWindow.rowconfigure(0, weight=1)
                SettingWindow.columnconfigure(0, weight=1)
                SettingWindow.grid()

                frame_setting = ttk.Frame(SettingWindow)
                frame_setting.rowconfigure(0, weight=1)
                frame_setting.columnconfigure(0, weight=1)
                frame_setting.grid(sticky=(tkinter.N, tkinter.E, tkinter.S, tkinter.W))

                grid_enable_ax = ttk.Checkbutton(frame_setting, text="グリッドを有効にする", var=self.enableGrid,
                                                 command=enable_grid_show)
                grid_enable_ax.grid(row=1, column=2, padx=10, pady=10, columnspan=1)

                grid_interval_entry_y = ttk.Entry(frame_setting, width=30, textvariable=self.grid_interval_y)
                grid_interval_entry_y.grid(row=2, column=2, padx=10, pady=10, columnspan=1)
                grid_interval_y_label = ttk.Label(frame_setting, text="y軸グリッド間隔 : ", anchor=tkinter.W)
                grid_interval_y_label.grid(row=2, column=1, padx=10)
                grid_interval_y_button = ttk.Button(frame_setting, text="適用", command=apply_grid_interval_y)
                if self.file_name.get() == "":
                    grid_interval_y_button.state(['disabled'])
                grid_interval_y_button.grid(row=2, column=3, padx=10)

                grid_interval_entry_x = ttk.Entry(frame_setting, width=30, textvariable=self.grid_interval_x)
                grid_interval_entry_x.grid(row=3, column=2, padx=10, pady=10, columnspan=1)
                grid_interval_x_label = ttk.Label(frame_setting, text="x軸グリッド間隔 : ", anchor=tkinter.W)
                grid_interval_x_label.grid(row=3, column=1, padx=10)
                grid_interval_x_button = ttk.Button(frame_setting, text="適用", command=apply_grid_interval_x)
                if self.file_name.get() == "":
                    grid_interval_x_button.state(['disabled'])
                grid_interval_x_button.grid(row=3, column=3, padx=10)

        except:
            import traceback
            traceback.print_exc()
            self.status_var.set("Error occurred")

    def get_csvlist_selected(self, *event):
        if len(self.listbox_plot_data_list.curselection()) != 0:
            self.plot_data_name.set(self.listbox_plot_data_list.get(self.listbox_plot_data_list.curselection()[0]))
            # DrawCanvas(event[0], event[1], 0)
            self.DrawCanvas(self.Canvas, self.Canvas2, self.ax1, self.ax2, 0)
            return
        else:
            print("null")
            print(self.plot_data_name.get())
            return

    def get_csvlist_select_file(self, *event):
        if len(self.listbox_csv_list.curselection()) != 0:
            self.file_name.set(os.path.basename(self.listbox_csv_list.get(self.listbox_csv_list.curselection()[0])))
            self.set_header()
            return
