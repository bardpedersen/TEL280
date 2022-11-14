import skimage
import matplotlib.pyplot as plt

image = skimage.io.imread('Assignment5_tel280.png')


class Squared:
    def __init__(self, x_start, x_stop, y_start, y_stop):
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.free = False
        self.goal = False
        self.start = False

    def check_for_collision(self):
        for k in range(int(self.x_start), int(self.x_stop)):
            for l in range(int(self.y_start), int(self.y_stop)):
                if image[k][l][0] > 200:
                    self.free = True
        pass

    def check_for_goal(self):
        for k in range(int(self.x_start), int(self.x_stop)):
            for l in range(int(self.y_start), int(self.y_stop)):
                if image[k][l][1] > 200:
                    self.goal = True
        pass
    def check_for_start(self):
        for k in range(int(self.x_start), int(self.x_stop)):
            for l in range(int(self.y_start), int(self.y_stop)):
                if image[k][l][3] > 200:
                    self.start = True
        pass


xstart = x__start = 0
xstop = x__stop = 1169
ystart = 0
ystop = y__stop = 797
grid_sizex = 0
stepx = (xstop-xstart)/22
grid_sizey = 0
stepy = (ystop-ystart)/15
x__stop = x__start + stepx
for i in range(21):
    x__start += stepx
    x__stop += stepx
    y__start = ystart
    y__stop = y__start + stepy
    for j in range(14):
        y__start += stepy
        y__stop += stepy
        box = Squared(x__start, x__stop, y__start, y__stop)
        print(x__start, x__stop, y__start, y__stop)
        image[int(y__start):int(y__stop), int(x__start)] = 0
        image[int(y__start):int(y__stop), int(x__stop)] = 0
        image[int(y__start), int(x__start):int(x__stop)] = 0
        image[int(y__start), int(x__stop):int(x__stop)] = 0
"""
for i in range(22):
    image[int(y_start):int(y_stop), int(grid_sizex)] = 0
    grid_sizex += (x_stop-x_start)/21
    print(grid_sizex, grid_sizey)

for i in range(15):
    image[int(grid_sizey), int(x_start):int(x_stop)] = 0
    grid_sizey += (y_stop-y_start)/14
    print(grid_sizex, grid_sizey)

"""
plt.imshow(image)
plt.show()