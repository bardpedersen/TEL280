import skimage
import matplotlib.pyplot as plt
import numpy as np


# Initialize a class for creating grid with G, F and H values as vel as if the grid
# contains goal, start or obstacle.

class GridCell(object):
    def __init__(self, x, y, x_start, x_stop, y_start, y_stop):
        self.x = x
        self.y = y
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.free = True
        self.goal = False
        self.start = False
        self.G = 0
        self.H = 0
        self.F = self.G + self.H
        self.parent = None

    # Checks if the goal, start or obstacle is in the cell
    # On this image, green is goal, blue is start and red is obstacle.
    def check_box(self, image):
        for k in np.arange(self.x_start, self.x_stop, 1):
            for o in np.arange(self.y_start, self.y_stop, 1):
                red = image[int(o), int(k), 0]
                green = image[int(o), int(k), 1]
                blue = image[int(o), int(k), 2]
                if red > 200 and green < 1 and blue < 1:
                    self.free = False
                    break

                elif green > 200 and red < 200 and blue < 200:
                    self.goal = True
                    break

                elif blue > 200 and red < 200 and green < 200:
                    self.start = True
                    break


# Import image
im = skimage.io.imread('Assignment5.png')

# Defines boundaries to align grid with image
xstart = x__start = 0
xstop = x__stop = 1169
ystart = 0
ystop = y__stop = 797
grid_sizex = 0
stepx = (xstop - xstart) / 22
grid_sizey = 0
stepy = (ystop - ystart) / 15

# Create grid with cell classes and adding them to a list
list_of_nodes = []
x__stop = x__start + stepx
for i in range(21):
    x__start += stepx
    x__stop += stepx
    y__start = ystart
    y__stop = y__start + stepy
    for j in range(14):
        y__start += stepy
        y__stop += stepy
        list_of_nodes.append(GridCell(i, j, x__start, x__stop, y__start, y__stop))

        # Draw cells
        im[int(y__start):int(y__stop), int(x__start)] = 0
        im[int(y__start):int(y__stop), int(x__stop)] = 0
        im[int(y__start), int(x__start):int(x__stop)] = 0
        im[int(y__start), int(x__stop):int(x__stop)] = 0

# Check every cell if its goal, start or obstacle
for element, node in enumerate(list_of_nodes):
    node.check_box(im)

# PLot origin image
plt.imshow(im)
plt.show()
im2 = im

# Find goal and start cell
open_list = []
closed_list = []
for i in range(len(list_of_nodes)):
    if list_of_nodes[i].start:
        start_square = list_of_nodes[i]
        open_list.append(list_of_nodes[i])

for i in range(len(list_of_nodes)):
    if list_of_nodes[i].goal:
        goal_square = list_of_nodes[i]

