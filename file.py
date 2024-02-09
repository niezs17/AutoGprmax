import os
import shutil


def find_and_copy_jpgs(src_dir):
    """
    找到所有源路径下所有子文件夹的.jpg文件, 并将他们统一复制到图片文件的上一级目录下./B-scan/XXXX-XX-XX
    :param src_dir:源路径文件夹
    :return: None
    """
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            # 检查文件是否是.jpg文件
            if file.lower().endswith('.jpg'):
                # 构建源文件完整路径
                file_path = os.path.join(root, file)
                # 获取图片的上一级目录路径
                parent_dir = os.path.abspath(os.path.join(root, os.pardir))
                # 确保上一级目录中存在名为result的文件夹
                result_dir = os.path.join(parent_dir, 'result')
                if not os.path.exists(result_dir):
                    os.makedirs(result_dir)
                # 构建目标文件完整路径
                dest_file_path = os.path.join(result_dir, file)
                # 复制文件
                shutil.copy(file_path, dest_file_path)
                print(f"Copied: {file_path} to {dest_file_path}")


# 使用示例
# 将 'src_dir' 替换成你的源目录路径, 'dest_dir' 替换成你的目的目录路径
if __name__ == '__main__':
    find_and_copy_jpgs(src_dir='./B-scan')
