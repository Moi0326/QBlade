# Created by Umemoto at 2020/07/03

import pandas as pd
import numpy as np


class QBlade:

    def __init__(self, save_figure, show_neg, only_mean, path_input, path_output):
        """
        :param save_figure: 1 → save, 0 → no save
        :param show_neg: 1 → 負の軸を表示する, 0 → 負の軸を表示しない
        :param only_mean: 1 → 平均値のみ表示, 0 → 平均値と生データを表示, -1 → 生データのみ表示
        :param path_input: plotするcsvの絶対パス
        :param path_output: output先の絶対パス
        """
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        self.path_input = path_input
        self.path_output = path_output
        self.savefig = save_figure
        self.only_mean = only_mean
        self.show_negative = show_neg
        self.csv = pd.read_csv(filepath_or_buffer=path_input,
                               sep=",",
                               index_col=None,
                               header=None,
                               skiprows=[0, 1, 2],
                               engine="python").iloc[:, :-1]

    def initialize(self):
        idx = pd.IndexSlice
        # CSV読み込み
        csv = pd.read_csv(filepath_or_buffer=self.path_input,
                          sep=",",
                          index_col=None,
                          header=None,
                          skiprows=[0, 1, 2],
                          engine="python").iloc[:, :-1]

        # ヘッダー読み込み
        headers = [p for p in pd.read_csv(filepath_or_buffer=self.path_input,
                                          sep=",",
                                          index_col=None,
                                          skiprows=[0],
                                          engine="python").columns][:-1]
        headers[1::2] = headers[::2]
        # print(csv, csv.columns)
        sub_columns = ['Degree', 'Momentary_Torque'] * (int(len(headers) / 2))

        column_arrays = [
            headers,
            sub_columns
        ]
        tuple_1 = list(zip(*column_arrays))

        index = pd.MultiIndex.from_tuples(tuple_1, names=['Title', 'Axis'])
        # print(index)
        csv.columns = index
        # print(csv.loc[:, idx[:,'Time[s]']])
        return csv

    def define_header(self):
        h = [p for p in pd.read_csv(filepath_or_buffer=self.path_input,
                                    sep=",",
                                    index_col=None,
                                    skiprows=[0],
                                    engine="python").columns]
        return h[0:-1:2]

    def mean_plot(self, deg, r):
        """
        :param deg:角度
        :param r: 値
        :return: 角度,平均値　のlist
        """
        """
        平均値計算
        """
        deg = deg.dropna(how='any')
        r = r.dropna(how='any')

        deg = deg.values.tolist()
        print(deg)
        # 変位角取得
        delta_deg = round(deg[1] - deg[0])
        # Revolution数取得
        loop_1 = int(360 / delta_deg)
        # print(loop_1)

        """
        新規Array作成
        """
        # csvデータ整形
        # print(type(r))

        value = [np.array(r.iloc[i::loop_1].values.tolist()[0:int(len(r) / loop_1)]) for i in range(loop_1)]
        # print(value)
        array1 = value[0]
        for i in range(loop_1 - 1):
            array1 = np.vstack([array1, value[i + 1]])

        # DataFrame作成
        df = pd.DataFrame(array1)
        # df.loc[loop_1] = df.iloc[0]

        degrees = pd.Series(deg[0:loop_1])
        df_output = pd.DataFrame(array1, index=degrees)
        # print(degrees)
        df_h = pd.DataFrame(index=degrees)
        df_mean = df.mean(axis='columns').tolist()
        df_median = df.median(axis='columns').tolist()
        print(df_mean)
        df_h['mean'] = df_mean
        df_h['median'] = df_median
        df_h.sort_index(inplace=True)
        if list(df_h.index)[0] == 0:
            addition = df_h.head(1)
            addition.rename(index=lambda s: 360, inplace=True)
            df_h = pd.concat([df_h, addition])
        else:
            addition = df_h.tail(1)
            addition.rename(index=lambda s: 0, inplace=True)
            df_h = pd.concat([addition, df_h])
        # zero.reset_index(inplace=True, drop=True)
        # df_h.sort_index(inplace=True)
        print(df,df_h)
        # deg = pd.DataFrame(deg.T)

        x = [degrees, df_mean, df_median]
        # print(x)
        print("mean: " + str(sum(df.mean(axis='columns')) / loop_1))
        d_mean = (sum(df.mean(axis='columns')) / loop_1)
        d_min = (min(df.mean(axis='columns')))
        d_max = (max(df.mean(axis='columns')))
        return df_h, d_mean, d_min, d_max, df_output
