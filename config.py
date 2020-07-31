# Created by Umemoto at 2020/07/31
import os
# import sys
import configparser

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

CONFIG_FILE_PATH = './config.ini'


class ConfigInit:
    def __init__(self):
        config_ini = configparser.ConfigParser()
        if not os.path.exists(CONFIG_FILE_PATH):
            exit(-1)
        config_ini.read(CONFIG_FILE_PATH, encoding='utf-8')
        try:
            self.w_dir = str(config_ini['CSVs']['Working Directory'])

            self.x_min_c = float(config_ini['GraphSetting']['x min'])
            self.x_max_c = float(config_ini['GraphSetting']['x max'])
            self.y_min_c = float(config_ini['GraphSetting']['y min'])
            self.y_max_c = float(config_ini['GraphSetting']['y max'])
            self.p_cutout_c = float(config_ini['GraphSetting']['Plot cut-out'])
            self.grid_x_c = float(config_ini['GraphSetting']['Grid x'])
            self.grid_y_c = float(config_ini['GraphSetting']['Grid y'])

        except Exception as e:
            print("error")


def main():
    Conf = ConfigInit()
    print(Conf.x_min_c)


if __name__ == '__main__':
    main()
