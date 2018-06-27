# Written by Peter Leonard: Z5128899 for COMP9021 
# Assignment 2 17s1

# Input:
# The input is expected to consist of ydim lines of xdim 0’s and 1’s,
# where xdim and ydim are at least equal to 2 and at most equal to 50,
# with possibly lines consisting of spaces only that will be ignored and with possibly spaces anywhere on the lines with digits.
# If n is the xth digit of the yth line with digits, with 0 ≤ x < xdim and 0 ≤ y < ydim,
# then n is to be associated with a point situated x×0.4 cm to the right and y×0.4 cm below an origin.

from argparse import ArgumentParser
from re import sub
from statistics import mean
from itertools import count
from math import ceil
import os
import sys

import operator

# length in cm
length = 0.4

# display grid (for testing purpose)
def display_grid():
    for i in range(y_dim):
        print('    ', end = '')
        for j in range(x_dim):
            print(f' {grid[i][j]}', end = '') if grid[i][j] else print(' 0', end = '')
        print()
    print()

def display_dirgrid():
    for i in range(y_dim):
        print('    ', end = '')
        for j in range(x_dim):
            print(f' {dir_grid[i][j]}', end = '') if grid[i][j] else print(' 0', end = '')
        print()
    print()

# direction list
dir_list = ['N','NE','E','SE','S','SW','W','NW']

def get_nextDirection(current_direction):
    if current_direction == 'NW':
        next_direction = dir_list[0]
    else:
        next_direction = dir_list[dir_list.index(current_direction) + 1]

    return next_direction

def get_ij_from_direction(direction, i, j):
    if i and direction == 'N':
        i = i - 1
        j = j
    elif i and j < x_dim - 1 and direction == 'NE':
        i = i - 1
        j = j + 1
    elif j < x_dim - 1 and direction == 'E':
        i = i
        j = j + 1
    elif i < y_dim - 1 and j < x_dim - 1 and direction == 'SE':
        i = i + 1
        j = j + 1
    elif i < y_dim - 1 and direction == 'S':
        i = i + 1
        j = j
    elif i < y_dim - 1 and j and direction == 'SW':
        i = i + 1
        j = j - 1
    elif j and direction == 'W':
        i = i
        j = j - 1
    elif i and j and direction == 'NW':
        i = i - 1
        j = j - 1
    else:
        return -1, -1

    return i, j

def get_direction(direction):
    original_direction = get_nextDirection(direction)
    original_direction = get_nextDirection(original_direction)
    original_direction = get_nextDirection(original_direction)
    original_direction = get_nextDirection(original_direction)
    
    next_direction = get_nextDirection(direction)
    next_direction = get_nextDirection(next_direction)
    next_direction = get_nextDirection(next_direction)
    next_direction = get_nextDirection(next_direction)
    next_direction = get_nextDirection(next_direction)

    return original_direction, next_direction
        
def clear_visited_grid():
    for i in range(y_dim):
        for j in range(x_dim):
            visited[i][j] = False

def colour_polygons():
    colour = 2
    for i in range(y_dim):
        for j in range(x_dim):
            if grid[i][j] == 1:
                # initiate variable
                start_i = i
                start_j = j
                direction = 'SE'
                axis = 0
                perimeter_axis[colour] = 0
                perimeter_diagonal[colour] = 0
                area[colour] = 0
                convex[colour] = True

                clear_visited_grid()
                colour_ij(start_i, start_j, i, j, direction, colour)
                perimeter_axis[colour] *= length
                area[colour] = abs(area[colour]) * (length**2) / 2
                colour += 1
    return colour

def get_perimeter(next_direction, colour):
    if next_direction == 'N' or next_direction == 'E' or next_direction == 'S' or next_direction == 'W':
        perimeter_axis[colour] += 1
    else:
        perimeter_diagonal[colour] += 1

def get_area(i, j, next_i, next_j, colour):
    area[colour] += (i * next_j) - (j * next_i)

def is_convex(original_direction, next_direction, colour):
    if next_direction == (get_nextDirection(original_direction)) or next_direction == (get_nextDirection(get_nextDirection(original_direction))) or next_direction == get_nextDirection(get_nextDirection(get_nextDirection(original_direction))):
        convex[colour] = False
    
