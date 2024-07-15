# AutoGprmax User Guide

## Basic Overview

### gprMax

GprMax is an open-source software based on the Finite-Difference Time-Domain (FDTD) method, primarily used for forward simulation processes in Ground Penetrating Radar (GPR). This software simulates the propagation of electromagnetic waves through various media, helping users understand and predict the performance of GPR systems in real geological environments.

GprMax can be operated on either CPU or GPU. Its CPU solver is parallelized using [OpenMP](http://openmp.org/wp/), enabling it to run efficiently on multi-core CPUs. The GPU solver, developed with the [NVIDIA CUDA](https://developer.nvidia.com/cuda-zone) programming model, further optimizes performance. Additionally, gprMax includes a [Message Passing Interface (MPI)](https://en.wikipedia.org/wiki/Message_Passing_Interface) task farm, compatible with CPU nodes or multiple GPUs.

GprMax requires users to create simple text files (`.in` files) to configure simulation scenarios. These files define the simulation's geometric structures, material properties, source signals, and receiver characteristics. This setup makes gprMax versatile, suitable not only for researchers studying geological radar but also for educational and industrial applications. Here is an example of what a typical `.in` file looks like:

```plaintext
#domain: 4.00 1.40 0.0025       
#dx_dy_dz: 0.0025 0.0025 0.0025   
#time_window: 3.2e-08
#waveform: ricker 1.0 600e6 my_ricker
#hertzian_dipole: z 0.0875 1.305 0 my_ricker
#rx: 0.1125 1.305 0
#src_steps: 0.031 0.0 0
#rx_steps: 0.031 0.0 0
#material: 4 0.005 1 0 asphalt
#material: 9 0.05 1 0 concrete
#material: 12 0.1 1 0 soilbase
#material: 81 0.03 1 0 water
#box: 0.00 0.00 0.00 4.00 1.00 0.0025 soilbase
#box: 0.00 1.00 0.00 4.00 1.15 0.0025 concrete
#box: 0.00 1.15 0.00 4.00 1.30 0.0025 asphalt
#box: 0.00 1.30 0.00 4.00 1.40 0.0025 free_space
#box: 2.787 0.604 0 2.84 0.657 0.0025 water
```

After the numerical calculations based on the `.in` files, gprMax outputs 3D GPR forward simulation results as binary files (`*.out`), generating data bodies and forward simulation images (including A-scan, B-scan, C-scan).

For more information on using gprMax, please visit:

- [gprMax official documentation](http://docs.gprmax.com/en/latest/)
- [gprMax official website](http://www.gprmax.com)

### AutoGprmax

Originally, gprMax was designed to facilitate research on the propagation characteristics of electromagnetic waves in geological environments, focusing on detailed simulations of complete propagation processes.

For example, it supports simulations of road pathologies in 2D and 3D GPR forward models, analyzing the radar reflection characteristics of pathologies and the spatial propagation characteristics of GPR waves, accumulating theoretical experience for GPR research in road cavity detection.

As machine learning and deep learning technologies for GPR image interpretation have flourished, many researchers have started using gprMax to simulate road structures, setting various road structure parameters, radar parameters, and forward simulation parameters to generate different GPR simulation images for network training datasets. However, gprMax currently only supports single operations. If there is a need to generate a batch of different road condition GPR simulation images, it requires manual adjustments to the parameters in the `.in` files, which is highly inefficient and tedious.

**AutoGprmax** was developed to address the challenge of rapidly and efficiently batch-creating complex feature images of road cavity pathologies using gprMax. Building on gprMax software, it wraps a set of Python scripts that allow you to adjust a series of parameters (mostly based on the .in file construction method used by gprMax, including basic road physical model parameters and randomly generated parameters for road cavities such as medium, quantity, diameter, and shape). With **AutoGprmax**, you can establish a complete physical model of a road area, randomly inserting cavities of various materials (inflated or water-filled), shapes (circular or rectangular), and controlling their relative random distribution within a limited time and road space range. This tool enables the generation of B-scan images that reflect hyperbolic features of cavities at various depths, quantities, and relative positions.

**Key Features of AutoGprmax:**

- AutoGprmax currently only supports the construction of datasets for road cavity pathologies.
- AutoGprmax is controlled via the command line.
- AutoGprmax can be used offline.
- AutoGprmax defaults to using CUDA drivers for simulations, requiring at least one NVIDIA parallel computing card.
- AutoGprmax has not specifically optimized GPU memory usage, **so the utilization is close to 100%**.

**Generation Speed**

- According to tests conducted by the developer, AutoGprmax's dataset generation speeds are approximately 136 images/day with an `RTX 3050ti`, 236 images/day with an `RTX 2070`, and 336 images/day with an `RTX 3060`.
- The test conditions were: 120 scans per single B-scan image, scanning step lengths of 0.0025 meters for the x, y, z axes, and a scanning time window of 32x10^{-9} seconds.

## Environment Setup

**AutoGprmax requires the following runtime environment:**

- Miniconda3
- Python version 3.9.0
- gprMax version 3.1.6
- pycuda-2021.1+cuda115
- NVIDIA (R) CUDA Compiler Driver: CUDA compilation tools, release 11.5, V11.5.50

## How to Use AutoGprmax

The parameters you need to configure are stored in the `config.py` file. You only need to modify the content of the `config.py` file to customize your own road void dataset without changing the specific source code. The main content is as follows:

```python
AIR_CAVITY_NUM : (int)
WATER_CAVITY_NUM : (int)
GENERATE_MODE : (string)
ASCAN_TIMES : (int)
TIME_WINDOW : (float)
DX : (float)
DY : (float)
DZ : (float)
TEXT_INTACT_ROAD : (string)
TEXT_GEO : (string)
```

Here is a step-by-step guide:

**First, set the road model parameters for your dataset:**

Remember that voids are generated within a defect-free road structure. A complete and ideal physical model of a road typically includes layers such as the soilbase, concrete, asphalt, and free_space. Each layer has different spatial ranges, electrical constants, and names. Additionally, when using gprMax, you need to configure the complete spatial domain, spatial step size, types of excitation signal waveforms, and more, in the road model (refer to the `.in` file in gprMax). You need to write this information into the `TEXT_INTACT_ROAD` string. Customize your physical model by modifying the following example. In subsequent random void generation, these model parameters will never change; they will be the foundation of your simulation modeling. `DX`, `DY`, `DZ`, and `TIME_WINDOW` need to be specified separately:

```python
TEXT_INTACT_ROAD = ("#domain: 4.00 1.40 0.0025\n"
                f"#dx_dy_dz: {DX} {DY} {DZ}\n"
                f"#time_window: {TIME_WINDOW}\n"
                "#waveform: ricker 1.0 600e6 my_ricker\n"
                "#hertzian_dipole: z 0.0875 1.305 0 my_ricker\n"
                "#rx: 0.1125 1.305 0\n"
                "#src_steps: 0.031 0.0 0\n"
                "#rx_steps: 0.031 0.0 0\n"  
                "#material: 4 0.005 1 0 asphalt\n"   
                "#material: 9 0.05 1 0 concrete\n"
                "#material: 12 0.1 1 0 soilbase\n"
                "#material: 81 0.03 1 0 water\n"
                "#box: 0.00 0.00 0.00 4.00 1.00 0.0025 soilbase\n"
                "#box: 0.00 1.00 0.00 4.00 1.15 0.0025 concrete\n"
                "#box: 0.00 1.15 0.00 4.00 1.30 0.0025

 asphalt\n"
                "#box: 0.00 1.30 0.00 4.00 1.40 0.0025 free_space\n")

GENERATE_MODE = 'scan'
TIME_WINDOW = 32e-9
DX = 0.0025
DY = 0.0025
DZ = 0.0025
```

**Next, determine the characteristics of the cavities you want to generate:**

In AutoGprmax, you initially need to determine the type and quantity of voids to be generated. The software supports the random creation of any number of water-filled or air-filled voids, as long as the total number is less than three. To specify the number of water-filled and air-filled voids respectively, adjust the following parameters (In subsequent operations, you will also need to specify `AIR_CAVITY_NUM` and `WATER_CAVITY_NUM` when running the `run.bat` file. Therefore, the modifications made in the `config.py` file serve only as default values when the required parameters are not inputted in the `run.bat`. This ensures that your system has predefined settings to fall back on in case the necessary parameters are omitted during the execution of the batch file, maintaining the continuity and reliability of your simulation or modeling process.):

```python
AIR_CAVITY_NUM = 1
WATER_CAVITY_NUM = 1
```

Road voids are typically distributed within a range of 0.3 to 1 meter below the ground surface, known as the soilbase. When using AutoGprmax, it is recommended that you set the spatial range for the random generation of void models based on this fact. This ensures that voids are not incorrectly generated at too shallow or too deep locations. To define the spatial range for the random generation of voids, modify the following dictionary. The keys of the dictionary include the diagonal coordinates of the generation range space and the maximum and minimum values of the void radius:

```python
RANDOM_PARA = {'x1': 0.4, 'y1': 0.35, 'z1': 0, 'x2': 3.6, 'y2': 0.7, 'z2': 0.0025, 'r_min': 0.025, 'r_max': 0.05}
```

**Then, customize the preprocessing operations for drawing B-scan images:**

To generate a single B-scan image with AutoGprmax, it first produces several A-scan (n).out scan result files along a certain line, i.e., the number of scans, which you can specify. After completing multiple A-scans, AutoGprmax merges them into an Ascan_merged.out file, and the B-scan image is then created from this merged file. Generally, the higher the number of scans, the higher the resolution of the resulting B-scan image, but the generation time will also increase accordingly.

In the process of going from the Ascan_merged.out file to drawing the B-scan image, you can specify your own B-scan image preprocessing methods. These methods often need to be implemented using array-based Python algorithms. AutoGprmax comes with exponential gain and median filter algorithms. You can select the filtering method by modifying the `PLOT_FILTER` parameter, including 'e', 'f', 'ef', 'fe', 'ee', 'eef', 'efe', 'fee'. Here, 'e' stands for the exponential gain algorithm, and 'f' stands for the median filter algorithm. Their combinations represent the sequence and number of filter applications.

```python
PLOT_FILTER = 'fee'
```

> For example:
>
> 'ef' applies the exponential gain algorithm first, followed by the median filter.
>
> 'fe' applies the median filter first, followed by the exponential gain algorithm.
>
> 'eef' applies the exponential gain algorithm twice, followed by the median filter.

**Finally, run AutoGprmax in the background for a while, and you will have completed a batch generation:**

Before running AutoGprmax, it is essential to specify the number of A-scan lines for a single image. This is typically calculated based on the length of the road model you have set and the spatial step size:

```python
ASCAN_TIMES = 120
```

After setting the number of A-scan lines for a single image in AutoGprmax, the next step is to specify the generation mode. AutoGprmax supports three operational modes, which can be modified through the `GENERATE_MODE` parameter:

```python
GENERATE_MODE = 'scan'
```

- 'geo' mode is only used to verify that the holes you have generated are correct. Each run will generate a `*.vti` file called `basic.vti` that you can open and inspect with ParaView.
- In the 'scan' mode, you are empowered to generate B-scan images entirely from scratch. This is achieved by compiling data from multiple A-scan measurements into a single, unified file. The B-scan image is then meticulously rendered based on the data contained within the `Ascan_merged.out` file.
- The 'plot' mode is specifically designed for scenarios where you have already generated the Ascan_merged.out file. In such cases, you can utilize this mode to directly draw the B-scan image based on the data from the Ascan_merged.out file.

**AutoGprmax** operates using command-line methods and includes a batch file for Windows systems named `run.bat`. If you are not using a Windows system, you can construct your own script file, like a shell script, based on the contents of the `run.bat` file.

```bash
run.bat [air_num] [water_num] [times]
```

`air_num`, `water_num`, and `times` respectively represent the number of air-filled cavities, water-filled cavities, and the total number of images to generate. Press Enter, and the script will run automatically; just leave it running in the background. For example: `run.bat 1 1 100` (1 air-filled cavity, 1 water-filled cavity, total 100 images generated)

If you see this interface, it means the run was successful!

<img src="https://cdn.jsdelivr.net/gh/niezishan/MyPic/img/image-20240715145049378.png" alt="image-20240715145049378" style="zoom:67%;" />

**In addition to this, AutoGprmax has built-in tools for automatically organizing and cropping the generated image files:**

- Running the `file.py` script enables you to calculate various metrics of the dataset and organize all successfully generated images into a unified folder named `\figure`.
- Executing the `plot.py` script allows you to crop images generated by gprMax that include axes and borders, and then consolidate all the processed images into another folder named `\processed_figure`. This helps to minimize the interference of irrelevant factors when training models.
- You have the flexibility to modify these two scripts to tailor your own statistical methods and image preprocessing techniques.

```bash
python file.py
python plot.py
```

## Prospects

- This script is constructed based on actual engineering applications and is open-sourced only for communication and reference. AutoGprmax has relatively simple functions, and the writing process was added step by step according to actual needs, lacking systematic and clarity, and there are also many redundant parts. I hope everyone understands and is welcome to make suggestions for improvement.
- The code will generate redundant `des` files. The purpose of this file is mainly to generate a file that describes the relevant void information through text each time a road void model is generated, to avoid the trouble of opening Paraview to check the correctness of the model every time. However, due to the problem of code redundancy structure, this function currently has errors and needs to be improved.
