import auto_gprmax

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

generate_num = 1  # 定义要生成的文件数量generate
TEXT_NGEO = t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11 + t12 + t13 + t14 + t15 + t16
TEXT_GEO = TEXT_NGEO + t17

for figure in range(1, generate_num + 1, 1):
    auto_gprmax.generate_bscan(
        text_in_ngeo=TEXT_NGEO,
        text_in_geo=TEXT_GEO,
        generate=1,
        geometry=0,
        ascan_times=60,
        figure_number=figure,
        time_window=15e-9
    )
