import os
import random

import matplotlib.patches as mpathes
import matplotlib.pyplot as plt
import numpy as np
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files
from tools.plot_Bscan import mpl_plot

t1 = ['#title: text\n', '#domain: 0.240 0.210 0.002\n', '#dx_dy_dz: 0.002 0.002 0.002\n', '#time_window: 3e-9\n', '\n']
t2 = ['#material: 6 0 1 0 half_space\n']
t3 = ['#waveform: ricker 1 1.5e9 my_ricker\n', '#hertzian_dipole: z 0.040 0.170 0 my_ricker\n', '\n']
t4 = ['#rx: 0.080 0.170 0\n', '#src_steps: 0.002 0 0\n', '#rx_steps: 0.002 0 0\n', '\n']
t5 = ['#box: 0 0 0 0.240 0.170 0.002 half_space\n', '\n']

N = 3  # 需生成N个文件

for i in range(1, N, 1):
    a = (random.randint(5, 115)) * 0.002
    b = (random.randint(5, 80)) * 0.002

    t6 = ['#cylinder: ', str(a), ' ', str(b), ' ', '0 ', str(a), ' ', str(b), ' ', '0.002 0.010 pec\n']

    f = open(r"./model_in/" + str(i) + '.txt', 'w')
    f.writelines(t1)
    f.writelines(t2)
    f.writelines(t3)
    f.writelines(t4)
    f.writelines(t5)
    f.writelines(t6)
    f.close()

    fig, ax = plt.subplots()
    plt.xlim(0, 0.240)
    plt.ylim(0, 0.210)
    xy1 = np.array([0, 0])
    xy2 = np.array([a, b])
    rect = mpathes.Rectangle(xy1, 0.240, 0.170, color='y')
    ax.add_patch(rect)
    circle = mpathes.Circle(xy2, radius=0.010, color='b')
    ax.add_patch(circle)
    plt.axis('equal')
    plt.savefig(r"./model_in/fig_in/" + str(i) + 'model_in.jpg')
    plt.close()

    dmax = r"./model_in"
    fil_in = os.path.join(dmax, str(i) + '.txt')

    # 扫描倒数需要自己定义
    api(fil_in, n=60, geometry_only=False)

    fi = fil_in[0:-4]
    merge_files(fi, removefiles=True)
    fi_b = fi + '_merged.out'
    rxnumber = 1
    rxcomponent = 'Ez'
    outputdata, dt = get_output_data(fi_b, rxnumber, rxcomponent)

    plt = mpl_plot(fi_b, outputdata, dt * 1e9, rxnumber, rxcomponent)
    plt.ylabel('Time [ns]')
    plt.savefig(r"./model_in/fig_out/" + str(i) + 'model_out.jpg')
