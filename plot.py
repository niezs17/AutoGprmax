from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
from tools.outputfiles_merge import get_output_data
from file import reorganize

def medianFilter(image_data):
    row_num = image_data.shape[1]
    for j in range(0, row_num):
        median_value = np.median(image_data[:, j])
        for i in range(0, 2189):
                image_data[i, j] = image_data[i, j] - median_value
                # image_data[i, j] = 0
    return image_data

def exponentialGain(image_data, ymax, a=1.3,b=3.2):
    for _ymax_ in ymax[:1]:
        x = np.arange(1, len(image_data) + 1)
        y = a ** (x * 1e-2) - b 
        y = np.clip(y, None, _ymax_)

        if image_data.ndim == 1:
            image_data = image_data * y
        else:
            image_data = image_data * y[:, np.newaxis]
    return image_data

def mplPlot(filename, outputdata, dt, rxnumber, rxcomponent):
    """Creates a plot (with matplotlib) of the B-scan.

    Args:
        filename (string): Filename (including path) of output file.
        outputdata (array): Array of A-scans, i.e. B-scan data.
        dt (float): Temporal resolution of the model.
        rxnumber (int): Receiver output number.
        rxcomponent (str): Receiver output field/current component.

    Returns:
        plt (object): matplotlib plot object.
    """

    (path, filename) = os.path.split(filename)

    fig = plt.figure(num=filename + ' - rx' + str(rxnumber), 
                     figsize=(20, 10), facecolor='w', edgecolor='w')
    plt.imshow(outputdata, 
               extent=[0, outputdata.shape[1], outputdata.shape[0] * dt, 0],
               interpolation='nearest', aspect='auto', cmap='seismic', 
               vmin=-np.amax(np.abs(outputdata)), vmax=np.amax(np.abs(outputdata)))
    plt.xlabel('Trace number')
    plt.ylabel('Time [s]')
    # plt.title('{}'.format(filename))

    # Grid properties
    ax = fig.gca()
    ax.grid(which='both', axis='both', linestyle='-.')

    cb = plt.colorbar()
    if 'E' in rxcomponent:
        cb.set_label('Field strength [V/m]')
    elif 'H' in rxcomponent:
        cb.set_label('Field strength [A/m]')
    elif 'I' in rxcomponent:
        cb.set_label('Current [A]')

    # Save a PDF/PNG of the figure
    # savefile = os.path.splitext(filename)[0]
    # fig.savefig(path + os.sep + savefile + '.pdf', dpi=None, format='pdf', 
    #             bbox_inches='tight', pad_inches=0.1)
    # fig.savefig(path + os.sep + savefile + '.png', dpi=150, format='png', 
    #             bbox_inches='tight', pad_inches=0.1)

    return plt

def normalizedMplPlot(filename, outputdata, dt, rxnumber, rxcomponent, ascan_times, time_window, ymax, plot_filter):
    """Creates a plot (with matplotlib) of the B-scan.

    Args:
        filename (string): Filename (including path) of output file.
        outputdata (array): Array of A-scans, i.e. B-scan data.
        dt (float): Temporal resolution of the model.
        rxnumber (int): Receiver output number.
        rxcomponent (str): Receiver output field/current component.

    Returns:
        plt (object): matplotlib plot object.
    """

    plt.figure(num=filename + ' - rx' + str(rxnumber),
                     figsize=(6,6), facecolor='w', edgecolor='w')

    if plot_filter == 'e':
        outputdata = exponentialGain(outputdata, ymax)
    elif plot_filter == 'f':
        outputdata = medianFilter(outputdata)
    elif plot_filter == 'ee':
        outputdata = exponentialGain(outputdata, ymax)
        outputdata = exponentialGain(outputdata, ymax)
    elif plot_filter == 'ef':
        outputdata = exponentialGain(outputdata, ymax=ymax)
        outputdata = medianFilter(outputdata)
    elif plot_filter == 'fe':
        outputdata = medianFilter(outputdata)
        outputdata = exponentialGain(outputdata, ymax=ymax)
    elif plot_filter == 'eef':
        outputdata = exponentialGain(outputdata, ymax=ymax)
        outputdata = exponentialGain(outputdata, ymax=ymax)
        outputdata = medianFilter(outputdata)
    elif plot_filter == 'efe':
        outputdata = medianFilter(outputdata)
        outputdata = exponentialGain(outputdata, ymax=ymax)
        outputdata = medianFilter(outputdata)
    elif plot_filter == 'fee':
        outputdata = medianFilter(outputdata)
        outputdata = exponentialGain(outputdata, ymax=ymax)
        outputdata = exponentialGain(outputdata, ymax=ymax)
    else:
        outputdata = outputdata

    plt.imshow(outputdata,
               extent=[0, outputdata.shape[1], outputdata.shape[0] * dt, 0],
               interpolation='nearest', aspect='auto', cmap='gray',
               vmin=-np.amax(np.abs(outputdata)), vmax=np.amax(np.abs(outputdata)))
    
    plt.axis('off')
    return plt

