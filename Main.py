# Created by Umemoto at 2019/05/08
# -*-coding:utf-8-*-
"""
参考
    http://b4rracud4.hatenadiary.jp/entry/20181207/1544129263
    https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_sgskip.html
    https://pg-chain.com/python-tkinter-entry
"""
import tkinter.filedialog
from matplotlib import rcParams
from QBlade_processing import QBlade
from GUI import Application

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Sans', 'BIZ UDGothic', 'Yu Gothic', 'Meiryo', 'Noto Sans CJK JP',
                               'IPAexGothic', 'DejaVu Sans']


def main():
    root = tkinter.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except:
        import traceback

        traceback.print_exc()
    finally:

        input(">>")  # エラー吐き出したときの表示待ち
