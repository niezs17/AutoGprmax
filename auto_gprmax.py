import os
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files
from tools.plot_Bscan import normalized_mpl_plot


def generate_bscan(text_in_ngeo, text_in_geo, generate, geometry, ascan_times, figure_number, time_window):
    """
    :param text_in_ngeo:    不带几何建模指令的输入代码(str)
    :param text_in_geo:     带有几何建模指令的输入代码(str)
    :param generate:        是否重建Bscan
    :param geometry:        是否生成几何建模
                GEN = 1, GEO = 0      重新合成BScan, 生成图像, 不生成几何建模
                GEN = 0, GEO = 0      不合成Bscan, 生成图像, 不生成几何建模
                GEN = 0, GEO = 1      无事发生
                GEN = 1, GEO = 1      不生成新的Bscan数据和图像, 只生成几何建模
    :param ascan_times:      Ascan扫描次数
    :param figure_number:   生成图像的编号
    :param time_window:     仿真时间
    :return None
    """
    if generate:
        # 生成输入文件
        in_file_name = r"./text_in/figure" + str(figure_number) + "/Ascan" + '.in'
        # 设置gprMax模拟的输入文件路径
        fil_in = os.path.join(in_file_name)
        f = open(in_file_name, 'w')
        if geometry:
            # 从头写入不带几何设置命令的in文件, 只执行1次，因为目的仅为得到建模图像，此时不需要merge
            f.writelines(text_in_geo)
            f.close()
            api(fil_in, n=1, geometry_only=False)
        else:
            f.writelines(text_in_ngeo)
            f.close()
            api(fil_in, n=ascan_times, geometry_only=False)  # A-scan 60 times
            # 用模拟出的A-Scan条数合并生成B-Scan图像(注意，这里的文件路径只能从AScan停止， 不能带数字，不能带后缀)
            merge_files(r"./text_in/figure" + str(figure_number) + "/Ascan", removefiles=True)
        print("generating succeed")
    else:
        print("skipping the generate stage")

    if geometry:
        if generate:
            print("saving succeed")
            print("looking *.out/*.in files in \'figure_x\'")
            print("looking *.vti/*.vtp files in \'figure_x\'")
        else:
            print("nothing happened")
    else:
        # 提取输出数据
        out_file_name = r"./text_in/figure" + str(figure_number) + "/Ascan_merged.out"  # 合并后文件名
        outputdata, dt = get_output_data(out_file_name, 1, 'Ez')
        plt = normalized_mpl_plot(out_file_name, outputdata, dt * 1e9, 1, 'Ez', ascan_times, time_window)
        plt.savefig(r"./scan_out" + '/Bscan' + str(figure_number) + '.jpg')
        print("saving succeed")
        print("looking *.out/*.in files in \'figure_x\'")
        print("looking *.jpg files in \'scan_out\'")
