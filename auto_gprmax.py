import os
import numpy as np
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files
from tools.plot_Bscan import normalized_mpl_plot
import random


def check_distance(center1, center2, radium):
    return np.linalg.norm(np.array(center1) - np.array(center2)) < np.sum(radium)


def generate_cavity_center(region):
    x_center = random.uniform(region['x'][0], region['x'][1])
    y_center = random.uniform(region['y'][0], region['y'][1])
    return x_center, y_center


def create_cavity_instruction(x, y, z1, z2, radium, cavity_type):
    return f"#cylinder: {round(x,2)} {round(y,2)} {z1} " \
           f"{round(x,2)} {round(y,2)} {z2} {round(radium,2)} {cavity_type}\n"


def generate_bscan(text_in, generate, geometry, ascan_times, figure_number, time_window, info):
    """
    :param text_in:    不带几何建模指令的输入代码(str)
    :param generate:        是否重建Bscan
    :param geometry:        是否生成几何建模
                GEN = 1, GEO = 0      重新合成BScan, 生成图像, 不生成几何建模
                GEN = 0, GEO = 0      不合成Bscan, 生成图像, 不生成几何建模
                GEN = 0, GEO = 1      无事发生
                GEN = 1, GEO = 1      不生成新的Bscan数据和图像, 只生成几何建模
    :param ascan_times:      Ascan扫描次数
    :param figure_number:   生成图像的编号
    :param time_window:     仿真时间
    :param info:            生成图像基本信息 格式: air_x_water_y(x表示充气空洞数量，y表示充水空洞数量)
    :return None
    """
    if generate:
        # 生成输入文件
        in_file_name = f"./text_in/figure{str(figure_number)}_{info}/Ascan.in"
        # 设置gprMax模拟的输入文件路径
        fil_in = os.path.join(in_file_name)
        if not os.path.exists(f"./text_in/figure{str(figure_number)}_{info}"):
            os.makedirs(f"./text_in/figure{str(figure_number)}_{info}")
        f = open(in_file_name, 'w')
        if geometry:
            # 从头写入不带几何设置命令的in文件, 只执行1次，因为目的仅为得到建模图像，此时不需要merge
            f.writelines(text_in)
            f.writelines("#geometry_view: 0 0 0 2.00 2.00 0.01 0.01 0.01 0.01 basic n \n")
            f.close()
            api(fil_in, n=1, geometry_only=False)
        else:
            f.writelines(text_in)
            f.close()
            api(fil_in, n=ascan_times, geometry_only=False)  # A-scan 60 times
            # 用模拟出的A-Scan条数合并生成B-Scan图像(注意，这里的文件路径只能从AScan停止， 不能带数字，不能带后缀)
            merge_files(f"./text_in/figure{str(figure_number)}_{info}/Ascan", removefiles=True)
        print("generating succeed")
    else:
        print("skipping the generate stage")

    if geometry:
        if generate:
            print("saving succeed")
            print("looking *.out/*.in files in \'figure_x\'")
            print("looking *.vti/*.vtp files in \'figure_x\'")
        else:
            print("nothing happened")
    else:
        # 提取输出数据
        out_file_name = f"./text_in/figure{str(figure_number)}_{info}/Ascan_merged.out"  # 合并后文件名
        outputdata, dt = get_output_data(out_file_name, 1, 'Ez')
        plt = normalized_mpl_plot(out_file_name, outputdata, dt * 1e9, 1, 'Ex', ascan_times, time_window)
        plt.savefig(f"./scan_out/Bscan{str(figure_number)}_{info}.jpg")
        print(f"figure_{str(figure_number)}_{info} saving succeed")
        print("looking *.out/*.in files in \'figure_x\'")
        print("looking *.jpg files in \'scan_out\'")


def random_cavity(soil_base_space, air_cavity_num_all, water_cavity_num_all):
    """
    :param soil_base_space:     路基空间范围
    :param air_cavity_num_all:      充气空洞数量
    :param water_cavity_num_all:    充水空洞数量
    :return: 完整in文件指令
    """
    new_inst = []
    if air_cavity_num_all + water_cavity_num_all > 3:
        cavity_x = (soil_base_space['x1'] + soil_base_space['x2']) / 2.0
        cavity_y = (soil_base_space['y1'] + soil_base_space['y2']) / 2.0
        cavity_radium = 0.2
        cavity_type = 'free_space'
        new_inst.append(create_cavity_instruction(cavity_x, cavity_y, soil_base_space['z1'], soil_base_space['z2'],
                                                  cavity_radium, cavity_type))
        print("Too many cavities!\n "
              "Automatically generate an cylinder air cavity with the center of soil base, r = 0.2")
        return ''.join(new_inst)
    # 随机生成空洞大小，先处理充气空洞
    else:
        cavity_radium = []
        cavity_centers = []
        cavity_num = 0
        while cavity_num < (air_cavity_num_all + water_cavity_num_all):
            cavity_radium.append(random.uniform(0.02, 0.20))        # 随机生成空洞半径
            # print(cavity_radium[-1])
            cavity_region = {'x': [soil_base_space['x1'] + np.max(cavity_radium),
                                   soil_base_space['x2'] - np.max(cavity_radium)],
                             'y': [soil_base_space['y1'] + np.max(cavity_radium),
                                   soil_base_space['y2'] - np.max(cavity_radium)]}
            x, y = generate_cavity_center(cavity_region)
            cavity_centers.append((x, y))
            # Check distance from previous cavities
            if all(not check_distance((x, y), center, cavity_radium[-2:]) for center in cavity_centers[:-1]):
                cavity_type = 'free_space' if cavity_num < air_cavity_num_all else 'water'
                new_inst.append(create_cavity_instruction(x, y, soil_base_space['z1'], soil_base_space['z2'],
                                                          cavity_radium[-1], cavity_type))
                cavity_num += 1
            else:
                # Adjusting cavity radius or position if necessary
                # Or handle overlapping cavities
                pass
        return ''.join(new_inst)


if __name__ == '__main__':
    for _ in range(0,10):
        print(random_cavity({'x1': 0, 'y1': 0, 'z1': 0, 'x2': 2.0, 'y2': 1.6, 'z2': 0.0025}, 3, 0))
        print()


