# Created by Umemoto at 2019/05/08
# -*-coding:utf-8-*-
"""
参考
    http://b4rracud4.hatenadiary.jp/entry/20181207/1544129263
    https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_sgskip.html
    https://pg-chain.com/python-tkinter-entry
"""
# import tkinter
from pathlib import Path
from tkinter import ttk
import tkinter.filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as tick
from functools import partial
import pandas as pd
import numpy as np
from matplotlib import rcParams
import os
import sys
from QBlade_processing import QBlade

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Sans', 'BIZ UDGothic', 'Yu Gothic', 'Meiryo', 'Noto Sans CJK JP',
                               'IPAexGothic', 'DejaVu Sans']


def Quit(*event):
    root.quit()
    root.destroy()
    sys.exit(0)
    # plt.close()


def open_file(*event):
    pass


def open_folder(*event):
    pass


def DrawCanvas(canvas, canvas2, ax, ax_2, colors="gray"):
    value = Entry_select_directory.get() + "\\" + Entry_csv_path.get()
    # qb.initialize()
    # print(qb.define_header())

    # if val.get():
    #     if len(file2.get()) == 0:
    #         return
    #     label1 = file2.get()
    # else:
    #     label1 = plot_title.get()

    if value != '\\' and file2.get() != '':
        qb = QBlade(0, 0, 0, value, value)
        # EditBox.delete(0, tkinter.END)
        ax.cla()  # 前の描画データの消去
        ax_2.cla()
        # ax.set_title(label1)

        csv = qb.initialize()
        x, _d_mean, _d_min, _d_max = qb.mean_plot(csv.loc[:, pd.IndexSlice[file2.get(), 'Degree']],
                                                  csv.loc[:,
                                                  pd.IndexSlice[file2.get(), 'Momentary_Torque']])
        d_max.set(_d_max)
        d_min.set(_d_min)
        d_mean.set(_d_mean)
        ax.plot(np.deg2rad(x[0]), x[1])
        ax_2.plot(x[0], x[1])
        x_min = xmin.get()
        x_max = xmax.get()
        y_min = ymin.get()
        y_max = ymax.get()
        # ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        ax_2.set_xlim([x_min, x_max])
        ax_2.set_ylim([y_min, y_max])
        ax_2.set_xticks(np.arange(0, x_max + 1, 30))
        # fig2.gca().xaxis.set_minor_locator(tick.MultipleLocator(30))
        # fig2.gca().yaxis.set_minor_locator(tick.MultipleLocator(50))

        if enableGrid.get():
            major_ticks = np.arange(x_min, x_max + 1, grid_interval_x.get())
            ax_2.set_xticks(major_ticks)
            major_ticks = np.arange(y_min, y_max + 1, grid_interval_y.get())
            ax_2.set_yticks(major_ticks)
            ax_2.grid(which='major')
        else:

            ax_2.grid(False)

        # ax.legend(framealpha=1)

        canvas.draw()  # キャンバスの描画
        canvas2.draw()  # キャンバスの描画
        status_var.set('"{}" has been drawn'.format(file2.get()))


def button_selected(l):
    # l = listbox.curselection()
    if l == -1:
        if len(plot_data_list.curselection()) == 0:
            return
        index = plot_data_list.curselection()[0]
        print(plot_data_list.get(index))
    else:
        if len(l) == 0:
            return
        index = l[0]
        return plot_data_list.get(index)


def set_header():
    plot_data_list.delete(0, tkinter.END)
    value = Entry_select_directory.get() + "\\" + Entry_csv_path.get()
    if value != '':
        qb = QBlade(0, 0, 0, value, value)
        h = qb.define_header()
        for i in h:
            plot_data_list.insert('end', i)


def refer_file(*event):
    fTyp = [("", "csv")]
    if Entry_select_directory.get() == '':
        iDir = os.path.abspath(os.path.dirname(__file__))
    else:
        iDir = Entry_select_directory.get()
    selection = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    if selection == '':
        return
    dir1.set(os.path.dirname(selection))
    file1.set(os.path.basename(selection))
    set_header()
    if plot_data_list.size() != 0:
        status_var.set("Select Plot Data")
    else:
        status_var.set("Choose .csv data file")


def refer_dir(*event):
    if Entry_select_directory.get() == '':
        idir = os.path.abspath(os.path.dirname(__file__))
    else:
        idir = Entry_select_directory.get()
    fld = tkinter.filedialog.askdirectory(initialdir=idir)
    if fld == '':
        return
    dir1.set(fld)
    p = Path(fld)
    csv_list.delete(0, tkinter.END)
    for file in list(p.glob("*.csv")):
        csv_list.insert('end', file)
    print(os.path.basename(list(p.glob("*.csv"))[0]))

    pass


