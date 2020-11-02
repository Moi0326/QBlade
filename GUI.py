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
from config import ConfigInit


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

        '''
        CheckButton
        '''
        self.ALL_A = tkinter.StringVar()
        self.ALL_N = tkinter.StringVar()
        self.ALL_T = tkinter.StringVar()
        self.MST_A = tkinter.StringVar()
        self.MST_N = tkinter.StringVar()
        self.MST_T = tkinter.StringVar()
        self.DMST_A = tkinter.StringVar()
        self.DMST_N = tkinter.StringVar()
        self.DMST_T = tkinter.StringVar()
        self.AC_A = tkinter.StringVar()
        self.AC_N = tkinter.StringVar()
        self.AC_T = tkinter.StringVar()
        self.U2DiVA_A = tkinter.StringVar()
        self.U2DiVA_N = tkinter.StringVar()
        self.U2DiVA_T = tkinter.StringVar()
        self.Cactus_A = tkinter.StringVar()
        self.Cactus_N = tkinter.StringVar()
        self.Cactus_T = tkinter.StringVar()
        self.ARDEMA2D_A = tkinter.StringVar()
        self.ARDEMA2D_N = tkinter.StringVar()
        self.ARDEMA2D_T = tkinter.StringVar()
        self.AoA_list = [self.MST_A, self.DMST_A, self.AC_A, self.U2DiVA_A, self.Cactus_A, self.ARDEMA2D_A]
        self.Norm_list = [self.MST_N, self.DMST_N, self.AC_N, self.U2DiVA_N, self.Cactus_N, self.ARDEMA2D_N]
        self.Tan_list = [self.MST_T, self.DMST_T, self.AC_T, self.U2DiVA_T, self.Cactus_T, self.ARDEMA2D_T]

        self.ALL_A.set('0'), self.ALL_N.set('0'), self.ALL_T.set('0')
        self.MST_A.set('0'), self.MST_N.set('0'), self.MST_T.set('0')
        self.DMST_A.set('0'), self.DMST_N.set('0'), self.DMST_T.set('0')
        self.AC_A.set('0'), self.AC_N.set('0'), self.AC_T.set('0')
        self.U2DiVA_A.set('0'), self.U2DiVA_N.set('0'), self.U2DiVA_T.set('0')
        self.Cactus_A.set('0'), self.Cactus_N.set('0'), self.Cactus_T.set('0')
        self.ARDEMA2D_A.set('0'), self.ARDEMA2D_N.set('0'), self.ARDEMA2D_T.set('0')
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
        self.txt_csv = tkinter.StringVar()
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
        self.low_cut = tkinter.IntVar(0)
        self.entry_low_cut = ttk.Entry(self.frame_lim, width=30, textvariable=self.low_cut)

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
        self.Label_plot_range = ttk.Label(self.frame_lim, text="Plot cut-out")
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
        self.button_csv_output = ttk.Button(self.frame_data, text="CSV出力", command=self.csv_output)
        self.button_what_to_plot = ttk.Button(self.frame_data, text="Plotデータ選択", command=self.select_what_to_plot)
        # Variables for Scrollbar
        self.scrollbar_v2 = ttk.Scrollbar(self.frame_csv_list, command=self.listbox_csv_list.yview)
        self.scrollbar_h2 = ttk.Scrollbar(self.frame_csv_list, command=self.listbox_csv_list.xview, orient='h')
        self.scrollbar_v = ttk.Scrollbar(self.frame_plot_data, command=self.listbox_plot_data_list.yview)
        self.scrollbar_h = ttk.Scrollbar(self.frame_plot_data, command=self.listbox_plot_data_list.xview, orient='h')
        self.status_var = tkinter.StringVar()
        self.status = ttk.Label(self.master, textvariable=self.status_var, relief=tkinter.SUNKEN, anchor=tkinter.W)

        self.SettingWindow = None
        self.CSVWindow = None
        self.what_to_plot = None
        self.csv_output_ = None

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
        self.read_config()

    def create_menu(self):
        # メニューの生成
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

    def create_statistics(self):  # Tips: Entry
        self.x_min.set(0)  # Todo: config作りたい
        self.x_max.set(360)
        self.x_minimum.grid(row=1, column=2, padx=10, pady=4)
        self.x_maximum.grid(row=2, column=2, padx=10, pady=4)
        self.entry_low_cut.grid(row=3, column=2, padx=10, pady=4)

        self.y_min.set(0)
        self.y_max.set(500)
        self.y_mag.set(1)
        self.y_move.set(0)
        self.y_minimum.grid(row=1, column=4, padx=10, pady=4)
        self.y_maximum.grid(row=2, column=4, padx=10, pady=4)
        self.y_magnification.grid(row=3, column=4, padx=10, pady=2)
        self.y_movement.grid(row=4, column=4, padx=10, pady=2)

        self.data_minimum.grid(row=1, column=2, padx=10, pady=4, columnspan=2)
        self.data_maximum.grid(row=2, column=2, padx=10, pady=4, columnspan=2)
        self.data_mean.grid(row=3, column=2, padx=10, pady=4, columnspan=2)

    def create_grid_label(self):
        # ラベルに関する諸々の設定
        self.Label_selected_data.grid(row=1, column=1, sticky=tkinter.E)
        self.Label_working_dir.grid(row=1, column=1, sticky=tkinter.E)
        self.Label_selected_csv.grid(row=2, column=1, sticky=tkinter.E)
        self.Label_x_min.grid(row=1, column=1, sticky=tkinter.E)
        self.Label_x_max.grid(row=2, column=1, sticky=tkinter.E)
        self.Label_plot_range.grid(row=3, column=1, sticky=tkinter.E)

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
        self.ReDrawButton.grid(row=2, column=5, columnspan=2, pady=4)
        self.button_header.grid(row=0, column=1, columnspan=10, sticky=(tkinter.W, tkinter.E, tkinter.S))
        self.button_refer_file.grid(row=1, column=10, sticky=tkinter.E)
        self.button_refer_dir.grid(row=1, column=10, sticky=tkinter.E)
        self.button_csv_output.grid(row=3, column=5, columnspan=2, pady=4)
        self.button_what_to_plot.grid(row=4, column=5, columnspan=2, pady=4)

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
        self.save_config()
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
            x, _d_mean, _d_min, _d_max, df_out = qb.mean_plot(
                csv.loc[:, pd.IndexSlice[self.plot_data_name.get(), 'Degree']],
                csv.loc[:, pd.IndexSlice[self.plot_data_name.get(), 'Momentary_Torque']])
            self.d_max.set(_d_max)
            self.d_min.set(_d_min)
            self.d_mean.set(_d_mean)
            # self.txt_csv.set(df_out)
            self.csv_output_ = df_out

            _x_mean = df_out.iloc[:, self.low_cut.get():].mean(axis='columns')
            _x_mean.sort_index(inplace=True)
            if list(_x_mean.index)[0] == 0:
                addition = _x_mean.head(1)
                addition.rename(index=lambda s: 360, inplace=True)
                _x_mean = pd.concat([_x_mean, addition])
            else:
                addition = _x_mean.tail(1)
                addition.rename(index=lambda s: 0, inplace=True)
                _x_mean = pd.concat([addition, _x_mean])
            _x_mean.sort_index(inplace=True)
            print("#####", _x_mean)
            descartes_deg = list(_x_mean.index)
            radian_deg = np.deg2rad(list(_x_mean.index))
            ax.plot(radian_deg, _x_mean * self.y_mag.get() + self.y_move.get())
            # ax.plot(np.deg2rad(list(x.index)), x['median']*self.y_mag.get()+self.y_move.get())
            ax_2.plot(descartes_deg, _x_mean * self.y_mag.get() + self.y_move.get())
            # ax_2.plot(x.index, x['median']*self.y_mag.get()+self.y_move.get())
            x_min = self.x_min.get()
            x_max = self.x_max.get()
            y_min = self.y_min.get()
            y_max = self.y_max.get()
            ax.set_ylim([y_min, y_max])
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
            self.txt_csv.set("")
            print(df_out.columns.values)
            self.txt_csv.set(
                "deg" + "," + ",".join([str(i) for i in range(self.low_cut.get(), df_out.columns.values[-1] + 1)]))
            # self.txt_csv.set(
            #     str(descartes_deg[0]) + "," + ",".join(list(map(str, df_out.iloc[0, self.low_cut.get():].tolist()))))
            csv_listed = []
            print(_x_mean.tolist())
            for i in range(0, len(descartes_deg) - 1):
                # print(i)
                csv_listed.append(
                    [(int((descartes_deg[i] + 270) % 360)),
                     ",".join(list(map(str, df_out.iloc[i, self.low_cut.get():].tolist()))),
                     str(np.average(df_out.iloc[i, self.low_cut.get():].tolist()))]
                )
                if int((descartes_deg[i] + 270) % 360) == 355:
                    csv_listed.append([360,
                                       ",".join(list(map(str, df_out.iloc[18,  # 18 is index of "0 degree"
                                                              self.low_cut.get():].tolist()))),
                                       str(_x_mean.tolist()[0])])
            csv_listed = sorted(csv_listed, key=lambda s: s[0])
            for i in range(0, len(descartes_deg)):
                csv_listed[i][0] = str(csv_listed[i][0])
            for i in range(0, len(descartes_deg)):
                self.txt_csv.set(self.txt_csv.get() + "\n" + ",".join(csv_listed[i]))

            # for i in range(0, len(descartes_deg) - 1):
            #                 # print(i)
            #                 self.txt_csv.set(self.txt_csv.get() + "\n" +
            #                                  str(int((descartes_deg[i] + 270) % 360)) + "," +
            #                                  ",".join(list(map(str, df_out.iloc[i, self.low_cut.get():].tolist()))))
            #

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

            if self.SettingWindow is None or not self.SettingWindow.winfo_exists():
                self.SettingWindow = tkinter.Toplevel(self.master)
                self.SettingWindow.title(u"直交座標系の設定")
                self.SettingWindow.minsize(300, 150)
                self.SettingWindow.rowconfigure(0, weight=1)
                self.SettingWindow.columnconfigure(0, weight=1)
                self.SettingWindow.grid()

                frame_setting = ttk.Frame(self.SettingWindow)
                frame_setting.rowconfigure(0, weight=1)
                frame_setting.columnconfigure(0, weight=1)
                frame_setting.grid(sticky=(tkinter.N, tkinter.E, tkinter.S, tkinter.W))

                grid_enable_ax = ttk.Checkbutton(frame_setting, text="グリッドを有効にする", var=self.enableGrid,
                                                 command=enable_grid_show)
                grid_enable_ax.grid(row=1, column=2, padx=10, pady=4, columnspan=1)

                grid_interval_entry_y = ttk.Entry(frame_setting, width=30, textvariable=self.grid_interval_y)
                grid_interval_entry_y.grid(row=2, column=2, padx=10, pady=4, columnspan=1)
                grid_interval_y_label = ttk.Label(frame_setting, text="y軸グリッド間隔 : ", anchor=tkinter.W)
                grid_interval_y_label.grid(row=2, column=1, padx=10)
                grid_interval_y_button = ttk.Button(frame_setting, text="適用", command=apply_grid_interval_y)
                if self.file_name.get() == "":
                    grid_interval_y_button.state(['disabled'])
                grid_interval_y_button.grid(row=2, column=3, padx=10)

                grid_interval_entry_x = ttk.Entry(frame_setting, width=30, textvariable=self.grid_interval_x)
                grid_interval_entry_x.grid(row=3, column=2, padx=10, pady=4, columnspan=1)
                grid_interval_x_label = ttk.Label(frame_setting, text="x軸グリッド間隔 : ", anchor=tkinter.W)
                grid_interval_x_label.grid(row=3, column=1, padx=10)
                grid_interval_x_button = ttk.Button(frame_setting, text="適用", command=apply_grid_interval_x)
                if self.file_name.get() == "":
                    grid_interval_x_button.state(['disabled'])
                grid_interval_x_button.grid(row=3, column=3, padx=10)
            else:
                self.SettingWindow.attributes('-topmost', True)
                self.SettingWindow.attributes('-topmost', False)

        except:
            import traceback
            traceback.print_exc()
            self.status_var.set("Error occurred")

    def csv_output(self):
        try:
            if self.CSVWindow is None or not self.CSVWindow.winfo_exists():
                self.CSVWindow = tkinter.Toplevel(self.master)
                self.CSVWindow.title(u"グラフデータ")
                self.CSVWindow.minsize(300, 600)
                self.CSVWindow.rowconfigure(0, weight=1)
                self.CSVWindow.columnconfigure(0, weight=1)
                self.CSVWindow.grid()
                ini_name = self.Entry_plot_data.get()

                def save_to_csv(*event):
                    idir_ = self.Entry_select_directory.get()
                    fld = tkinter.filedialog.asksaveasfilename(filetypes=[("csv Files", ".csv")],
                                                               initialdir=idir_, initialfile=ini_name + '.csv')
                    if fld == '':
                        return
                    p = Path(fld)
                    print(p)
                    with open(p, mode="w") as f:
                        f.write(self.txt_csv.get())

                frame_csv_output = ttk.Frame(self.CSVWindow)
                frame_csv_output.rowconfigure(0, weight=1)
                frame_csv_output.columnconfigure(0, weight=1)
                frame_csv_output.grid(sticky=(tkinter.N, tkinter.E, tkinter.S, tkinter.W))

                button_csv_output_save = ttk.Button(frame_csv_output, text="CSV保存", command=save_to_csv)
                button_csv_output_save.grid(row=2, column=0, sticky=(tkinter.N, tkinter.E, tkinter.S, tkinter.W))

                txt_csv_output = tkinter.Text(frame_csv_output, wrap=tkinter.NONE)
                txt_csv_output.insert('1.0', self.txt_csv.get())
                txt_csv_output.grid(row=0, column=0, sticky=(tkinter.N, tkinter.E, tkinter.S, tkinter.W))

                # Scrollbar
                scrollbar = ttk.Scrollbar(
                    frame_csv_output,
                    orient=tkinter.VERTICAL,
                    command=txt_csv_output.yview)
                scrollbar_2 = ttk.Scrollbar(frame_csv_output, command=txt_csv_output.xview, orient='h')
                scrollbar.grid(row=0, column=1, sticky=(tkinter.N, tkinter.S))
                scrollbar_2.grid(row=1, column=0, sticky=(tkinter.E, tkinter.W))

                txt_csv_output['xscrollcommand'] = scrollbar_2.set
                txt_csv_output['yscrollcommand'] = scrollbar.set
            else:
                self.CSVWindow.attributes('-topmost', True)
                self.CSVWindow.attributes('-topmost', False)
        except:
            import traceback
            traceback.print_exc()
            self.status_var.set("Error occurred")

    def other_method_plot(self, fn):
        self.ax1.cla()  # 前の描画データの消去
        self.ax2.cla()
        ls = ['MST', 'DMST', 'Actuator Cylinder', 'U2DiVA', 'Cactus', 'ARDEMA2D']
        aoa_file = 'SIMcsv/AoA.csv'
        norm_file = 'SIMcsv/NormalLoad.csv'
        tan_file = 'SIMcsv/TanLoad.csv'
        aoa_df = pd.read_csv(aoa_file)
        norm_df = pd.read_csv(norm_file)
        tan_df = pd.read_csv(tan_file)
        df = [aoa_df, norm_df, tan_df]
        # df_columns = list(df.columns)

        ls_a = list(df[0].columns)
        ls_n = list(df[1].columns)
        ls_t = list(df[2].columns)
        ls_name = [ls_a,ls_n,ls_t]
        ls_2 = []
        for i in range(len(ls)):
            ls_2.append([self.AoA_list[i].get(),
                         self.Norm_list[i].get(),
                         self.Tan_list[i].get()])
        for i in range(len(ls)):
            for j in range(3):
                if ls_2[i][j] == '1':
                    print(ls_2[i][j])
                    self.ax1.plot(df[j][ls_name[j][i * 2]],
                                  df[j][ls_name[j][i * 2 + 1]],
                                  label=ls[i])
                    print('Draw',ls_name[j][i*2])
                    self.ax2.plot(df[j][ls_name[j][i * 2]],
                                  df[j][ls_name[j][i * 2 + 1]],
                                  label=ls[i])
        self.Canvas.draw()
        self.Canvas2.draw()

        # print(df)
        print(ls_2)

    def select_what_to_plot(self):
        try:
            if self.what_to_plot is None or not self.what_to_plot.winfo_exists():
                self.what_to_plot = tkinter.Toplevel(self.master)
                self.what_to_plot.title(u"What to Plot")
                # self.what_to_plot.minsize(450, 450)
                self.what_to_plot.rowconfigure(0, weight=1)
                self.what_to_plot.columnconfigure(0, weight=1)
                self.what_to_plot.grid()
                ini_name = self.Entry_plot_data.get()

                frame_what_to_plot = ttk.Frame(self.what_to_plot)
                frame_what_to_plot.rowconfigure(0, weight=1)
                frame_what_to_plot.columnconfigure(0, weight=1)
                frame_what_to_plot.grid(sticky=(tkinter.N, tkinter.E, tkinter.S, tkinter.W))

                '''
                他シミュレーションのデータラベルなど
                '''

                ALL_Method = ttk.Label(frame_what_to_plot, text='ALL')
                MST = ttk.Label(frame_what_to_plot, text='MST')
                DMST = ttk.Label(frame_what_to_plot, text='DMST')
                AC = ttk.Label(frame_what_to_plot, text='Actuator Cylinder')
                U2DiVA = ttk.Label(frame_what_to_plot, text='U2DiVA')
                Cactus = ttk.Label(frame_what_to_plot, text='Cactus')
                ARDEMA2D = ttk.Label(frame_what_to_plot, text='ARDEMA2D')
                AoA = ttk.Label(frame_what_to_plot, text='Angle of attack')
                NormalLoad = ttk.Label(frame_what_to_plot, text='Normal Load')
                TangentialLoad = ttk.Label(frame_what_to_plot, text='Tangential Load')

                ALL_Method.grid(row=1, column=0, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                MST.grid(row=2, column=0, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                DMST.grid(row=3, column=0, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                AC.grid(row=4, column=0, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                U2DiVA.grid(row=5, column=0, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                Cactus.grid(row=6, column=0, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                ARDEMA2D.grid(row=7, column=0, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                AoA.grid(row=0, column=1, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                NormalLoad.grid(row=0, column=2, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
                TangentialLoad.grid(row=0, column=3, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))

                def aoa_on():
                    self.MST_A.set(self.ALL_A.get())
                    self.DMST_A.set(self.ALL_A.get())
                    self.AC_A.set(self.ALL_A.get())
                    self.U2DiVA_A.set(self.ALL_A.get())
                    self.Cactus_A.set(self.ALL_A.get())
                    self.ARDEMA2D_A.set(self.ALL_A.get())

                def norm_on():
                    self.MST_N.set(self.ALL_N.get())
                    self.DMST_N.set(self.ALL_N.get())
                    self.AC_N.set(self.ALL_N.get())
                    self.U2DiVA_N.set(self.ALL_N.get())
                    self.Cactus_N.set(self.ALL_N.get())
                    self.ARDEMA2D_N.set(self.ALL_N.get())

                def tang_on():
                    self.MST_T.set(self.ALL_T.get())
                    self.DMST_T.set(self.ALL_T.get())
                    self.AC_T.set(self.ALL_T.get())
                    self.U2DiVA_T.set(self.ALL_T.get())
                    self.Cactus_T.set(self.ALL_T.get())
                    self.ARDEMA2D_T.set(self.ALL_T.get())

                cALL_A = ttk.Checkbutton(frame_what_to_plot,
                                         padding=5,
                                         onvalue='1',
                                         offvalue='0',
                                         variable=self.ALL_A,
                                         command=aoa_on)
                cALL_N = ttk.Checkbutton(frame_what_to_plot,
                                         padding=5,
                                         onvalue='1',
                                         offvalue='0',
                                         variable=self.ALL_N,
                                         command=norm_on)
                cALL_T = ttk.Checkbutton(frame_what_to_plot,
                                         padding=5,
                                         onvalue='1',
                                         offvalue='0',
                                         variable=self.ALL_T,
                                         command=tang_on)
                cMST_A = ttk.Checkbutton(frame_what_to_plot,
                                         padding=5,
                                         onvalue='1',
                                         offvalue='0',
                                         variable=self.MST_A,
                                         command=lambda: print(self.MST_A.get()))
                cMST_N = ttk.Checkbutton(frame_what_to_plot,
                                         padding=5,
                                         onvalue='1',
                                         offvalue='0',
                                         variable=self.MST_N,
                                         command=lambda: print(self.MST_N.get()))
                cMST_T = ttk.Checkbutton(frame_what_to_plot,
                                         padding=5,
                                         onvalue='1',
                                         offvalue='0',
                                         variable=self.MST_T,
                                         command=lambda: print(self.MST_T.get()))
                cDMST_A = ttk.Checkbutton(frame_what_to_plot,
                                          padding=5,
                                          onvalue='1',
                                          offvalue='0',
                                          variable=self.DMST_A,
                                          command=lambda: print(self.DMST_A.get()))
                cDMST_N = ttk.Checkbutton(frame_what_to_plot,
                                          padding=5,
                                          onvalue='1',
                                          offvalue='0',
                                          variable=self.DMST_N,
                                          command=lambda: print(self.DMST_N.get()))
                cDMST_T = ttk.Checkbutton(frame_what_to_plot,
                                          padding=5,
                                          onvalue='1',
                                          offvalue='0',
                                          variable=self.DMST_T,
                                          command=lambda: print(self.DMST_T.get()))
                cAC_A = ttk.Checkbutton(frame_what_to_plot,
                                        padding=5,
                                        onvalue='1',
                                        offvalue='0',
                                        variable=self.AC_A,
                                        command=lambda: print(self.AC_A.get()))
                cAC_N = ttk.Checkbutton(frame_what_to_plot,
                                        padding=5,
                                        onvalue='1',
                                        offvalue='0',
                                        variable=self.AC_N,
                                        command=lambda: print(self.AC_N.get()))
                cAC_T = ttk.Checkbutton(frame_what_to_plot,
                                        padding=5,
                                        onvalue='1',
                                        offvalue='0',
                                        variable=self.AC_T,
                                        command=lambda: print(self.AC_T.get()))
                cU2DiVA_A = ttk.Checkbutton(frame_what_to_plot,
                                            padding=5,
                                            onvalue='1',
                                            offvalue='0',
                                            variable=self.U2DiVA_A,
                                            command=lambda: print(self.U2DiVA_A.get()))
                cU2DiVA_N = ttk.Checkbutton(frame_what_to_plot,
                                            padding=5,
                                            onvalue='1',
                                            offvalue='0',
                                            variable=self.U2DiVA_N,
                                            command=lambda: print(self.U2DiVA_N.get()))
                cU2DiVA_T = ttk.Checkbutton(frame_what_to_plot,
                                            padding=5,
                                            onvalue='1',
                                            offvalue='0',
                                            variable=self.U2DiVA_T,
                                            command=lambda: print(self.U2DiVA_T.get()))
                cCactus_A = ttk.Checkbutton(frame_what_to_plot,
                                            padding=5,
                                            onvalue='1',
                                            offvalue='0',
                                            variable=self.Cactus_A,
                                            command=lambda: print(self.Cactus_A.get()))
                cCactus_N = ttk.Checkbutton(frame_what_to_plot,
                                            padding=5,
                                            onvalue='1',
                                            offvalue='0',
                                            variable=self.Cactus_N,
                                            command=lambda: print(self.Cactus_N.get()))
                cCactus_T = ttk.Checkbutton(frame_what_to_plot,
                                            padding=5,
                                            onvalue='1',
                                            offvalue='0',
                                            variable=self.Cactus_T,
                                            command=lambda: print(self.Cactus_T.get()))
                cARDEMA2D_A = ttk.Checkbutton(frame_what_to_plot,
                                              padding=5,
                                              onvalue='1',
                                              offvalue='0',
                                              variable=self.ARDEMA2D_A,
                                              command=lambda: print(self.ARDEMA2D_A.get()))
                cARDEMA2D_N = ttk.Checkbutton(frame_what_to_plot,
                                              padding=5,
                                              onvalue='1',
                                              offvalue='0',
                                              variable=self.ARDEMA2D_N,
                                              command=lambda: print(self.ARDEMA2D_N.get()))
                cARDEMA2D_T = ttk.Checkbutton(frame_what_to_plot,
                                              padding=5,
                                              onvalue='1',
                                              offvalue='0',
                                              variable=self.ARDEMA2D_T,
                                              command=self.other_method_plot('SIMcsv/AoA.csv'))
                # Layout
                cALL_A.grid(row=1, column=1), cALL_N.grid(row=1, column=2), cALL_T.grid(row=1, column=3)
                cMST_A.grid(row=2, column=1), cMST_N.grid(row=2, column=2), cMST_T.grid(row=2, column=3)
                cDMST_A.grid(row=3, column=1), cDMST_N.grid(row=3, column=2), cDMST_T.grid(row=3, column=3)
                cAC_A.grid(row=4, column=1), cAC_N.grid(row=4, column=2), cAC_T.grid(row=4, column=3)
                cU2DiVA_A.grid(row=5, column=1), cU2DiVA_N.grid(row=5, column=2), cU2DiVA_T.grid(row=5, column=3)
                cCactus_A.grid(row=6, column=1), cCactus_N.grid(row=6, column=2), cCactus_T.grid(row=6, column=3)
                cARDEMA2D_A.grid(row=7, column=1), cARDEMA2D_N.grid(row=7, column=2), cARDEMA2D_T.grid(row=7, column=3)



            else:
                self.what_to_plot.attributes('-topmost', True)
                self.what_to_plot.attributes('-topmost', False)
        except:
            import traceback
            traceback.print_exc()
            self.status_var.set("Error occurred")

    def csv_output_save(self):
        try:
            pass

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

    def read_config(self):
        config = ConfigInit()
        self.dir_path.set(config.w_dir)
        self.x_min.set(config.x_min_c)
        self.x_max.set(config.x_max_c)
        self.y_min.set(config.y_min_c)
        self.y_max.set(config.y_max_c)
        self.low_cut.set(config.p_cutout_c)
        self.grid_interval_x.set(config.grid_x_c)
        self.grid_interval_y.set(config.grid_y_c)

        fld = self.dir_path.get()
        p = Path(fld)
        self.listbox_csv_list.delete(0, tkinter.END)
        for file in list(p.glob("*.csv")):
            self.listbox_csv_list.insert('end', file)
        # print(os.path.basename(list(p.glob("*.csv"))[0]))

    def save_config(self):
        import configparser
        config = configparser.ConfigParser()
        # config.read('./config.ini')
        config['CSVs'] = {
            'Working Directory': self.dir_path.get()
        }
        config['GraphSetting'] = {
            'x min': self.x_min.get(),
            'x max': self.x_max.get(),
            'y min': self.y_min.get(),
            'y max': self.y_max.get(),
            'Plot cut-out': self.low_cut.get(),
            'Grid x': self.grid_interval_x.get(),
            'Grid y': self.grid_interval_y.get()
        }

        with open('./config.ini', 'w') as f:
            config.write(f)
