import os
import shutil

# def exponential_gain(image_data, a=1.3, b=3.1, ymax=500):
#     x = np.arange(1, len(image_data) + 1)
#     y = a ** (x * 1e-2) - b
#     # Limiting the gain
#     y = np.clip(y, None, ymax)
#
#     # Check if image_data is 1D or 2D and apply gain accordingly
#     if image_data.ndim == 1:
#         image_data = image_data * y
#     else:
#         image_data = image_data * y[:, np.newaxis]
#
#     col_num = image_data.shape[1]
#     row_num = image_data.shape[0]
#     for i in range(col_num):
#         # 计算平均值
#         median_value = np.median(image_data[:, i])
#         # print(f"col_before: {np.array(image_data[:, i])}")
#         # print(f"median_values: {median_value}")
#         image_data[:, i] = image_data[:, i] - median_value
#         # for j in range(row_num):
#             # if image_data[j, i] < median_value:
#             #     image_data[:, i] = image_data[:, i] + median_value * weight
#             # else:
#             #     image_data[:, i] = image_data[:, i] - median_value * weight
#         # print(f"col_then  : {np.array(image_data[:, i])}")
#     return image_data


def count_all_jpgs():
    """
    对生成图片统计
    """
    goal = 300
    count_sum = 0
    root_dir = './B-scan'
    all_count = {'air2_water0': 0, 'air0_water2': 0,
                 'air1_water0': 0, 'air0_water1': 0,
                 'air1_water1': 0}
    print("\nStatistics on generated results...\n")
    print("Statistics by date...")
    for date_dir in os.listdir(root_dir):
        count = {'air2_water0': 0, 'air0_water2': 0,
                 'air1_water0': 0, 'air0_water1': 0,
                 'air1_water1': 0}
        for basic_dir in os.listdir(os.path.join(root_dir, date_dir)):
            # print(os.path.join(basic_dir))
            if not basic_dir.lower().startswith('result') :
                print(basic_dir)
                count[f"air{''.join(basic_dir)[10]}_water{''.join(basic_dir)[18]}"] += 1
                all_count[f"air{''.join(basic_dir)[10]}_water{''.join(basic_dir)[18]}"] += 1
        print("***************************")
        print(f"{os.path.join(date_dir[:10])}")
        for key, value in count.items():
            print(f"{key}: {value:>4}")
    print("\nStatistics by all...")
    print("***************************************************")
    for key, value in all_count.items():
        print(f"{key}: {value:>4}      goal: {goal:>4}       prog: {int(value / goal * 100):>3}%")
        count_sum += value
    print("***************************************************")
    print(f"sum: {count_sum:>5}")
    print("***************************************************")


def classify_all_jpgs(way):
    """
    对生成图片分类保存
    :way='date':     按时间分类保存
    :way='content':  按内容分类保存
    :return: None
    """
    new_file = []
    overwrite_file = []
    count = {'air2_water0': 0, 'air0_water2': 0,
             'air1_water0': 0, 'air0_water1': 0,
             'air1_water1': 0}
    cavity_class = 'none'
    dest_file_path = 'none'

    if way == 'date':
        print("\nSave by date...\n")
    elif way == 'content':
        print("\nSave by content...\n")
    else:
        print("\nargs error: \'way\'\n")
        return

    for root, dirs, files in os.walk('B-scan'):
        # 跳过result目录中的文件
        if 'result' in root:
            continue

        for file in files:
            if file.lower().endswith('.jpg') and file.lower().startswith('bscan'):
                file_path = os.path.join(root, file)
                parent_dir = os.path.abspath(os.path.join(root, os.pardir))

                if way == 'date':
                    result_dir = os.path.join(parent_dir, 'result')
                elif way == 'content':
                    cavity_class = f"air{file[10]}_water{file[18]}"
                    count[cavity_class] += 1
                    result_dir = os.path.join('figure', cavity_class)
                else:
                    break

                if not os.path.exists(result_dir):
                    os.makedirs(result_dir)

                if way == 'date':
                    dest_file_path = os.path.join(result_dir, file)
                elif way == 'content':
                    dest_file_path = os.path.join(result_dir, f"{count[cavity_class]}.jpg")

                if os.path.exists(dest_file_path):
                    overwrite_file.append(f"overwrite: {file_path} -> {dest_file_path}\n")
                else:
                    new_file.append(f"add: {file_path} -> {dest_file_path}\n")
                shutil.copy(file_path, dest_file_path)

    if new_file:
        print(f"\n** New   \n{''.join(new_file)}\ncount: {len(new_file):>5}\n")
    else:
        print("No files added")

    if overwrite_file:
        print(f"\n** Overwrite   \n{''.join(overwrite_file)}\ncount: {len(overwrite_file):>5}\n")
    else:
        print("No files overwrote")


def remove_all_jpgs(way):
    """
    安全删除图像
    :way='date':     删除时间分类文件夹
    :way='content':  删除内容分类文件夹
    :return: None
    """
    # 遍历root_dir下的所有文件和文件夹
    remove_file = []
    if way == 'date':
        print("\nRomove by date...\n")
        for root, dirs, files in os.walk('B-scan'):
            # 检查当前目录名是否为result
            if os.path.basename(root) == 'result':
                # 遍历当前result文件夹下的所有文件
                for file in files:
                    # 假设图片文件的扩展名为.jpg等
                    if file.lower().endswith('.jpg') and file.lower().startswith('bscan'):
                        # 构建图片的完整路径
                        file_path = os.path.join(root, file)
                        remove_file.append(f"remove: {file_path}\n")
                        # 删除图片
                        os.remove(file_path)
    elif way == 'content':
        print("\nRemove by content...\n")
        for root, dirs, files in os.walk('figure'):
            # 遍历当前figure文件夹下的所有文件
            for file in files:
                # 假设图片文件的扩展名为.jpg等
                if file.lower().endswith('.jpg') and file.lower().startswith('bscan'):
                    # 构建图片的完整路径
                    file_path = os.path.join(root, file)
                    remove_file.append(f"remove: {file_path}\n")
                    # 删除图片
                    os.remove(file_path)
    else:
        print("args error: \'way\'")
        return
    if len(remove_file) > 0:
        print(f"\n** Remove   \n{''.join(remove_file)}\ncount: {len(remove_file):>5}\n")
    else:
        print(f"No files removed")


# def exponential_gain(data, a=1.3, b=3.1, ymax=500):
#     x = np.arange(1, len(data) + 1)
#     y = a ** (x * 1e-2) - b
#     # Limiting the gain
#     y = np.clip(y, None, ymax)
#
#     # Check if data is 1D or 2D and apply gain accordingly
#     if data.ndim == 1:
#         data = data * y
#     else:
#         data = data * y[:, np.newaxis]
#
#     return data

def file():
    os.system('cls' if os.name == 'nt' else 'clear')
    # remove_all_jpgs(way='date')
    # remove_all_jpgs(way='content')
    classify_all_jpgs(way='date')
    classify_all_jpgs(way='content')
    count_all_jpgs()


if __name__ == '__main__':
    file()
