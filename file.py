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
    1. 按时间分类保存
    2. 按内容分类保存
    :return:
    """
    count = {'air1_water2': 0, 'air2_water1': 0, 'air0_water3': 0, 'air3_water0': 0}
    if way == 'date':
        print("\nSave by date...\n")
    elif way == 'content':
        print("\nSave by content...\n")
    else:
        print("\nargs error: \'way\'\n")
        return
    for root, dirs, files in os.walk('B-scan'):
        for file in files:
            # 检查文件是否是.jpg文件
            if file.lower().endswith('.jpg'):
                # 构建源文件完整路径
                file_path = os.path.join(root, file)
                if way == 'date':
                    # 查找所有子目录下的.jpg文件，并将其存入每个日期对应文件夹内(位于每张查找到的图像的上一级中result文件夹)
                    # 获取图片的上一级目录路径
                    parent_dir = os.path.abspath(os.path.join(root, os.pardir))
                    # 确保上一级目录中存在名为result的文件夹
                    result_dir = os.path.join(parent_dir, 'result')
                    if not os.path.exists(result_dir):
                        os.makedirs(result_dir)
                    # 构建目标文件完整路径
                    dest_file_path = os.path.join(result_dir, file)
                elif way == 'content':
                    cavity_class = f"air{''.join(file)[10]}_water{''.join(file)[18]}"
                    count[cavity_class] += 1
                    result_dir = os.path.join('figure', cavity_class)
                    if not os.path.exists(result_dir):
                        os.makedirs(result_dir)
                    # 构建目标文件完整路径
                    dest_file_path = os.path.join(result_dir, f"{count[cavity_class]}.jpg")
                else:
                    break
                # 复制文件
                if not os.path.exists(dest_file_path):
                    shutil.copy(file_path, dest_file_path)
                    print(f"Copied: {file_path} to {dest_file_path} successfully")
                else:
                    print(f"{dest_file_path} already exists")


# 使用示例
# 将 'src_dir' 替换成你的源目录路径, 'dest_dir' 替换成你的目的目录路径
if __name__ == '__main__':
    # classify_all_jpgs(way='date')
    # classify_all_jpgs(way='content')
    count_all_jpgs()

# 下次更新思路:
# 1. 在终端展示文件结构
# 2. 有处理重复文件名的能力
# 3. 按照图片目标分类
# 4. 轻量化，能做到一键处理
