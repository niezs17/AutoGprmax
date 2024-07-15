import os
from sys import argv
from datetime import date
import config as conf
from random_cavity import RandomCavity
from gprMax.gprMax import api
from tools.outputfiles_merge import get_output_data, merge_files
from plot import normalizedMplPlot, getYmax

def generateBscan(TEXT_IN, regenerate, geometry, describe):
    """
    Generates B-scan images and manages file operations based on given parameters.
    :param regenerate: whether to regenerate Bscan
    :param geometry: whether to generate geometry modeling
    :param describe: text description of basic image content, saved to: `./B-scan/{date.today()}/basic_{info}_{figure_number}/describe.txt`
    :return None
    """
    figure_number = 1
    text_in = TEXT_IN
    text_geo = conf.TEXT_GEO 
    info=f"air_{conf.AIR_CAVITY_NUM}_water_{conf.WATER_CAVITY_NUM}"
    figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
    if regenerate:
        if geometry:
            while os.path.exists(figure_path):
                figure_number += 1
                figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
            figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
            os.makedirs(figure_path)
        else:
            while os.path.exists(figure_path):
                figure_number += 1
                figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
            figure_number -= 1
            figure_path = f"./B-scan/{date.today()}/basic_{info}_{figure_number}"
    else:
        pass

    in_file_name = f"{figure_path}/Ascan.in"

    # Handle the generation logic
    if regenerate:
        if geometry:
            # Create directory and check if the file already exists, if so, increment the file number
            with open(in_file_name, 'w') as f:
                # Add a line to the original text for geometry modeling
                f.write(text_in)
                f.write(text_geo)
                f.close()
                api(in_file_name, n=1, geometry_only=True, gpu={0})

        else:
            # Delete the last line and scan n times based on the original in file
            with open(in_file_name, 'r') as f:
                lines = f.readlines()[:-1]
                f.close()
            with open(in_file_name, 'w') as f:
                f.writelines(lines)
                f.close()
            api(in_file_name, n=conf.ASCAN_TIMES, geometry_only=False, gpu={0})
            merge_files(f"{figure_path}/Ascan", removefiles=True)
        print("Process completed.")
    if (regenerate and not geometry) or (not regenerate):
        out_file_name = f"{figure_path}/Ascan_merged.out"
        outputdata, dt = get_output_data(out_file_name, 1, 'Ez')
        plt = normalizedMplPlot(out_file_name, outputdata, dt * 1e9, 1, ymax=getYmax(in_file_name), plot_filter='fee')
        plt.savefig(f"{figure_path}/bscan_{info}_{figure_number}.jpg")
        plt.close()
        print(f"looking *.out/*.in files in {figure_path}")
    if describe != None:
        describe_file_name = f"{figure_path}/des.txt"
        with open(describe_file_name, 'w') as f:
            f.write(describe)
            f.close()

def AutoGprmax():
    TEXT_IN = conf.TEXT_INTACT_ROAD + RandomCavity()[0]
    DESCRIBE = RandomCavity()[1]
    if conf.GENGERATE_MODE == 'geo':
        # This mode is only used to verify that the holes you have generated are correct. 
        # Each run will generate a *.vti file called basic.vti that you can open and inspect with ParaView
        generateBscan(TEXT_IN, regenerate=1, geometry=1,describe=DESCRIBE)
    elif conf.GENGERATE_MODE == 'scan':
        # This mode allows you to generate B-scan images from scratch.
        # The merged file is obtained through several A-scans, and the B-scan image is drawn according to the Ascan_merged.out file
        generateBscan(TEXT_IN, regenerate=1, geometry=1,describe=None)
        generateBscan(TEXT_IN, regenerate=1, geometry=0, describe=DESCRIBE)
    elif conf.GENGERATE_MODE == 'plot':
        # If you already generated the Ascan_merged.out file, draw the B-scan image based on the Ascan_merged.out file
        generateBscan(TEXT_IN, regenerate=0,geometry=0,describe=DESCRIBE)
    else:
        print("generate_mode error")

if __name__ == '__main__':
    # Check if there are enough parameters
    if len(argv) == 3:
        # The first element in argv (sys.argv[0]) is the script name, so parameter indices start from 1
        conf.AIR_CAVITY_NUM = int(argv[1])  # Get the first parameter
        conf.WATER_CAVITY_NUM = int(argv[2])  # Get the second parameter
        print(f"air_cavity_num: {conf.AIR_CAVITY_NUM}, water_cavity_num: {conf.WATER_CAVITY_NUM}")
    AutoGprmax()



