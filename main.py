import os
# import random

# import matplotlib.patches as mpathes
# import matplotlib.pyplot as plt
# import numpy as np
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files
from tools.plot_Bscan import normalized_mpl_plot

# 初始化gprMax模拟的基础配置(不变量)
t1 = "#domain: 2.5 0.5 0.002\n"  # 模型尺寸 #domain: f1 f2 f3 (m)
t2 = "#dx_dy_dz: 0.005 0.005 0.002\n"  # 空间步长 #dx_dy_dz: f1 f2 f3
t3 = "#time_window: 15e-9\n"  # 总模拟时间
t4 = "#waveform: ricker 1.0 900e6 my_ricker\n"  # 源波形
t5 = "#hertzian_dipole: z 0.0875 0.4525 0 my_ricker\n"  # 赫兹偶极子:模拟理想化的天线源
t6 = "#rx: 0.1125 0.4525 0\n"  # 接收点 (x, y, z)
t7 = "#src_steps: 0.02 0.0 0\n"  # 源点移动步长
t8 = "#rx_steps: 0.02 0.0 0\n"  # 接收点移动步长
t17 = "#geometry_view: 0 0 0 2.5 0.5 0.0025 0.005 0.005 0.0025 model n\n"  # 几何视图设置

# 初始化gprMax模拟的基础配置(变量)
t9 = "#material: 6.4 0.01 1 0 concrete\n"  #
t10 = "#box: 0 0 0 2.5 0.45 0.0025 concrete\n"  #
t11 = "#box: 0 0.45 0 2.5 0.5 0.0025 free_space\n"  #
t12 = "#cylinder: 0.65 0.10 0.00 0.65 0.10 0.002 0.0119 pec\n"  #
t13 = "#cylinder: 1.01 0.15 0.00 1.01 0.15 0.002 0.0070 pec\n"  #
t14 = "#cylinder: 0.75 0.20 0.00 0.75 0.20 0.002 0.0070 pec\n"  #
t15 = "#cylinder: 1.44 0.31 0.00 1.44 0.31 0.002 0.0119 pec\n"  #
t16 = "#cylinder: 1.43 0.11 0.00 1.43 0.11 0.002 0.0119 pec\n"  #

N = 1  # 定义要生成的文件数量generate
time_window = 15e-9
Ascan_times = 60
GENERATE = 1
GEOMETRY = 1
text_in_NGEO = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11 + t12 + t13 + t14 + t15 + t16
text_in_GEO = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11 + t12 + t13 + t14 + t15 + t16 + t17


for figure in range(1, N + 1, 1):
    if GENERATE:
        # 生成输入文件
        in_file_name = r"./text_in/figure" + str(figure) + "/Ascan" + '.in'
        # 设置gprMax模拟的输入文件路径
        fil_in = os.path.join(in_file_name)
        # A-scan 60 times
        if GEOMETRY:
            # 从头写入不带几何设置命令的in文件, 然后执行Ascan_times-1次，直到最后一次Ascan停止
            f = open(in_file_name, 'w')
            f.writelines(text_in_NGEO)
            f.close()
            api(fil_in, n=Ascan_times-1, geometry_only=False)
            f = open(in_file_name, 'w')
            f.writelines(text_in_GEO)
            f.close()
            api(fil_in, n=1, geometry_only=False)
        else:
            f = open(in_file_name, 'w')
            f.writelines(text_in_NGEO)
            f.close()
            api(fil_in, n=Ascan_times, geometry_only=False)
        # 用模拟出的A-Scan条数合并生成B-Scan图像(注意，这里的文件路径只能从AScan停止， 不能带数字，不能带后缀)
        merge_files(r"./text_in/figure" + str(figure) + "/Ascan", removefiles=True)
        print("generating succeed")
    else:
        print("skipping the generate stage")

        # 提取输出数据
    out_file_name = r"./text_in/figure" + str(figure) + "/Ascan_merged.out"  # 合并后文件名
    outputdata, dt = get_output_data(out_file_name, 1, 'Ez')
    plt = normalized_mpl_plot(out_file_name, outputdata, dt * 1e9, 1, 'Ez', Ascan_times, time_window)
    plt.savefig(r"./scan_out" + '/Bscan' + str(figure) + '.jpg')

    print("saving succeed!")
    print("looking *.out/*.in files in \'figure_x\'")
    print("looking *.jpg files in \'scan_out\'")
