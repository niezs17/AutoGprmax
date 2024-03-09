from PIL import Image
import numpy as np
import os
from tools.plot_Bscan import normalized_mpl_plot
from tools.outputfiles_merge import get_output_data
from file import file


def crop_figure(output_root_dir="./processed_figure", root_dir="./figure"):
    # 裁剪根目录下所有.jpg格式图片
    # 指定处理后的图片存储路径
    # 输入处理后图片的尺寸
    target_width = 400
    target_height = 600

    # 输入裁剪的坐标范围
    left = 51
    top = 73
    right = 360
    bottom = 534

    count = 0

    # left = 0
    # top = 0
    # right = 400
    # bottom = 600
    if not os.path.exists(output_root_dir):
        os.makedirs(output_root_dir)
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.jpg'):
                count += 1
                file_path = os.path.join(root, file)
                with Image.open(file_path).convert('L') as img:
                    # 裁剪图片
                    cropped_img = img.crop((left, top, right, bottom))
                    # 调整图片尺寸
                    resized_img = cropped_img.resize((target_width, target_height), Image.LANCZOS)

                    # 将PIL图像转换为OpenCV图像
                    open_cv_image = np.array(resized_img)

                    # open_cv_image = exponential_gain(open_cv_image)

                    # 应用中值滤波
                    # median_filtered_image = cv2.medianBlur(open_cv_image, 5)
                    # median_filtered_image = median_filter(open_cv_image)

                    # 将OpenCV图像转换回PIL图像以保存(
                    final_img = Image.fromarray(open_cv_image)
                    # 保存处理后的图片
                    output_dir_path = os.path.join(output_root_dir, os.path.basename(os.path.dirname(file_path)))
                    if not os.path.exists(output_dir_path):
                        os.makedirs(output_dir_path)
                    output_path = os.path.join(output_dir_path, file)
                    final_img.save(output_path)
                    print(f'{file_path} -> {output_path}')
    print(f"Done, all count: {count}")


def get_ymax(in_file_path):
    if not in_file_path.endswith('.in'):
        return 580
    else:
        with open(in_file_path, 'r') as file:
            text = file.readlines()
            # 这里写死了.in文件不变的部分为16行，待更改
            depth = []
            for element_line in text[16 - len(text):]:
                element = element_line.split()[0]
                if element == '#cylinder:':
                    depth.append(float(element_line.split()[2]))
                elif element == '#box:':
                    depth.append((float(element_line.split()[5]) + float(element_line.split()[2]))/2)
                else:
                    pass
            depth = np.array(depth)
    ymax = np.int32(40 * (37.8 * (1 - depth) - 15) + 100)
    return ymax


def generate_figure(out_file_path, save_file_path, outputdata, dt, ascan_times, time_window, plot_filter,
                    ymax=np.array([580])):
    plt = normalized_mpl_plot(out_file_path, outputdata, dt * 1e9, 1, 'Ex', ascan_times, time_window,
                              ymax, plot_filter)
    # save_file_path = os.path.join(figure_path, plot_filter)
    # if not os.path.exists(save_file_path):
    #     os.mkdir(save_file_path)
    # if not plot_filter == 'none':
    #     save_file_path = os.path.join(figure_path, plot_filter, f'ymax={ymax}.jpg')
    # else:
    #     save_file_path = os.path.join(figure_path, plot_filter, f'none.jpg')
    # plt.savefig(save_file_path)
    plt.close()
    print(f"looking *.out/*.in files in {save_file_path}, ymax = {ymax}, filter = {plot_filter}")


def plot(ascan_times=120, time_window=20e-9, all_count=0, plot_filter='none'):
    root_dir = "./B-scan"
    count = 0
    ashbin = []
    for root, dirs, files in os.walk(root_dir):
        for dirname in dirs:
            if dirname.lower().startswith("basic"):
                # figure文件夹的绝对路径
                figure_path = os.path.join(root, dirname)
                out_file_path = os.path.join(figure_path, "Ascan_merged.out")
                in_file_path = os.path.join(figure_path, "Ascan.in")
                if not os.path.exists(out_file_path):
                    ashbin.append(''.join(figure_path + '\n'))
                    continue
                info = f"{dirname[6:]}"
                save_file_path = os.path.join(figure_path, f"bscan_{info}.jpg")
                outputdata, dt = get_output_data(out_file_path, 1, 'Ez')
                ymax = get_ymax(in_file_path)
                generate_figure(out_file_path, save_file_path, outputdata, dt, ascan_times,
                                time_window, plot_filter, ymax)
                count += 1
                if count >= all_count != 0:
                    return
                # print(f"figure_path:{figure_path}")
                # print(f"out_file_path:{out_file_path}")
                # print(f"save_file_path:{save_file_path}")
    if len(ashbin) > 0:
        print(f"*.out files not found in these folders")
        print(''.join(ashbin))
    else:
        print("procession: \'plot\' all success")



if __name__ == "__main__":
    plot( all_count=0, plot_filter='eef')
    # file()
    # print(get_ymax('E:\\PAPPER\\PROCESS\\GprMax\\gpr_in\\B-scan\\2024-03-05\\basic_air_1_water_1_49\\Ascan.in'))
