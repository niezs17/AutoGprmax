import os
import shutil


def count_all_jpgs():
    """
    对生成图片统计
    """
    goal = 300
    root_dir = './B-scan'
    all_count = {'air1_water2': 0, 'air2_water1': 0, 'air0_water3': 0, 'air3_water0': 0}
    print("\nStatistics on generated results...\n")
    print("Statistics by date...")
    for date_dir in os.listdir(root_dir):
        count = {'air1_water2': 0, 'air2_water1': 0, 'air0_water3': 0, 'air3_water0': 0}
        for basic_dir in os.listdir(os.path.join(root_dir, date_dir)):
            # print(os.path.join(basic_dir))
            if ''.join(basic_dir) != 'result':
                count[f"air{''.join(basic_dir)[10]}_water{''.join(basic_dir)[18]}"] += 1
                all_count[f"air{''.join(basic_dir)[10]}_water{''.join(basic_dir)[18]}"] += 1
        print("***************************")
        print(f"{os.path.join(date_dir)}")
        for key, value in count.items():
            print(f"{key}: {value:>4}")
    print("\nStatistics by all...")
    print("***************************************************")
    for key, value in all_count.items():
        print(f"{key}: {value:>4}      goal: {goal:>4}       prog: {int(value/goal * 100):>3}%")
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
    count = {'air1_water2': 0, 'air2_water1': 0, 'air0_water3': 0, 'air3_water0': 0}

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
            if file.lower().endswith('.jpg'):
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
                    if file.lower().endswith('.jpg'):
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
                if file.lower().endswith('.jpg'):
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


# 使用示例
# 将 'src_dir' 替换成你的源目录路径, 'dest_dir' 替换成你的目的目录路径
if __name__ == '__main__':
    classify_all_jpgs(way='date')
    classify_all_jpgs(way='content')
    count_all_jpgs()