def cropFigure(output_root_dir="./processed_figure", root_dir="./figure"):
    # Crop all .jpg images in the root directory
    # Specify the path to store processed images
    # Input the size of the processed images
    target_width = 320
    target_height = 320
    left, top, right, bottom, count= 75, 75, 540, 533, 0
    if not os.path.exists(output_root_dir):
        os.makedirs(output_root_dir)
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.jpg'):
                count += 1
                file_path = os.path.join(root, file)
                with Image.open(file_path).convert('L') as img:
                    cropped_img = img.crop((left, top, right, bottom))
                    resized_img = cropped_img.resize((target_width, target_height), Image.LANCZOS)
                    output_dir_path = os.path.join(output_root_dir, os.path.basename(os.path.dirname(file_path)))
                    if not os.path.exists(output_dir_path):
                        os.makedirs(output_dir_path)
                    output_path = os.path.join(output_dir_path, file)
                    resized_img.save(output_path)
                    print(f'{file_path} -> {output_path}')
    print(f"Done, all count: {count}")

def getYmax(in_file_path):
    if not in_file_path.endswith('.in'):
        return 580
    else:
        with open(in_file_path, 'r') as file:
            text = file.readlines()
            # The unchanged part of the .in file is fixed at 16 lines, to be updated
            depth = []
            for element_line in text[16 - len(text):]:
                element = element_line.split()[0]
                if element == '#cylinder:':
                    depth.append(float(element_line.split()[2]))
                elif element == '#box:':
                    depth.append((float(element_line.split()[5]) + float(element_line.split()[2])) / 2)
                else:
                    pass
            depth = np.array(depth)
    ymax = np.int32(40 * (37.8 * (1 - depth) - 15) + 100)
    return ymax

def generateFigure(out_file_path, save_file_path, outputdata, dt, ascan_times, time_window, plot_filter, ymax=np.array([580])):
    plt = normalizedMplPlot(out_file_path, outputdata, dt * 1e9, 1, 'Ex', ascan_times, time_window, ymax, plot_filter)
    plt.close()
    print(f"looking *.out/*.in files in {save_file_path}, ymax = {ymax}, filter = {plot_filter}")

def plot(ascan_times=120, time_window=20e-9, all_count=0, plot_filter='none'):
    root_dir = "./B-scan"
    count = 0
    ashbin = []
    for root, dirs, files in os.walk(root_dir):
        for dirname in dirs:
            if dirname.lower().startswith("basic"):
                # Absolute path of the figure folder
                figure_path = os.path.join(root, dirname)
                out_file_path = os.path.join(figure_path, "Ascan_merged.out")
                in_file_path = os.path.join(figure_path, "Ascan.in")
                if not os.path.exists(out_file_path):
                    ashbin.append(''.join(figure_path + '\n'))
                    continue
                info = f"{dirname[6:]}"
                save_file_path = os.path.join(figure_path, f"bscan_{info}.jpg")
                outputdata, dt = get_output_data(out_file_path, 1, 'Ez')
                ymax = getYmax(in_file_path)
                generateFigure(out_file_path, save_file_path, outputdata, dt, ascan_times, time_window, plot_filter, ymax)
                cropFigure()
                count += 1
                if count >= all_count != 0:
                    return
    if len(ashbin) > 0:
        print(f"*.out files not found in these folders")
        print(''.join(ashbin))
    else:
        print("procession: \'plot\' all success")

if __name__ == "__main__":
    reorganize()
    plot(all_count=1, plot_filter='eef')