def colour_ij(start_i, start_j, i, j, direction, colour):
    grid[i][j] = colour
    visited[i][j] = True
    
    original_direction, next_direction = get_direction(direction)
    next_i, next_j = get_ij_from_direction(next_direction, i, j)

    for _ in range(7):
        # base case
        if start_i == next_i and start_j == next_j:
            dir_grid[i][j] = next_direction
            get_perimeter(next_direction, colour)
            get_area(i, j, next_i, next_j, colour)
            is_convex(original_direction, next_direction, colour)
            return True

        # if not valid get next direction
        if (next_i == -1 and next_j == -1) or (grid[next_i][next_j] != 1) or (visited[next_i][next_j]):
            next_direction = get_nextDirection(next_direction)
            next_i, next_j = get_ij_from_direction(next_direction, i, j)
            continue
        
        if colour_ij(start_i, start_j, next_i, next_j, next_direction, colour):
            dir_grid[i][j] = next_direction
            get_perimeter(next_direction, colour)
            get_area(i, j, next_i, next_j, colour)
            if not (start_i == i and start_j == j):
                is_convex(original_direction, next_direction, colour)
            return True

        # if colour_ij false, get next direction
        next_direction = get_nextDirection(next_direction)
        next_i, next_j = get_ij_from_direction(next_direction, i, j)

    # backtracking
    grid[i][j] = 1
    return False

# check for validity (non 1's after colouring)
def check_validity():
    for i in range(y_dim):
        for j in range(x_dim):
            if grid[i][j] == 1:
                print('Incorrect input.')
                sys.exit()

# print result function
def print_result():
    for i in range(2,nb_of_polygons):
        print(f'Polygon {i-1}:')
        if perimeter_diagonal[i] == 0:
            print(f'    Perimeter: {perimeter_axis[i]:.1f}')
        elif perimeter_axis[i] == 0:
            print(f'    Perimeter: {perimeter_diagonal[i]}*sqrt(.32)')
        else:
            print(f'    Perimeter: {perimeter_axis[i]:.1f} + {perimeter_diagonal[i]}*sqrt(.32)')
        print(f'    Area: {area[i]:.2f}')
        if convex[i]:
            print(f'    Convex: yes')
        else:
            print(f'    Convex: no')
        print(f'    Nb of invariant rotations: {rotations[i]}')
        print(f'    Depth: {depth[i]}')

def get_rotations():
    for colour in range(2, nb_of_polygons):
        # by default 1 rotation exists
        rotations[colour] = 1
        stop = False
        for i in range(y_dim):
            if stop:
                break
            for j in range(x_dim):
                if stop:
                    break
                if grid[i][j] == colour:
                    start_i = i
                    start_j = j
                    direction = dir_grid[start_i][start_j]
                    next_i, next_j = get_ij_from_direction(direction, start_i, start_j)
                    while True:
                        if next_i == i and next_j == j:
                            break
                        complete = True
                        if dir_grid[start_i][start_j] != dir_grid[next_i][next_j]:
                            if len(dir_grid[start_i][start_j]) == len(dir_grid[next_i][next_j]):
                                # start looping to check
                                temp_dir = dir_grid[start_i][start_j]
                                current_i, current_j = get_ij_from_direction(temp_dir, start_i, start_j)
                                next_temp_dir = dir_grid[next_i][next_j]
                                next_next_i, next_next_j = get_ij_from_direction(next_temp_dir,next_i, next_j)
                                while True:
                                    if current_i == start_i and current_j == start_j:
                                        break
                                    if len(dir_grid[current_i][current_j]) != len(dir_grid[next_next_i][next_next_j]):
                                        complete = False
                                        break
                                    temp_dir = dir_grid[current_i][current_j]
                                    next_temp_dir = dir_grid[next_next_i][next_next_j]
                                    current_i, current_j = get_ij_from_direction(temp_dir, current_i, current_j)
                                    next_next_i, next_next_j = get_ij_from_direction(next_temp_dir, next_next_i, next_next_j)
                                if complete:
                                    start_i = next_i
                                    start_j = next_j
                                    rotations[colour] += 1
                        direction = dir_grid[next_i][next_j]
                        next_i, next_j = get_ij_from_direction(direction, next_i, next_j)
                    stop = True