def save(*event):
    try:
        idir = os.path.abspath(dir1.get())
        folder_path = tkinter.filedialog.asksaveasfilename(defaultextension=".PNG", initialdir=idir, title="Save as")
        if nb.index(nb.select()) == 0:
            fig.savefig(folder_path, format='png', dpi=350, transparent=True)
        elif nb.index(nb.select()) == 1:
            fig2.savefig(folder_path, format='png', dpi=350, transparent=True)
        status_var.set("Save done.")
    except:
        import traceback

        traceback.print_exc()
        status_var.set("Error occurred")


def graph_setting(*event):
    SettingWindow = None
    try:
        def enable_grid_show(*event):
            partial(DrawCanvas, Canvas, Canvas2, ax1, ax2)()
            print("{} Grid".format("enable" if enableGrid.get() else "disable"))

        def apply_grid_interval_x(*event):
            _grid_interval_x = grid_interval_entry_x.get()
            grid_interval_x.set(_grid_interval_x)
            partial(DrawCanvas, Canvas, Canvas2, ax1, ax2)()
            print("Grid interval set to {}".format(_grid_interval_x))

        def apply_grid_interval_y(*event):
            _grid_interval_y = grid_interval_entry_y.get()
            grid_interval_y.set(_grid_interval_y)
            partial(DrawCanvas, Canvas, Canvas2, ax1, ax2)()
            print("Grid interval set to {}".format(_grid_interval_y))

        if SettingWindow is None or not SettingWindow.winfo_exists():
            SettingWindow = tkinter.Toplevel(root)
            SettingWindow.title(u"直交座標系の設定")
            SettingWindow.minsize(300, 150)
            SettingWindow.rowconfigure(0, weight=1)
            SettingWindow.columnconfigure(0, weight=1)
            SettingWindow.grid()

            frame_setting = ttk.Frame(SettingWindow)
            frame_setting.rowconfigure(0, weight=1)
            frame_setting.columnconfigure(0, weight=1)
            frame_setting.grid(sticky=(tkinter.N, tkinter.E, tkinter.S, tkinter.W))

            grid_enable_ax = ttk.Checkbutton(frame_setting, text="グリッドを有効にする", var=enableGrid, command=enable_grid_show)
            grid_enable_ax.grid(row=1, column=2, padx=10, pady=10, columnspan=1)

            grid_interval_entry_y = ttk.Entry(frame_setting, width=30, textvariable=grid_interval_y)
            grid_interval_entry_y.grid(row=2, column=2, padx=10, pady=10, columnspan=1)
            grid_interval_y_label = ttk.Label(frame_setting, text="y軸グリッド間隔 : ", anchor=tkinter.W)
            grid_interval_y_label.grid(row=2, column=1, padx=10)
            grid_interval_y_button = ttk.Button(frame_setting, text="適用", command=apply_grid_interval_y)
            if file1.get() == "":
                grid_interval_y_button.state(['disabled'])
            grid_interval_y_button.grid(row=2, column=3, padx=10)

            grid_interval_entry_x = ttk.Entry(frame_setting, width=30, textvariable=grid_interval_x)
            grid_interval_entry_x.grid(row=3, column=2, padx=10, pady=10, columnspan=1)
            grid_interval_x_label = ttk.Label(frame_setting, text="x軸グリッド間隔 : ", anchor=tkinter.W)
            grid_interval_x_label.grid(row=3, column=1, padx=10)
            grid_interval_x_button = ttk.Button(frame_setting, text="適用", command=apply_grid_interval_x)
            if file1.get() == "":
                grid_interval_x_button.state(['disabled'])
            grid_interval_x_button.grid(row=3, column=3, padx=10)



    except:
        import traceback

        traceback.print_exc()
        status_var.set("Error occurred")


def get_csvlist_selected(*event):
    if len(plot_data_list.curselection()) != 0:
        file2.set(plot_data_list.get(plot_data_list.curselection()[0]))
        # DrawCanvas(event[0], event[1], 0)
        DrawCanvas(Canvas, Canvas2, ax1, ax2, 0)
        return
    else:
        print("null")
        print(file2.get())
        return


def get_csvlist_select_file(*event):
    if len(csv_list.curselection()) != 0:
        file1.set(os.path.basename(csv_list.get(csv_list.curselection()[0])))
        set_header()
        return


