import datetime
import os
import numpy as np
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files
from tools.plot_Bscan import normalized_mpl_plot
import random
from datetime import date


# import cv2


def check_distance(center1, center2, radium, limit):
    # print(np.linalg.norm(np.array(center1) - np.array(center2)) < (np.sum(radium)+1.))
    # print(np.linalg.norm(np.array(center1) - np.array(center2)) )
    # print(f"center1: {center1}, center2: {center2}")
    distance = np.linalg.norm(np.array(center1) - np.array(center2))
    # print(distance)
    return (np.sum(radium) + limit[1]) >= distance >= (np.sum(radium) + limit[0])


def create_cavity_instruction(x, y, z1, z2, r, cavity_type):
    """
    :param x:   中心点横坐标
    :param y:   中心点纵坐标
    :param z1:  底面高
    :param z2:  顶面高
    :param r:   半径
    :param cavity_type: 空洞类型
    :return:    inst:  加入到.in文件的指令字符串
                describe_input_file(random_shape, x, y, r, cavity_type, inst):  描述空洞类型的字符串
    """
    # 待选取的形状
    shape = ['box', 'cylinder']
    random_shape = random.choice(shape)
    if random_shape == 'box':
        inst = f"#{random_shape}: {round(x - r, 3)} {round(y - r, 3)} {z1} " \
               f"{round(x + r, 3)} {round(y + r, 3)} {z2} {cavity_type}\n"
    else:
        inst = f"#{random_shape}: {round(x, 3)} {round(y, 3)} {z1} " \
               f"{round(x, 3)} {round(y, 3)} {z2} {round(r, 3)} {cavity_type}\n"

    return [inst, describe_input_file(random_shape, x, y, r, cavity_type, inst)]


def describe_input_file(shape, x, y, r, cavity_type, inst):
    """
    # 生成一个文档，简单描述该输入文件的信息，在生成空洞组合之后使用
    # 注意，此处的路基坐标范围'1.60'是写死的，修改路基坐标的时候要改这个
    :return: text
    """
    text = ["**********************************************************************\n"]
    if shape == 'box':
        text.append("shape: box\n")
        text.append(f"cavity_type: {cavity_type}\n")
        text.append(f"origin position: ({round(x, 3)}, {round(y, 3)})   (m)\n")
        text.append(f"depth: {round(1.60 - y, 3)}   (m)\n")
        text.append(f"width: {round(2 * r, 3)}  (m)\n")
        text.append(f"height: {round(2 * r, 3)} (m)\n\n")
        text.append(f"{inst}")
    elif shape == 'cylinder':
        text.append("shape: cylinder\n")
        text.append(f"cavity_type: {cavity_type}\n")
        text.append(f"origin position: ({round(x, 3)}, {round(y, 3)})   (m)\n")
        text.append(f"depth: {round(1.60 - y, 3)}  (m)\n")
        text.append(f"radium: {round(2 * r, 3)}    (m)\n\n")
        text.append(f"{inst}")
    else:
        text.append("your shape is wrong!\n")
    text.append("**********************************************************************\n\n")
    return ''.join(text)

# def plot_input_file(shape, x, y, r, cavity_type):


def generate_bscan(text_in, regenerate, geometry, ascan_times, figure_number, time_window, info, describe):
    """
    :param text_in:         不带几何建模指令的输入代码(str)
    :param regenerate:      是否重建Bscan
    :param geometry:        是否生成几何建模
    :param ascan_times:     Ascan扫描次数
    :param figure_number:   生成图像的编号
    :param time_window:     仿真时间
    :param info:            生成图像基本信息 格式: air_x_water_y(x表示充气空洞数量，y表示充水空洞数量)
    :param describe:        用文字描述图像基本内容 存在:f"./B-scan/{date.today()}/basic_{info}_{figure_number}/describe.txt"
    :return None
    """
    figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
    text_geo = "#geometry_view: 0 0 0 4.00 1.40 0.0025 0.0025 0.0025 0.0025 basic n \n"

    if regenerate:
        if geometry:
            while os.path.exists(figure_path):
                figure_number += 1
                figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
            figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
            os.makedirs(figure_path)
        else:
            while os.path.exists(figure_path):
                figure_number += 1
                figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
            figure_number -= 1
            figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
    else:
        pass

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
                api(in_file_name, n=1, geometry_only=True, gpu={0})

        else:
            # 删除最后一行，并在原有in文件基础上扫描n次
            with open(in_file_name, 'r') as f:
                lines = f.readlines()[:-1]
                f.close()
            with open(in_file_name, 'w') as f:
                f.writelines(lines)
                f.close()
            api(in_file_name, n=ascan_times, geometry_only=False, gpu={0})
            merge_files(f"{figure_path}/Ascan", removefiles=True)
        print("Process completed.")
    if (regenerate and not geometry) or (not regenerate):
        out_file_name = f"{figure_path}/Ascan_merged.out"
        outputdata, dt = get_output_data(out_file_name, 1, 'Ez')
        plt = normalized_mpl_plot(out_file_name, outputdata, dt * 1e9, 1, 'Ex', ascan_times, time_window, ymax=580)
        # plt = mpl_plot(out_file_name, outputdata, dt * 1e9, 1, 'Ex')
        plt.savefig(f"{figure_path}/bscan_{info}_{figure_number}.jpg")
        print(f"looking *.out/*.in files in {figure_path}")
    describe_file_name = f"{figure_path}/des.txt"
    with open(describe_file_name, 'w') as f:
        f.write(describe)
        f.close()