def check_top(i, j, in_top, colour, cross, in_bottom):
    if j:
        if dir_grid[i-1][j-1] == 'SE' and grid[i-1][j-1] == colour:
            if in_bottom == -1:
                cross += 1
                in_bottom = 0
                in_top = 0
                return in_top, cross, in_bottom
            elif in_top == -1:
                in_top = 0
                return in_top, cross, in_bottom
            in_top = 1
    if dir_grid[i-1][j] == 'S' and grid[i-1][j] == colour:
        if in_bottom == -1:
            cross += 1
            in_bottom = 0
            in_top = 0
            return in_top, cross, in_bottom
        elif in_top == -1:
            in_top = 0
            return in_top, cross, in_bottom
        in_top = 1
    if dir_grid[i-1][j+1] == 'SW' and grid[i-1][j+1] == colour:
        if in_bottom == -1:
            cross += 1
            in_bottom = 0
            in_top = 0
            return in_top, cross, in_bottom
        elif in_top == -1:
            in_top = 0
            return in_top, cross, in_bottom
        in_top = 1
    return in_top, cross, in_bottom

def check_bottom(i, j, in_bottom, colour, cross, in_top):
    if j:
        if dir_grid[i+1][j-1] == 'NE' and grid[i+1][j-1] == colour:
            if in_bottom == -1:
                in_bottom = 0
                return in_bottom, cross, in_top
            elif in_top == -1:
                in_top = 0
                cross += 1
                in_bottom = 0
                return in_bottom, cross, in_top
            in_bottom = 1
    if dir_grid[i+1][j] == 'N' and grid[i+1][j] == colour:
        if in_bottom == -1:
            in_bottom = 0
            return in_bottom, cross, in_top
        elif in_top == -1:
            in_top = 0
            cross += 1
            in_bottom = 0
            return in_bottom, cross, in_top
        in_bottom = 1
    if dir_grid[i+1][j+1] == 'NW' and grid[i+1][j+1] == colour:
        if in_bottom == -1:
            in_bottom = 0
            return in_bottom, cross, in_top
        elif in_top == -1:
            in_top = 0
            cross += 1
            in_bottom = 0
            return in_bottom, cross, in_top
        in_bottom = 1
    return in_bottom, cross, in_top

def check_mid(i, j, in_top, in_bottom, cross):
    if not in_top and not in_bottom:
        if 'S' in dir_grid[i][j]:
            in_bottom = -1
        elif 'N' in dir_grid[i][j]:
            in_top = -1
    if in_top == 1:
        if 'S' in dir_grid[i][j]:
            cross += 1
            in_top = 0
        elif 'N' in dir_grid[i][j]:
            in_top = 0
    if in_bottom == 1:
        if 'N' in dir_grid[i][j]:
            cross += 1
            in_bottom = 0
        elif 'S' in dir_grid[i][j]:
            in_bottom = 0
    return cross, in_top, in_bottom

def get_depth():
    # first polygon always have 0 depth (outermost so to say)
    depth[2] = 0
    for colour in range(3, nb_of_polygons):
        # initiate depth for colour
        depth[colour] = 0
        in_top = 0
        in_bottom = 0
        stop = False
        for i in range(y_dim):
            if stop:
                break
            for j in range(x_dim):
                if stop:
                    break
                if grid[i][j] == colour:
                    for outer_layer in range(2, colour):
                        start_i = i
                        start_j = j
                        cross = 0
                        while (start_j):
                            start_j -= 1
                            if grid[start_i][start_j] == outer_layer:
                                if start_i:
                                    in_top, cross, in_bottom = check_top(start_i, start_j, in_top, outer_layer, cross, in_bottom)
                                if start_i < y_dim - 1:
                                    in_bottom, cross, in_top = check_bottom(start_i, start_j, in_bottom, outer_layer, cross, in_top)
                                cross, in_top, in_bottom = check_mid(start_i, start_j, in_top, in_bottom, cross)
                        if cross % 2 == 1:
                            depth[colour] += 1
                    stop = True

