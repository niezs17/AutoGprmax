from auto_gprmax import generate
from sys import argv
time_window = 36e-9

# 目前确定生成范围不能小于y=0.8
if __name__ == '__main__':
    # 无缺损的道路模型
    TEXT_BASE \
        = ("#domain: 2.00 2.00 0.0025\n"
           "#dx_dy_dz: 0.0025 0.0025 0.0025\n"
           f"#time_window: {time_window}\n"
           "#waveform: ricker 1.0 600e6 my_ricker\n"
           "#hertzian_dipole: z 0.0875 1.905 0 my_ricker\n"
           "#rx: 0.1125 1.905 0\n"
           "#src_steps: 0.016 0.0 0\n"
           "#rx_steps: 0.016 0.0 0\n"  
           "#material: 4 0.005 1 0 asphalt\n"   
           "#material: 9 0.05 1 0 concrete\n"
           "#material: 12 0.1 1 0 soilbase\n"
           "#material: 81 0.03 1 0 water\n"
           "#box: 0.00 0.00 0.00 2.00 1.90 0.0025 soilbase\n"
           "#box: 0.00 1.60 0.00 2.00 1.75 0.0025 concrete\n"
           "#box: 0.00 1.75 0.00 2.00 1.90 0.0025 asphalt\n"
           "#box: 0.00 1.90 0.00 2.00 2.00 0.0025 free_space\n"
           )
    # 检查是否有足够的参数
    # argv列表的第一个元素（sys.argv[0]）是脚本名称，所以参数索引从1开始
    if len(argv) == 3:
        air_cavity_num = argv[1]  # 获取第一个参数
        water_cavity_num = argv[2]  # 获取第二个参数
        print(f"air_cavity_num: {air_cavity_num}, water_cavity_num: {water_cavity_num}")
        generate(TEXT_INTACT_ROAD=TEXT_BASE, generate_num=1, ascan_times=120,
                 air_cavity_num=int(air_cavity_num), water_cavity_num=int(water_cavity_num),
                 time_window=time_window,
                 soil_base_space={'x1': 0.4, 'y1': 0.9, 'z1': 0, 'x2': 1.6, 'y2': 1.3, 'z2': 0.0025},
                 generate_mode='scan')
    else:
        print("you need 2 parameters: air_cavity_num, water_cavity_num")
































