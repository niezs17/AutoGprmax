from auto_gprmax import random_cavity
from auto_gprmax import generate_bscan

# 无缺损的道路模型
TEXT_INTACT_ROAD \
    = ("#domain: 2.00 2.00 0.0025\n"
       "#dx_dy_dz: 0.01 0.01 0.0025\n"
       "#time_window: 16e-9\n"
       "#waveform: ricker 1.0 400e6 my_ricker\n"
       "#hertzian_dipole: z 0.2 1.905 0 my_ricker\n"
       "#rx: 0.3 1.905 0\n"
       "#src_steps: 0.02 0.0 0\n"
       "#rx_steps: 0.02 0.0 0\n"
       "#material: 4 0.005 1 0 asphalt\n"
       "#material: 9 0.05 1 0 concrete\n"
       "#material: 12 0.1 1 0 soilbase\n"
       "#box: 0.00 0.00 0.00 2.00 1.60 0.0025 soilbase\n"
       "#box: 0.00 1.60 0.00 2.00 1.75 0.0025 concrete\n"
       "#box: 0.00 1.75 0.00 2.00 1.90 0.0025 asphalt\n"
       "#box: 0.00 1.90 0.00 2.00 2.00 0.0025 free_space\n"
       )

# 定义要生成的文件数量generate
generate_num = 1
# 路基空间范围(x1, x2, y1, y2, z1, z2) y2作为y方向的起始坐标
soil_base_space = {'x1': 0, 'y1': 0, 'z1': 0, 'x2': 2.0, 'y2': 1.6, 'z2': 0.0025}
# 加上缺损
TEXT_IN = TEXT_INTACT_ROAD + random_cavity(soil_base_space, 3, 0)

# 生成Bscan图像
for figure in range(1, generate_num + 1, 1):
    generate_bscan(
        text_in=TEXT_IN,
        generate=1,
        geometry=0,
        ascan_times=70,
        figure_number=figure,
        time_window=16e-9
    )
