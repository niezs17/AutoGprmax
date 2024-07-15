import numpy as np
import random
import config as conf

def checkDistance(center1, center2, radium, limit):
    # Calculate the distance between two centers and check if it is within the limits
    distance = np.linalg.norm(np.array(center1) - np.array(center2))
    return (np.sum(radium) + limit[1]) >= distance >= (np.sum(radium) + limit[0])

def createCavityInst(x, y, z1, z2, r, cavity_type):
    """
    Generates an instruction string to be included in the .in file and a descriptive string about the cavity type.
    :param x: center x-coordinate
    :param y: center y-coordinate
    :param z1: base height
    :param z2: top height
    :param r: radius
    :param cavity_type: type of cavity
    :return: instruction string and a description string
    """
    # Select a shape
    shape = ['box', 'cylinder']
    random_shape = random.choice(shape)
    if random_shape == 'box':
        inst = f"#{random_shape}: {round(x - r, 3)} {round(y - r, 3)} {z1} " \
               f"{round(x + r, 3)} {round(y + r, 3)} {z2} {cavity_type}\n"
    else:
        inst = f"#{random_shape}: {round(x, 3)} {round(y, 3)} {z1} " \
               f"{round(x, 3)} {round(y, 3)} {z2} {round(r, 3)} {cavity_type}\n"

    return [inst, genDescribeFile(random_shape, x, y, r, cavity_type, inst)]

def genDescribeFile(shape, x, y, r, cavity_type, inst):
    """
    Generates a document that briefly describes the input file information, used after generating cavity combinations.
    Note, the hardcoded road base coordinate '1.60' must be adjusted if road base coordinates change.
    :return: text
    """
    text = ["**********************************************************************\n"]
    if shape == 'box':
        text.append("shape: box\n")
        text.append(f"cavity_type: {cavity_type}\n")
        text.append(f"origin position: ({round(x, 3)}, {round(y, 3)})   (m)\n")
        text.append(f"depth: {round(1.60 - y, 3)}   (m)\n")
        text.append(f"width: {round(2 * r, 3)}  (m)\n")
        text.append(f"height: {round(2 * r, 3)} (m)\n\n")
        text.append(f"{inst}")
    elif shape == 'cylinder':
        text.append("shape: cylinder\n")
        text.append(f"cavity_type: {cavity_type}\n")
        text.append(f"origin position: ({round(x, 3)}, {round(y, 3)})   (m)\n")
        text.append(f"depth: {round(1.60 - y, 3)}  (m)\n")
        text.append(f"radius: {round(2 * r, 3)}    (m)\n\n")
        text.append(f"{inst}")
    else:
        text.append("Your shape is incorrect!\n")
    text.append("**********************************************************************\n\n")
    return ''.join(text)

def RandomCavity(distance_limit=None):
    """
    Generates random cavities within the specified soil base space.
    :param distance_limit: minimum and maximum distance between cavities
    :return: complete in file instructions
    """
    if distance_limit is None:
        distance_limit = [1, 2]
    create_result = [[], []]
    # Adjust road base space to prevent cavities from intersecting with PML
    conf.RANDOM_PARA['x1'] += conf.DX
    conf.RANDOM_PARA['y1'] += conf.DY
    conf.RANDOM_PARA['x2'] -= conf.DX
    conf.RANDOM_PARA['y2'] -= conf.DY
    # If the number of cavities is too large, generate only one air-filled cavity in the center of the road base
    print(f"allowed distance range between any two cavities --- min: {distance_limit[0]}, max: {distance_limit[1]}")
    if conf.AIR_CAVITY_NUM + conf.WATER_CAVITY_NUM > 2:
        x = (conf.RANDOM_PARA['x1'] + conf.RANDOM_PARA['x2']) / 2.0
        y = (conf.RANDOM_PARA['y1'] + conf.RANDOM_PARA['y2']) / 2.0
        cavity_radium = 0.2
        cavity_type = 'free_space'
        create_result[0].append(createCavityInst(x, y, conf.RANDOM_PARA['z1'], conf.RANDOM_PARA['z2'],
                                                          cavity_radium, cavity_type)[0])
        create_result[1].append(createCavityInst(x, y, conf.RANDOM_PARA['z1'], conf.RANDOM_PARA['z2'],
                                                          cavity_radium, cavity_type)[1])
        print("Too many cavities! More than 2\n"
              "Automatically generate a cylinder air cavity at the center of the road base, r = 0.2")
        return create_result
    else:
        cavity_radium = []
        cavity_centers = []
        cavity_num = 0
        while cavity_num < (conf.AIR_CAVITY_NUM + conf.WATER_CAVITY_NUM):
            cavity_radium.append(random.uniform(conf.RANDOM_PARA['r_min'], conf.RANDOM_PARA['r_max']))  # Randomly generate cavity radius
            cavity_region = {'x': [conf.RANDOM_PARA['x1'] + np.max(cavity_radium),
                                   conf.RANDOM_PARA['x2'] - np.max(cavity_radium)],
                             'y': [conf.RANDOM_PARA['y1'] + np.max(cavity_radium),
                                   conf.RANDOM_PARA['y2'] - np.max(cavity_radium)]}
            x = random.uniform(cavity_region['x'][0], cavity_region['x'][1])
            y = random.uniform(cavity_region['y'][0], cavity_region['y'][1])
            cavity_centers.append((x, y))
            # Check distance from previous cavities
            if all(checkDistance((x, y), center, cavity_radium[-1:], distance_limit) for center in cavity_centers[:-1]):
                cavity_type = 'free_space' if cavity_num < conf.AIR_CAVITY_NUM else 'water'
                create_result[0].append(createCavityInst(x, y, conf.RANDOM_PARA['z1'], conf.RANDOM_PARA['z2'],
                                                                  cavity_radium[-1], cavity_type)[0])
                create_result[1].append(createCavityInst(x, y, conf.RANDOM_PARA['z1'], conf.RANDOM_PARA['z2'],
                                                                  cavity_radium[-1], cavity_type)[1])
                cavity_num += 1
            else:
                # Adjust cavity radius or position if necessary
                cavity_centers.pop()
                pass
        create_result[0] = ''.join(create_result[0])
        create_result[1] = ''.join(create_result[1])
        return create_result
    
if __name__ == '__main__':
	for _ in range(0, 30):
		print(''.join(RandomCavity()[0]))
	print('done')