run = True
while run:
    # Sort cells by F value and chooses the one with lowest
    open_list.sort(key=lambda x: x.F)
    q = open_list[0]

    # Find neighbouring cells
    neighbour_cell = []
    for i in range(len(list_of_nodes)):
        if list_of_nodes[i].y == q.y - 1 \
                and list_of_nodes[i].x == q.x \
                and list_of_nodes[i].free:
            upper = list_of_nodes[i]

        elif list_of_nodes[i].y == q.y - 1 \
                and list_of_nodes[i].x == q.x + 1 \
                and list_of_nodes[i].free:
            upper_right = list_of_nodes[i]

        elif list_of_nodes[i].x == q.x + 1 \
                and list_of_nodes[i].y == q.y \
                and list_of_nodes[i].free:
            right = list_of_nodes[i]

        elif list_of_nodes[i].x == q.x + 1 \
                and list_of_nodes[i].y == q.y + 1 \
                and list_of_nodes[i].free:
            lower_right = list_of_nodes[i]

        elif list_of_nodes[i].y == q.y + 1 \
                and list_of_nodes[i].x == q.x \
                and list_of_nodes[i].free:
            lower = list_of_nodes[i]

        elif list_of_nodes[i].y == q.y + 1 \
                and list_of_nodes[i].x == q.x - 1 \
                and list_of_nodes[i].free:
            lower_left = list_of_nodes[i]

        elif list_of_nodes[i].x == q.x - 1 \
                and list_of_nodes[i].y == q.y \
                and list_of_nodes[i].free:
            left = list_of_nodes[i]

        elif list_of_nodes[i].x == q.x - 1 \
                and list_of_nodes[i].y == q.y - 1 \
                and list_of_nodes[i].free:
            upper_left = list_of_nodes[i]

    neighbour_cell = [upper, upper_left, left, lower_left,
                      lower, lower_right, right, upper_right]

    for i in range(len(neighbour_cell)):

        # Calculate H. F and G in the neighbour cells
        dx = abs(goal_square.x - neighbour_cell[i].x)
        dy = abs(goal_square.y - neighbour_cell[i].y)
        neighbour_cell[i].H = (
                dx + dy)  # + (np.sqrt(2) - 2) * min(dx, dy)  # Only used for Diagonal distance

        dx = abs(start_square.x - neighbour_cell[i].x)
        dy = abs(start_square.y - neighbour_cell[i].y)
        neighbour_cell[i].G = (
                dx + dy)  # + (np.sqrt(2) - 2) * min(dx, dy)  # Only used for Diagonal distance

        neighbour_cell[i].F = neighbour_cell[i].G + neighbour_cell[i].H

        # Mark every cell we have been in with green
        im[int(neighbour_cell[i].y_start):int(neighbour_cell[i].y_stop),
            int(neighbour_cell[i].x_start):int(neighbour_cell[i].x_stop), 2] = 0
        im[int(neighbour_cell[i].y_start):int(neighbour_cell[i].y_stop),
            int(neighbour_cell[i].x_start):int(neighbour_cell[i].x_stop), 0] = 0
        im[int(neighbour_cell[i].y_start):int(neighbour_cell[i].y_stop),
            int(neighbour_cell[i].x_start):int(neighbour_cell[i].x_stop), 1] = 255

        # Checks if the neighbour cell have a parent, if not assign it one.
        if neighbour_cell[i].parent is None:
            neighbour_cell[i].parent = q

    temp = []
    not_add = []
    for i in range(len(neighbour_cell)):
        for j in range(len(open_list)):
            """if a node with the same position as successor is in the OPEN list which 
            has a lower f than successor, skip this successor"""
            if (neighbour_cell[i].y == open_list[j].y
                    and neighbour_cell[i].x == open_list[j].x
                    and neighbour_cell[i].F >= open_list[j].F):
                not_add.append(neighbour_cell[i])

            elif (neighbour_cell[i].y == open_list[j].y
                  and neighbour_cell[i].x == open_list[j].x
                  and neighbour_cell[i].F < open_list[j].F):
                open_list.remove(open_list[j])

        for j in range(len(closed_list)):
            """if a node with the same position as successor  is in the CLOSED list which
            has a lower f than successor, skip this successor"""
            if (neighbour_cell[i].y == closed_list[j].y
                    and neighbour_cell[i].x == closed_list[j].x
                    and neighbour_cell[i].F >= closed_list[j].F):
                not_add.append(neighbour_cell[i])

            elif (neighbour_cell[i].y == closed_list[j].y
                  and neighbour_cell[i].x == closed_list[j].x
                  and neighbour_cell[i].F < closed_list[j].F):
                open_list.remove(closed_list[j])

        temp.append(neighbour_cell[i])

    for i in range(len(not_add)):
        temp.remove(not_add[i])

    for i in range(len(temp)):
        open_list.append(temp[i])

    open_list.remove(q)
    closed_list.append(q)

    for i in range(len(neighbour_cell)):
        if neighbour_cell[i].goal:
            closed_list.append(neighbour_cell[i])
            run = False

plt.imshow(im)
plt.show()


# Callback to find the shortest path from start to goal
def callback(cell, start_square1, im2, parent_list):
    if start_square1.x == cell.x and start_square1.y == cell.y:
        return parent_list
    parent = cell.parent
    im2[int(cell.y_start):int(cell.y_stop), int(cell.x_start):int(cell.x_stop), 2] = 255
    im2[int(cell.y_start):int(cell.y_stop), int(cell.x_start):int(cell.x_stop), 0] = 0
    im2[int(cell.y_start):int(cell.y_stop), int(cell.x_start):int(cell.x_stop), 1] = 0
    parent_list.append(parent)
    callback(parent, start_square1, im2, parent_list)


closed_list.reverse()
parent_list = []
ans = callback(goal_square, start_square, im2, parent_list)
plt.imshow(im2)
plt.show()
plt.imsave('Assigment_5_results_manhaten_diagonal.png', im2)
