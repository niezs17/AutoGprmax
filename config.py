# Currently, the generation range cannot be less than y=0.8
AIR_CAVITY_NUM = 1
WATER_CAVITY_NUM = 1
RANDOM_PARA = {'x1': 0.4, 'y1': 0.35, 'z1': 0, 'x2': 3.6, 'y2': 0.7, 'z2': 0.0025, 'r_min': 0.025, 'r_max': 0.05}
TIME_WINDOW = 32e-9
DX = 0.0025
DY = 0.0025
DZ = 0.0025

GENGERATE_MODE = 'scan'
ASCAN_TIMES = 10
# Road model without defects
TEXT_INTACT_ROAD = ("#domain: 4.00 1.40 0.0025\n"
                f"#dx_dy_dz: {DX} {DY} {DZ}\n"
                f"#time_window: {TIME_WINDOW}\n"
                "#waveform: ricker 1.0 600e6 my_ricker\n"
                "#hertzian_dipole: z 0.0875 1.305 0 my_ricker\n"
                "#rx: 0.1125 1.305 0\n"
                "#src_steps: 0.031 0.0 0\n"
                "#rx_steps: 0.031 0.0 0\n"  
                "#material: 4 0.005 1 0 asphalt\n"   
                "#material: 9 0.05 1 0 concrete\n"
                "#material: 12 0.1 1 0 soilbase\n"
                "#material: 81 0.03 1 0 water\n"
                "#box: 0.00 0.00 0.00 4.00 1.00 0.0025 soilbase\n"
                "#box: 0.00 1.00 0.00 4.00 1.15 0.0025 concrete\n"
                "#box: 0.00 1.15 0.00 4.00 1.30 0.0025 asphalt\n"
                "#box: 0.00 1.30 0.00 4.00 1.40 0.0025 free_space\n")

PLOT_FILTER = 'fee'
TEXT_GEO = "#geometry_view: 0 0 0 4.00 1.40 0.0025 0.0025 0.0025 0.0025 basic n \n"