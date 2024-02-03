import os
import numpy as np
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files
from tools.plot_Bscan import normalized_mpl_plot
import random


# import cv2


def check_distance(center1, center2, radium):
    return np.linalg.norm(np.array(center1) - np.array(center2)) < np.sum(radium)


def create_cavity_instruction(x, y, z1, z2, r, cavity_type):
    # 待选取的形状
    shape = ['box', 'cylinder']
    random_shape = random.choice(shape)
    if random_shape == 'box':
        return f"#{random_shape}: {round(x - r, 2)} {round(y - r, 2)} {z1} " \
               f"{round(x + r, 2)} {round(y + r, 2)} {z2} {cavity_type}\n"
    else:
        return f"#{random_shape}: {round(x, 2)} {round(y, 2)} {z1} " \
               f"{round(x, 2)} {round(y, 2)} {z2} {round(r, 2)} {cavity_type}\n"


def generate_bscan(text_in, regenerate, geometry, ascan_times, figure_number, time_window, info):
    """
    :param text_in:         不带几何建模指令的输入代码(str)
    :param regenerate:      是否重建Bscan
    :param geometry:        是否生成几何建模
    :param ascan_times:     Ascan扫描次数
    :param figure_number:   生成图像的编号
    :param time_window:     仿真时间
    :param info:            生成图像基本信息 格式: air_x_water_y(x表示充气空洞数量，y表示充水空洞数量)
    :return None
    """
    figure_path = f"./text_in/basic_{info}_{figure_number}"
    text_geo = "#geometry_view: 0 0 0 2.00 2.00 0.0025 0.0025 0.0025 0.0025 basic n \n"

    while os.path.exists(figure_path):
        figure_number += 1
        figure_path = f"./text_in/basic_{info}_{figure_number}"

    if (regenerate and not geometry) or not regenerate:
        figure_number -= 1
        figure_path = f"./text_in/basic_{info}_{figure_number}"
    else:
        figure_path = f"./text_in/basic_{info}_{figure_number}"
        os.makedirs(figure_path)
    in_file_name = f"{figure_path}/Ascan.in"

    # 处理生成逻辑
    if regenerate:
        if geometry:
            # 创建目录  在存文件之前，检查先前是否已经生成过同名文件，若有，则存在该文件编号后面
            with open(in_file_name, 'w') as f:
                # 处理几何建模 在原有文本基础上加一行
                f.write(text_in)
                f.write(text_geo)
                f.close()
                api(in_file_name, n=1, geometry_only=True)
        else:
            # 删除最后一行，并在原有in文件基础上扫描n次
            with open(in_file_name, 'r') as f:
                lines = f.readlines()[:-1]
                f.close()
            with open(in_file_name, 'w') as f:
                f.writelines(lines)
                f.close()
            api(in_file_name, n=ascan_times, geometry_only=False)
            merge_files(f"{figure_path}/Ascan", removefiles=True)
        print("Process completed.")
    if (regenerate and not geometry) or (not regenerate):
        out_file_name = f"{figure_path}/Ascan_merged.out"
        outputdata, dt = get_output_data(out_file_name, 1, 'Ez')
        plt = normalized_mpl_plot(out_file_name, outputdata, dt * 1e9, 1, 'Ex', ascan_times, time_window)
        plt.savefig(f"{figure_path}/bscan_{info}_{figure_number}.jpg")
        print(f"{info}_{figure_number} saving succeeded.")
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
    # 对路基空间范围修正，防止生成空洞与PML相交
    soil_base_space['x1'] += 0.1
    soil_base_space['y1'] += 0.1
    soil_base_space['x2'] -= 0.1
    soil_base_space['y2'] -= 0.1
    # 如果生成数量过多，则默认只生成一个充气型空洞，位于路基正中间
    if air_cavity_num_all + water_cavity_num_all > 5:
        cavity_x = (soil_base_space['x1'] + soil_base_space['x2']) / 2.0
        cavity_y = (soil_base_space['y1'] + soil_base_space['y2']) / 2.0
        cavity_radium = 0.2
        cavity_type = 'free_space'
        new_inst.append(create_cavity_instruction(cavity_x, cavity_y, soil_base_space['z1'], soil_base_space['z2'],
                                                  cavity_radium, cavity_type))
        print("Too many cavities!\n "
              "Automatically generate an cylinder air cavity with the center of soil base, r = 0.2")
        return ''.join(new_inst)
    else:
        cavity_radium = []
        cavity_centers = []
        cavity_num = 0
        while cavity_num < (air_cavity_num_all + water_cavity_num_all):
            cavity_radium.append(random.uniform(0.05, 0.20))  # 随机生成空洞半径
            # print(cavity_radium[-1])
            cavity_region = {'x': [soil_base_space['x1'] + np.max(cavity_radium),
                                   soil_base_space['x2'] - np.max(cavity_radium)],
                             'y': [soil_base_space['y1'] + np.max(cavity_radium),
                                   soil_base_space['y2'] - np.max(cavity_radium)]}
            x = random.uniform(cavity_region['x'][0], cavity_region['x'][1])
            y = random.uniform(cavity_region['y'][0], cavity_region['y'][1])
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


def generate(TEXT_INTACT_ROAD, generate_num, air_cavity_num,
             water_cavity_num, soil_base_space, time_window, generate_mode):
    for _ in range(1, generate_num + 1, 1):
        TEXT_IN = TEXT_INTACT_ROAD + random_cavity(soil_base_space, air_cavity_num, water_cavity_num)
        # TEXT_IN = TEXT_INTACT_ROAD
        # 生成Bscan图像
        if generate_mode == 'geo':
            generate_bscan(
                TEXT_IN,
                regenerate=1,
                geometry=1,
                ascan_times=10,
                figure_number=_,
                time_window=time_window,
                info=f"air_{air_cavity_num}_water_{water_cavity_num}"
            )
        elif generate_mode == 'all':
            generate_bscan(
                TEXT_IN,
                regenerate=1,
                geometry=1,
                ascan_times=10,
                figure_number=_,
                time_window=time_window,
                info=f"air_{air_cavity_num}_water_{water_cavity_num}"
            )
            generate_bscan(
                TEXT_IN,
                regenerate=1,
                geometry=0,
                ascan_times=10,
                figure_number=_,
                time_window=time_window,
                info=f"air_{air_cavity_num}_water_{water_cavity_num}"
            )
        elif generate_mode == 'plot':
            generate_bscan(
                TEXT_IN,
                regenerate=0,
                geometry=0,
                ascan_times=10,
                figure_number=_,
                time_window=time_window,
                info=f"air_{air_cavity_num}_water_{water_cavity_num}"
            )
        else:
            print("generate_mode error")


if __name__ == '__main__':
    for _ in range(0, 10):
        print(random_cavity({'x1': 0, 'y1': 0.6, 'z1': 0, 'x2': 2.0, 'y2': 1.6, 'z2': 0.0025}, 2, 1))
        print()
