import os
import shutil

def countAllJpgs():
    """
    Count all generated images
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
            if not basic_dir.lower().startswith('result'):
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

def classifyAllJpgs(way):
    """
    Classify and save generated images
    :way='date':     Save by date
    :way='content':  Save by content
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
        # Skip files in the result directory
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

def removeAllJpgs(way):
    """
    Safely remove images
    :way='date':     Remove date-classified folders
    :way='content':  Remove content-classified folders
    :return: None
    """
    # Traverse all files and folders under root_dir
    remove_file = []
    if way == 'date':
        print("\nRemove by date...\n")
        for root, dirs, files in os.walk('B-scan'):
            # Check if the current directory is result
            if os.path.basename(root) == 'result':
                # Traverse all files under the current result folder
                for file in files:
                    # Assume image file extensions are .jpg, etc.
                    if file.lower().endswith('.jpg') and file.lower().startswith('bscan'):
                        # Construct the full path of the image
                        file_path = os.path.join(root, file)
                        remove_file.append(f"remove: {file_path}\n")
                        # Delete the image
                        os.remove(file_path)
    elif way == 'content':
        print("\nRemove by content...\n")
        for root, dirs, files in os.walk('figure'):
            # Traverse all files under the current figure folder
            for file in files:
                # Assume image file extensions are .jpg, etc.
                if file.lower().endswith('.jpg') and file.lower().startswith('bscan'):
                    # Construct the full path of the image
                    file_path = os.path.join(root, file)
                    remove_file.append(f"remove: {file_path}\n")
                    # Delete the image
                    os.remove(file_path)
    else:
        print("args error: \'way\'")
        return
    if len(remove_file) > 0:
        print(f"\n** Remove   \n{''.join(remove_file)}\ncount: {len(remove_file):>5}\n")
    else:
        print(f"No files removed")

def reorganize():
    os.system('cls' if os.name == 'nt' else 'clear')
    # removeAllJpgs(way='date')
    # removeAllJpgs(way='content')
    classifyAllJpgs(way='date')
    classifyAllJpgs(way='content')
    countAllJpgs()

if __name__ == '__main__':
    reorganize()
