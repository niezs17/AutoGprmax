from auto_gprmax import generate
time_window = 36e-9

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


# 目前确定生成范围不能小于y=0.8
if __name__ == '__main__':
    generate(TEXT_INTACT_ROAD=TEXT_BASE, generate_num=2, ascan_times=120,
             air_cavity_num=2, water_cavity_num=1,
             time_window=time_window,
             soil_base_space={'x1': 0.4, 'y1': 0.9, 'z1': 0, 'x2': 1.6, 'y2': 1.3, 'z2': 0.0025},
             generate_mode='scan')