def random_cavity(soil_base_space, air_cavity_num_all, water_cavity_num_all, distance_limit=None):
    """
    :param distance_limit:
    :param soil_base_space:     路基空间范围
    :param air_cavity_num_all:      充气空洞数量
    :param water_cavity_num_all:    充水空洞数量
    :return: 完整in文件指令
    """
    if distance_limit is None:
        distance_limit = [0.6, 1.2]
    create_result = [[], []]
    # 对路基空间范围修正，防止生成空洞与PML相交
    soil_base_space['x1'] += 0.025
    soil_base_space['y1'] += 0.025
    soil_base_space['x2'] -= 0.025
    soil_base_space['y2'] -= 0.025
    # 如果生成数量过多，则默认只生成一个充气型空洞，位于路基正中间
    print(f"allowed distance range between any two cavities --- min: {distance_limit[0]}, max: {distance_limit[1]}")
    if air_cavity_num_all + water_cavity_num_all > 2:
        x = (soil_base_space['x1'] + soil_base_space['x2']) / 2.0
        y = (soil_base_space['y1'] + soil_base_space['y2']) / 2.0
        cavity_radium = 0.2
        cavity_type = 'free_space'
        create_result[0].append(create_cavity_instruction(x, y, soil_base_space['z1'], soil_base_space['z2'],
                                                          cavity_radium, cavity_type)[0])
        create_result[1].append(create_cavity_instruction(x, y, soil_base_space['z1'], soil_base_space['z2'],
                                                          cavity_radium, cavity_type)[1])
        print("Too many cavities! more than 2\n "
              "Automatically generate an cylinder air cavity with the center of soil base, r = 0.2")
        return create_result
    else:
        cavity_radium = []
        cavity_centers = []
        cavity_num = 0
        while cavity_num < (air_cavity_num_all + water_cavity_num_all):
            cavity_radium.append(random.uniform(0.02, 0.05))  # 随机生成空洞半径
            # print(cavity_radium[-1])
            cavity_region = {'x': [soil_base_space['x1'] + np.max(cavity_radium),
                                   soil_base_space['x2'] - np.max(cavity_radium)],
                             'y': [soil_base_space['y1'] + np.max(cavity_radium),
                                   soil_base_space['y2'] - np.max(cavity_radium)]}
            x = random.uniform(cavity_region['x'][0], cavity_region['x'][1])
            y = random.uniform(cavity_region['y'][0], cavity_region['y'][1])
            cavity_centers.append((x, y))
            # Check distance from previous cavities
            # Check distance from the last cavity
            if all(check_distance((x, y), center, cavity_radium[-1:], distance_limit) for center in cavity_centers[:-1]):
                # check_distance((x, y), (1, 2), cavity_radium[-2:])
                cavity_type = 'free_space' if cavity_num < air_cavity_num_all else 'water'
                create_result[0].append(create_cavity_instruction(x, y, soil_base_space['z1'], soil_base_space['z2'],
                                                                  cavity_radium[-1], cavity_type)[0])
                create_result[1].append(create_cavity_instruction(x, y, soil_base_space['z1'], soil_base_space['z2'],
                                                                  cavity_radium[-1], cavity_type)[1])
                cavity_num += 1
            else:
                # Adjusting cavity radius or position if necessary
                # Or handle overlapping cavities
                print("else")
                cavity_centers.pop()
                pass
        create_result[0] = ''.join(create_result[0])
        create_result[1] = ''.join(create_result[1])
        return create_result


def generate(TEXT_INTACT_ROAD, generate_num, ascan_times, air_cavity_num,
             water_cavity_num, soil_base_space, time_window, generate_mode):
    for figure_number in range(1, generate_num + 1, 1):
        # os.system('cls' if os.name == 'nt' else 'clear')
        TEXT_IN = TEXT_INTACT_ROAD + random_cavity(soil_base_space, air_cavity_num, water_cavity_num)[0]
        DESCRIBE = random_cavity(soil_base_space, air_cavity_num, water_cavity_num)[1]
        # TEXT_IN = TEXT_INTACT_ROAD
        # 生成Bscan图像
        if generate_mode == 'geo':
            generate_bscan(
                TEXT_IN,
                regenerate=1,
                geometry=1,
                ascan_times=ascan_times,
                figure_number=figure_number,
                time_window=time_window,
                info=f"air_{air_cavity_num}_water_{water_cavity_num}",
                describe=DESCRIBE
            )
        elif generate_mode == 'scan':
            generate_bscan(
                TEXT_IN,
                regenerate=1,
                geometry=1,
                ascan_times=ascan_times,
                figure_number=figure_number,
                time_window=time_window,
                info=f"air_{air_cavity_num}_water_{water_cavity_num}",
                describe=DESCRIBE
            )
            generate_bscan(
                TEXT_IN,
                regenerate=1,
                geometry=0,
                ascan_times=ascan_times,
                figure_number=figure_number,
                time_window=time_window,
                info=f"air_{air_cavity_num}_water_{water_cavity_num}",
                describe=DESCRIBE
            )
        elif generate_mode == 'plot':
            generate_bscan(
                TEXT_IN,
                regenerate=0,
                geometry=0,
                ascan_times=ascan_times,
                figure_number=figure_number,
                time_window=time_window,
                info=f"air_{air_cavity_num}_water_{water_cavity_num}",
                describe=DESCRIBE
            )
        else:
            print("generate_mode error")


if __name__ == '__main__':
    for _ in range(0, 3000):
        print(''.join(random_cavity({'x1': 0.4, 'y1': 1.0, 'z1': 0, 'x2': 3.6, 'y2': 1.4, 'z2': 0.0025}, 1, 1)))
        print()
    print('done')