def get_coordinate():
    for colour in range(2, nb_of_polygons):
        coordinates[colour] = []
        stop = False
        for i in range(y_dim):
            if stop:
                break
            for j in range(x_dim):
                if stop:
                    break
                if grid[i][j] == colour:
                    coordinates[colour] = [(j, i)]
                    start_i = i
                    start_j = j
                    direction = dir_grid[start_i][start_j]
                    next_i, next_j = get_ij_from_direction(direction, start_i, start_j)
                    while True:
                        if next_i == i and next_j == j:
                            break
                        if dir_grid[start_i][start_j] != dir_grid[next_i][next_j]:
                            coordinates[colour] += [(next_j, next_i)]
                            start_i = next_i
                            start_j = next_j
                        direction = dir_grid[next_i][next_j]
                        next_i, next_j = get_ij_from_direction(direction, next_i, next_j)
                    stop = True

                    
def output_tex():
    tex_filename = sub('\..*$', '', filename) + '.tex'
    max_area = max(area.values())
    min_area = min(area.values())
    max_depth = max(depth.values())
    with open(tex_filename, 'w') as tex_file:
        print('\\documentclass[10pt]{article}\n'
              '\\usepackage{tikz}\n'
              '\\usepackage[margin=0cm]{geometry}\n'
              '\\pagestyle{empty}\n'
              '\n'
              '\\begin{document}\n'
              '\n'
              '\\vspace*{\\fill}\n'
              '\\begin{center}\n'
              '\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]', file = tex_file)
        print(f'\\draw[ultra thick] (0, 0) -- ({x_dim - 1}, 0) -- ({x_dim - 1}, {y_dim - 1}) -- (0, {y_dim - 1}) -- cycle;', file = tex_file)
        for i in range(max_depth + 1):
            print(f'%Depth {i}', file = tex_file)
            for x in range(2, nb_of_polygons):
                if depth[x] == i:
                    colour = round((max_area - area[x]) / (max_area - min_area) * 100)
                    print(f'\\filldraw[fill=orange!{colour}!yellow]', end = ' ', file = tex_file)
                    for y in coordinates[x]:
                        print(f'{y} --', end = ' ', file = tex_file)
                    print('cycle;', file = tex_file)
        print('\\end{tikzpicture}\n'
              '\\end{center}\n'
              '\\vspace*{\\fill}\n'
              '\n'
              '\\end{document}', file = tex_file)

    return tex_filename

parser = ArgumentParser()
parser.add_argument('-print', dest = 'print_tex', action= 'store_true')
parser.add_argument('--file', dest = 'filename', required = True)
args = parser.parse_args()

filename = args.filename
print_tex = args.print_tex
try:
    read_list = []
    with open(filename) as file:
        for line_no,line in enumerate(file):
            line = line.strip('\n')
            line = line.replace(" ", "")
            if line != '':
                read_list += [line]

    # getting x dim and y dim
    x_dim = len(read_list[0])
    y_dim = len(read_list)

    # check for incorrect input
    incorrect_input = False
    if x_dim > 50 or y_dim > 50 or x_dim < 2 or y_dim < 2:
        incorrect_input = True

    for i in range(0, len(read_list)):
        for x in range(0, len(read_list[i])):
            if int(read_list[i][x]) < 0 or int(read_list[i][x]) > 1:
                incorrect_input = True
                break

    if incorrect_input:
        print('Incorrect input.')
        sys.exit()

except FileNotFoundError:
    print(f'File {filename} could not be found.')


# creating grid
grid = [[0 for _ in range(x_dim)] for _ in range(y_dim)]
visited = [[None for _ in range(x_dim)] for _ in range(y_dim)]
dir_grid = [[None for _ in range(x_dim)] for _ in range(y_dim)]

for i in range(y_dim):
    for j in range(x_dim):
        grid[i][j] = int(read_list[i][j])

# initiate dictionary for each answer
perimeter_axis = {}
perimeter_diagonal = {}
area = {}
convex = {}
rotations = {}
depth = {}
coordinates = {}

# colour polygons
try:
    nb_of_polygons = colour_polygons()
except RecursionError:
    print('Incorrect input.')
    sys.exit()
# check validity
check_validity()

# get invariant rotations and depth
get_rotations()
get_depth()
get_coordinate()

# print the calculation
print_result()

# output -print
if print_tex:
    tex_filename = output_tex()
    os.system('pdflatex ' + tex_filename)
