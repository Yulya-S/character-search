import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def filling_factor(region):
    return region.image.mean()


def recognize(region):
    if filling_factor(region) == 1:
        return "-"
    else:
        euler = region.euler_number
        if euler == -1:  # B or 8
            if 1 in region.image.mean(0)[:3]:
                return "B"
            else:
                return "8"

        elif euler == 0:  # A 0 P D and 1/10 *
            tmp = region.image.copy()
            tmp[-1, :] = 1
            tmp_labeled = label(tmp)
            tmp_region = regionprops(tmp_labeled)
            if tmp_region[0].euler_number == -1:
                if region.eccentricity > 0.5:
                    return "A"
                else:
                    return "*"
            else:
                if 1 in region.image.mean(0)[:3]:
                    tmp = region.image.copy()
                    tmp[int(region.image.shape[0]/2) + 2, :] = 1
                    tmp_labeled = label(tmp)
                    tmp_region = regionprops(tmp_labeled)
                    if tmp_region[0].euler_number == -1:
                        return "D"
                    else:
                        return "P"
                else:
                    return "0"
        else:  # 1 W X * /
            if 1 in region.image.mean(0):
                if region.eccentricity > 0.5:
                    return "1"
                else:
                    return "*"
            tmp = region.image.copy()
            tmp[[0, -1], :] = 1
            tmp_labeled = label(tmp)
            tmp_region = regionprops(tmp_labeled)
            euler = tmp_region[0].euler_number
            if euler == -1:
                return "X"
            elif euler == -2:
                return "W"
            if region.eccentricity > 0.5:
                return "/"
            else:
                return "*"
    return "?"

image = plt.imread("symbols.png")
image = image.mean(2)
back = image[0]
image[image == back] = 0
image[image != 0] = 1
image = label(image)
regions = regionprops(image)

plt.imshow(image)
plt.show()

counts = {}

# test описан для файла "symbols.png"
test = ['D', 'X', '/', '*', '1', '*', 'A', 'A', 'P', '8', '1', 'D', 'D', 'D', '8', '*', 'P', '-', '8', 'P', '/', 'P',
        'D', '-', 'P', 'D', '/', 'A', '8', 'B', 'P', 'A', '*', 'W', '-', 'X', '8', 'A', 'A', '-', '0', 'P', '*', '8',
        'D', '8', '1', '1', 'B', 'A', '-', 'P', 'A', 'X', 'B', '*', 'P', '8', '*', '8', 'D', 'W', 'P', 'B', 'A', '/',
        'D', 'B', '-', '/', '-', '8', 'W', '1', '8', '*', 'B', '0', '*', 'X', '*', '*', '/', '0', '*', '*', '0', 'B',
        '0', '-', '-', '/', '/', 'A', 'W', '/', 'W', '8', '8', '0', 'D', '/', 'P', 'B', 'A', '1', '8', '1', '/', 'A',
        '*', '1', 'B', 'P', 'B', '0', 'B', 'W', '1', 'P', 'X', 'D', 'W', '*', 'D', 'B', 'W', '8', '-', '*', '/', '1',
        '*', 'A', '*', 'X', '*', 'A', 'B', '/', 'B', 'A', '0', '*', 'A', '/', '-', '1', 'A', '0', '/', '1', '-', '1',
        'W', '0', '*', '*', 'X', 'B', 'P', '8', 'B', '1', 'W', 'B', 'B', 'A', 'A', 'B', '*', '/', '0', 'A', 'B', '-',
        '-', 'P', '/', 'A', '-', 'X', '*', 'P', 'X', 'D', '*', 'B', 'P', '0', '-', 'A', 'D', '0', 'W', 'P', 'B', '/',
        '8', '0', '1', '8', 'D', '-', '*', '0', 'P', 'B', 'D', 'W', 'D', '*', 'W', 'P', '8', '-', 'X', 'A', '-', 'D',
        '/', '0', 'B', '-', 'B', 'P', 'B', 'B', 'D', '1', 'W', '1', 'W', '-', '*', 'X', '8', 'B', '-', '*', '0', 'X',
        'A', '0', 'P', '/', '*', 'B', '8', 'A', '1', 'P', '1', 'A', '-', 'W', 'A', '/', 'B', 'W', '1', 'B', '/', '0',
        'X', '*', 'D', 'P', '1', '0', '1', '1', 'P', '-', '*', '8', '*', 'X', 'A', '0', '1', '1', '-', '8', 'X', 'P',
        'W', 'W', 'A', '1', '1', 'D', 'W', '0', 'D', '1', 'X', 'P', '0', '*', '/', '/', 'P', '-', 'W', 'X', 'P', '8',
        '8', 'B', '-', '/', '/', '1', '1', 'X', '*', 'D', 'P', '/', '*', '1', 'D', '1', '8', '0', '*', '*', '8', '1',
        'W', 'D', 'W', 'B', '1', 'D', 'P', 'B', '8', 'D', 'B', '8', '-', 'A', '8', '/', 'D', 'P', '*', 'P', '1', '0',
        '/', '1', '0', 'P', '0', '1', 'A', '1', '*', 'W', 'X', '/', '/', 'X', '/', '-', '0', 'P', 'X', '0', '/', 'P',
        'B', 'A', 'W', '8', 'D', '/', 'W', 'X', '8', 'A', '-', 'B', 'P', 'X', '/', '1', 'D', 'A', 'B', 'D', '-', '1',
        '8', 'A', '0', '*']

er = 0

#tes = []

for region in regions:
    symbol = recognize(region)
    #tes.append(symbol)
    if test[regions.index(region)] != symbol:
        er += 1
    if symbol not in counts:
        counts[symbol] = 0
    counts[symbol] += 1

#m = 1
#for i in range(len(regions)):
#    plt.subplot(1, 10, m)
#    plt.imshow(regions[i].image)
#    m += 1
#    if m > 10:
#        print(tes[i-9: i + 1], i+1)
#        m = 1
#        plt.show()

#print(er)
print(counts)
#print(1 - counts.get("?", 0) / image.max())
print(1 - er / image.max())