if __name__ == "__main__":
    try:
        # GUIの生成
        root = tkinter.Tk()
        root.title(u"QBlade")
        root.columnconfigure(0, weight=1, uniform='group1')
        root.rowconfigure(0, weight=1, uniform='group1')
        # root.resizable(width=False, height=False)  # ウィンドウサイズ固定

        frame_Graph = tkinter.Frame(root, width=300, height=300, bd=2, relief="ridge")
        frame_Graph.grid(row=0, column=0, rowspan=10, columnspan=10)

        # 子フレームの生成
        # frame = tkinter.Frame(root, width=500, height=300, bg="white")
        # frame.grid(row=2, column=11, columnspan=5)

        data_list = ttk.Frame(root)
        data_list.grid(row=1, column=11, columnspan=10, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
        # data_list.columnconfigure(0, weight=1)
        # data_list.rowconfigure(0, weight=1)
        frame_csv_list = ttk.Frame(data_list)
        frame_csv_list.grid(row=1, column=1, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
        # frame_csv_list.columnconfigure(0, weight=1)
        # frame_csv_list.columnconfigure(1, weight=1)
        # frame_csv_list.rowconfigure(0, weight=1)
        # frame_csv_list.rowconfigure(1, weight=1)
        frame_plot_data = ttk.Frame(data_list)
        frame_plot_data.grid(row=2, column=1)

        config = tkinter.Frame(root, width=300, height=300, bd=2)
        config.grid(row=11, column=1)
        # frame_label = tkinter.Frame(config, width=300, height=300, bd=2, relief="ridge")
        # frame_label.grid(row=1, column=1)
        frame_lim = tkinter.Frame(config, width=300, height=300, bd=2, relief="ridge")
        frame_lim.grid(row=1, column=2)

        frame_data = tkinter.Frame(root, bd=2, relief="ridge")
        frame_data.grid(row=11, column=11)

        # メニューの生成
        men = tkinter.Menu(root)
        root.config(menu=men)
        # メニューに親メニュー（ファイル）を作成する
        menu_file = tkinter.Menu(root, tearoff=0)
        menu_setting = tkinter.Menu(root, tearoff=0)
        men.add_cascade(label='ファイル', menu=menu_file)
        men.add_cascade(label='設定', menu=menu_setting)

        # 親メニューに子メニュー（開く・閉じる）を追加する
        menu_file.add_command(label='ファイルを開く', command=refer_file, accelerator='Ctrl+O')
        root.bind_all("<Control-o>", refer_file)
        menu_file.add_command(label='フォルダを開く', command=refer_dir, accelerator='Ctrl+Shift+O')
        root.bind_all("<Control-O>", open_folder)
        menu_file.add_command(label='グラフを保存する', command=save, accelerator='Ctrl+S')
        root.bind_all("<Control-s>", save)
        menu_file.add_separator()
        menu_file.add_command(label='終了する', command=Quit, accelerator='Ctrl+Q')
        root.bind_all("<Control-q>", Quit)

        enableGrid = tkinter.BooleanVar()
        enableGrid.set(True)
        grid_interval_x = tkinter.DoubleVar(value=100)
        # grid_interval_x.set(120)
        grid_interval_y = tkinter.DoubleVar(value=100)
        # grid_interval_y.set(100)
        menu_setting.add_command(label='グラフ設定', command=graph_setting)

        # グラフの設定Q
        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='polar')
        fig.gca().set_aspect('equal', adjustable='box')  # グラフ領域の調整
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        # fig2.gca().set_aspect('equal', adjustable='box')  # グラフ領域の調整
        # fig2.gca().set_aspect('equal', adjustable='box')  # グラフ領域の調整
        # plt.close()

        # ノートブック&タブの生成
        nb = ttk.Notebook(frame_Graph)
        polar_tab = tkinter.Frame(nb)
        Descartes_tab = tkinter.Frame(nb)
        nb.add(polar_tab, text='極形式グラフ', padding=3)
        nb.add(Descartes_tab, text='直交座標系グラフ', padding=3)
        nb.grid(row=0, column=0, sticky=(tkinter.E, tkinter.W,))

        # キャンバスの生成
        Canvas = FigureCanvasTkAgg(fig, master=polar_tab)
        Canvas.get_tk_widget().grid(row=1, column=1)
        Canvas.get_tk_widget().columnconfigure(0, weight=1)
        Canvas.get_tk_widget().rowconfigure(0, weight=1)

        Canvas2 = FigureCanvasTkAgg(fig2, master=Descartes_tab)
        Canvas2.get_tk_widget().grid(row=1, column=1)
        Canvas2.get_tk_widget().columnconfigure(0, weight=1)
        Canvas2.get_tk_widget().rowconfigure(0, weight=1)

        # テキストボックスに関する諸々の設定
        dir1 = tkinter.StringVar()
        Entry_select_directory = ttk.Entry(frame_csv_list, textvariable=dir1, state="readonly")  # テキストボックスの生成
        Entry_select_directory.grid(row=1, column=2, columnspan=8, sticky=(tkinter.E, tkinter.W))
        file1 = tkinter.StringVar()
        Entry_csv_path = ttk.Entry(frame_csv_list, textvariable=file1, state="readonly")  # テキストボックスの生成
        Entry_csv_path.grid(row=2, column=2, columnspan=9, sticky=(tkinter.E, tkinter.W))

        file2 = tkinter.StringVar()
        Entry_plot_data = ttk.Entry(frame_plot_data, textvariable=file2, state="readonly")  # テキストボックスの生成
        Entry_plot_data.grid(row=1, column=2, columnspan=8, sticky=(tkinter.E, tkinter.W))

        # plot_title = ttk.Entry(frame_label, width=30)  # テキストボックスの生成
        # plot_title.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        xmin = tkinter.IntVar()
        xmin.set(0)
        x_min = ttk.Entry(frame_lim, width=30, textvariable=xmin)  # テキストボックスの生成
        x_min.grid(row=1, column=2, padx=10, pady=10)
        xmax = tkinter.IntVar()
        xmax.set(360)
        x_max = ttk.Entry(frame_lim, width=30, textvariable=xmax)  # テキストボックスの生成
        x_max.grid(row=2, column=2, padx=10, pady=10)

        ymin = tkinter.IntVar()
        ymin.set(0)
        y_min = ttk.Entry(frame_lim, width=30, textvariable=ymin)  # テキストボックスの生成
        y_min.grid(row=1, column=4, padx=10, pady=10)
        ymax = tkinter.IntVar()
        ymax.set(500)
        y_max = ttk.Entry(frame_lim, width=30, textvariable=ymax)  # テキストボックスの生成
        y_max.grid(row=2, column=4, padx=10, pady=10)

        d_min = tkinter.IntVar()
        data_min = ttk.Entry(frame_data, width=30, textvariable=d_min, state="readonly")
        data_min.grid(row=1, column=2, padx=10, pady=10, columnspan=2)
        d_max = tkinter.IntVar()
        data_max = ttk.Entry(frame_data, width=30, textvariable=d_max, state="readonly")
        data_max.grid(row=2, column=2, padx=10, pady=10, columnspan=2)
        d_mean = tkinter.IntVar()
        data_mean = ttk.Entry(frame_data, width=30, textvariable=d_mean, state="readonly")
        data_mean.grid(row=3, column=2, padx=10, pady=10, columnspan=2)

        # チェックボックスの設定
        # val = tkinter.BooleanVar()
        # val.set(False)
        # CheckBox = tkinter.Checkbutton(frame_label, variable=val)
        # CheckBox.grid(row=1, column=1)

        # ラベルに関する諸々の設定
        GridLabel1 = ttk.Label(frame_plot_data, text="選択中 : ", anchor=tkinter.W)
        GridLabel1.grid(row=1, column=1)
        GridLabel1_2 = ttk.Label(frame_csv_list, text="作業フォルダ: ", anchor=tkinter.W)
        GridLabel1_2.grid(row=1, column=1)
        GridLabel1_3 = ttk.Label(frame_csv_list, text="選択中 : ", anchor=tkinter.W)
        GridLabel1_3.grid(row=2, column=1)
        # GridLabel2 = ttk.Label(root, text="CSV Path")
        # GridLabel2.grid(row=1, column=11)

        # GridLabel3 = ttk.Label(frame_label, text="Title設定")
        # GridLabel3.grid(row=0, column=0, rowspan=2)
        # GridLabel4 = ttk.Label(frame_label, text="Plotデータと同じにする")
        # GridLabel4.grid(row=1, column=2, sticky=tkinter.W)

        Label_xmin = ttk.Label(frame_lim, text="x最小値")
        Label_xmin.grid(row=1, column=1, sticky=tkinter.E)
        Label_xmax = ttk.Label(frame_lim, text="x最大値")
        Label_xmax.grid(row=2, column=1, sticky=tkinter.E)

        GridLabel5 = ttk.Label(frame_lim, text="y最小値")
        GridLabel5.grid(row=1, column=3, sticky=tkinter.E)
        GridLabel6 = ttk.Label(frame_lim, text="y最大値")
        GridLabel6.grid(row=2, column=3, sticky=tkinter.E)

        GridLabel7 = ttk.Label(frame_data, text="最小値")
        GridLabel7.grid(row=1, column=1, sticky=tkinter.E)
        GridLabel8 = ttk.Label(frame_data, text="最大値")
        GridLabel8.grid(row=2, column=1, sticky=tkinter.E)
        GridLabel9 = ttk.Label(frame_data, text="一周\n平均値")
        GridLabel9.grid(row=3, column=1, sticky=tkinter.E)

        # LIST BOXの設定
        csvlist = tkinter.StringVar(value=[])
        csv_list = tkinter.Listbox(frame_csv_list,
                                   listvariable=csvlist,
                                   height=10, width=60)
        csv_list.grid(row=3, column=1, columnspan=10, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
        csv_list.bind("<<ListboxSelect>>", get_csvlist_select_file)
        csv_list.columnconfigure(0, weight=1)
        csv_list.rowconfigure(0, weight=1)

        var1 = tkinter.StringVar(value=[])
        plot_data_list = tkinter.Listbox(frame_plot_data,
                                         listvariable=var1,
                                         height=11, width=60)
        plot_data_list.grid(row=2, column=1, columnspan=10, sticky=(tkinter.E, tkinter.W, tkinter.S, tkinter.N))
        plot_data_list.bind("<<ListboxSelect>>", get_csvlist_selected)
        # plot_data_list.bind("<<ListboxSelect>>", partial(DrawCanvas, Canvas, ax1, plot_data_list.curselection()))

        # ボタンに関する諸々の設定
        ReDrawButton = ttk.Button(frame_data, text="描画", width=15,
                                  command=partial(DrawCanvas, Canvas, Canvas2, ax1, ax2))  # ボタンの生成
        ReDrawButton.grid(row=2, column=5, columnspan=2, pady=10)

        button_header = ttk.Button(frame_plot_data, text="読み込み", command=set_header)
        button_header.grid(row=0, column=1, columnspan=10, sticky=(tkinter.W, tkinter.E, tkinter.S))
        # button_header = ttk.Button(frame_csv_list, text="読み込み", command=set_header)
        # button_header.grid(row=0, column=1, columnspan=5, sticky=(tkinter.W, tkinter.E, tkinter.S))

        button_refer_file = ttk.Button(frame_plot_data, text="ファイル選択", command=refer_file)
        button_refer_file.grid(row=1, column=10, sticky=tkinter.E)
        button_refer_dir = ttk.Button(frame_csv_list, text="フォルダ選択", command=refer_dir)
        button_refer_dir.grid(row=1, column=10, sticky=tkinter.E)
        # button_save = ttk.Button(root, text="保存", command=save)
        # button_save.grid(row=12, column=5, sticky=tkinter.E)

        # スクロールバーの設定
        scrollbar_v2 = ttk.Scrollbar(frame_csv_list, command=csv_list.yview)
        scrollbar_v2.grid(row=3, column=11, sticky=(tkinter.N, tkinter.S, tkinter.W))
        scrollbar_h2 = ttk.Scrollbar(frame_csv_list, command=csv_list.xview, orient='h')
        scrollbar_h2.grid(row=4, column=1, columnspan=10, sticky=(tkinter.E, tkinter.W, tkinter.N))
        csv_list['yscrollcommand'] = scrollbar_v2.set
        csv_list['xscrollcommand'] = scrollbar_h2.set

        scrollbar_v = ttk.Scrollbar(frame_plot_data, command=plot_data_list.yview)
        scrollbar_v.grid(row=2, column=11, sticky=(tkinter.N, tkinter.S, tkinter.W))
        scrollbar_h = ttk.Scrollbar(frame_plot_data, command=plot_data_list.xview, orient='h')
        scrollbar_h.grid(row=3, column=1, columnspan=10, sticky=(tkinter.E, tkinter.W, tkinter.N))
        plot_data_list['yscrollcommand'] = scrollbar_v.set
        plot_data_list['xscrollcommand'] = scrollbar_h.set

        # ***** Status Bar *****
        status_var = tkinter.StringVar()
        status_var.set("Choose .csv data file")
        status = ttk.Label(root, textvariable=status_var, relief=tkinter.SUNKEN, anchor=tkinter.W)
        # bd=border, relief to make it look like a status bar, want anchor to be left
        status.grid(row=20, column=0, columnspan=20, sticky=(tkinter.W, tkinter.E, tkinter.S))

        # DrawCanvas(Canvas, ax1, listbox.curselection())

        root.mainloop()  # 描画し続ける
    except:
        import traceback

        traceback.print_exc()
    finally:
        input(">>")  # エラー吐き出したときの表示待ち
