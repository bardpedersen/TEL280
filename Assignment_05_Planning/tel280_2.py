import skimage
import matplotlib.pyplot as plt
import numpy as np


class Squared(object):
    def __init__(self, x_start, x_stop, y_start, y_stop):
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.free = True
        self.goal = False
        self.start = False

    def check_box(self, image):
        for k in np.arange(self.x_start, self.x_stop, 1):
            for o in np.arange(self.y_start, self.y_stop, 1):
                red = image[int(o), int(k), 0]
                green = image[int(o), int(k), 1]
                blue = image[int(o), int(k), 2]
                if red > 200 and green < 1 and blue < 1:
                    self.free = False
                    break

                elif 100 < green > 200 and red < 200 and blue < 200:
                    self.goal = True
                    break

                elif blue > 200 and red < 200 and green < 200:
                    self.start = True
                    break


if __name__ == '__main__':

    im = skimage.io.imread('Assignment5_tel280.png')

    xstart = x__start = 0
    xstop = x__stop = 1169
    ystart = 0
    ystop = y__stop = 797
    grid_sizex = 0
    stepx = (xstop-xstart)/22
    grid_sizey = 0
    stepy = (ystop-ystart)/15
    x__stop = x__start + stepx

    list_of_nodes = []
    for i in range(21):
        x__start += stepx
        x__stop += stepx
        y__start = ystart
        y__stop = y__start + stepy
        for j in range(14):
            y__start += stepy
            y__stop += stepy
            list_of_nodes.append(Squared(x__start, x__stop, y__start, y__stop))
            im[int(y__start):int(y__stop), int(x__start)] = 0
            im[int(y__start):int(y__stop), int(x__stop)] = 0
            im[int(y__start), int(x__start):int(x__stop)] = 0
            im[int(y__start), int(x__stop):int(x__stop)] = 0

    for element, node in enumerate(list_of_nodes):
        node.check_box(im)

    plt.imshow(im)
    plt.show()
