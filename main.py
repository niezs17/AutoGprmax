from auto_gprmax import random_cavity
from auto_gprmax import generate_bscan

# 无缺损的道路模型
TEXT_BASE \
    = ("#domain: 2.00 2.00 0.0025\n"
       "#dx_dy_dz: 0.0025 0.0025 0.0025\n"
       "#time_window: 32e-9\n"
       "#waveform: ricker 1.0 600e6 my_ricker\n"
       "#hertzian_dipole: z 0.0875 1.905 0 my_ricker\n"
       "#rx: 0.1125 1.905 0\n"
       "#src_steps: 0.031 0.0 0\n"
       "#rx_steps: 0.031 0.0 0\n"  
       "#material: 4 0.005 1 0 asphalt\n"   
       "#material: 9 0.05 1 0 concrete\n"
       "#material: 12 0.1 1 0 soilbase\n"
       "#material: 81 0.03 1 0 water\n"
       "#box: 0.00 0.00 0.00 2.00 1.90 0.0025 soilbase\n"
       "#box: 0.00 1.60 0.00 2.00 1.75 0.0025 concrete\n"
       "#box: 0.00 1.75 0.00 2.00 1.90 0.0025 asphalt\n"
       "#box: 0.00 1.90 0.00 2.00 2.00 0.0025 free_space\n"
       # "#cylinder: 0.60 1.26 0 0.60 1.26 0.0025 0.1 free_space\n"
       # "#cylinder: 1.40 1.26 0 1.40 1.26 0.0025 0.1 water\n"
       )


def generate(TEXT_INTACT_ROAD, generate_num, air_cavity_num, water_cavity_num, soil_base_space, regenerate, geometry):
    for _ in range(1, generate_num + 1, 1):
        TEXT_IN = TEXT_INTACT_ROAD + random_cavity(soil_base_space, air_cavity_num, water_cavity_num)
        # TEXT_IN = TEXT_INTACT_ROAD
        # 生成Bscan图像
        generate_bscan(
            TEXT_IN,
            regenerate,
            geometry,
            ascan_times=60,
            figure_number=_,
            time_window=64e-9,
            info=f"air_{air_cavity_num}_water_{water_cavity_num}"
        )


_regenerate_ = 1
_geometry_ = 0

if __name__ == '__main__':
    generate(TEXT_INTACT_ROAD=TEXT_BASE, generate_num=2, air_cavity_num=3, water_cavity_num=0,
             soil_base_space={'x1': 0, 'y1': 0, 'z1': 0, 'x2': 2.0, 'y2': 1.6, 'z2': 0.0025},
             regenerate=_regenerate_, geometry=_geometry_)
    generate(TEXT_INTACT_ROAD=TEXT_BASE, generate_num=2, air_cavity_num=2, water_cavity_num=1,
             soil_base_space={'x1': 0, 'y1': 0, 'z1': 0, 'x2': 2.0, 'y2': 1.6, 'z2': 0.0025},
             regenerate=_regenerate_, geometry=_geometry_)
    generate(TEXT_INTACT_ROAD=TEXT_BASE, generate_num=2, air_cavity_num=1, water_cavity_num=2,
             soil_base_space={'x1': 0, 'y1': 0, 'z1': 0, 'x2': 2.0, 'y2': 1.6, 'z2': 0.0025},
             regenerate=_regenerate_, geometry=_geometry_)
    generate(TEXT_INTACT_ROAD=TEXT_BASE, generate_num=2, air_cavity_num=2, water_cavity_num=0,
             soil_base_space={'x1': 0, 'y1': 0, 'z1': 0, 'x2': 2.0, 'y2': 1.6, 'z2': 0.0025},
             regenerate=_regenerate_, geometry=_geometry_)


# if __name__ == '__main__':
#     generate(TEXT_INTACT_ROAD=TEXT_BASE, generate_num=1, air_cavity_num=1, water_cavity_num=1,
#              soil_base_space={'x1': 0, 'y1': 0, 'z1': 0, 'x2': 2.0, 'y2': 1.6, 'z2': 0.0025},
#              regenerate=_regenerate_, geometry=_geometry_)
