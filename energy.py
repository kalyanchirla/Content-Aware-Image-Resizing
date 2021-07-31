"""
The first step in the seam carving algorithm: computing the energy of an image.

The functions you fill out in this module will be used as part of the overall
seam carving process. If you run this module in isolation, the energy of an
image will be visualized as a grayscale heat map, with brighter spots
representing pixels:

    python3 energy.py surfer.jpg surfer-energy.png
"""


import sys

from utils import Color, read_image_into_array, write_array_into_image


def energy_at(pixels, x, y):
    """
    Compute the energy of the image at the given (x, y) position.

    The energy of the pixel is determined by looking at the pixels surrounding
    the requested position. In the case the requested position is at the edge
    of the image, the current position is used whenever a "surrounding position"
    would go out of bounds.

    This is one of the functions you will need to implement. Expected return
    value: a single number representing the energy at that point.
    """
    rows = len(pixels)
    col = len(pixels[0])

    #x_above=0,x_below=0,y_left=0,y_right=0
    if(x==0):
        x_above = x 
    else:
        x_above = x-1
    if(x==rows-1):
        x_below = x
    else:
        x_below = x+1
    if(y==0):
        y_left = y
    else:
        y_left = y-1
    if(y==col-1):
        y_right = y 
    else:
        y_right = y+1
    delta_red = ((pixels[x_below][y].r-pixels[x_above][y].r)*(pixels[x_below][y].r-pixels[x_above][y].r))+((pixels[x][y_left].r-pixels[x][y_right].r)*(pixels[x][y_left].r-pixels[x][y_right].r))
    delta_green = ((pixels[x_below][y].g-pixels[x_above][y].g)*(pixels[x_below][y].g-pixels[x_above][y].g))+((pixels[x][y_left].g-pixels[x][y_right].g)*(pixels[x][y_left].g-pixels[x][y_right].g))
    delta_blue = ((pixels[x_below][y].b-pixels[x_above][y].b)*(pixels[x_below][y].b-pixels[x_above][y].b))+((pixels[x][y_left].b-pixels[x][y_right].b)*(pixels[x][y_left].b-pixels[x][y_right].b))
    return delta_red+delta_blue+delta_green

def compute_energy(pixels):
    """
    Compute the energy of the image at every pixel. Should use the `energy_at`
    function to actually compute the energy at any single position.

    The input is given as a 2D array of colors, and the output should be a 2D
    array of numbers, each representing the energy value at the corresponding
    position.

    This is one of the functions you will need to implement. Expected return
    value: the 2D grid of energy values.
    """
    rows = len(pixels)
    col = len(pixels[0])
    energy = []
    for i in range(0,rows):
        temp = []
        for j in range(0,col):
            curr = energy_at(pixels,i,j)
            temp.append(curr)
        energy.append(temp)
    return energy


def energy_data_to_colors(energy_data):
    """
    Convert the energy values at each pixel into colors that can be used to
    visualize the energy of the image. The steps to do this conversion are:

      1. Normalize the energy values to be between 0 and 255.
      2. Convert these values into grayscale colors, where the RGB values are
         all the same for a single color.

    This is NOT one of the functions you have to implement.
    """

    colors = [[0 for _ in row] for row in energy_data]

    max_energy = max(
        energy
        for row in energy_data
        for energy in row
    )

    for y, row in enumerate(energy_data):
        for x, energy in enumerate(row):
            energy_normalized = round(energy / max_energy * 255)
            colors[y][x] = Color(
                energy_normalized,
                energy_normalized,
                energy_normalized
            )

    return colors


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    print('Computing the energy...')
    energy_data = compute_energy(pixels)
    energy_pixels = energy_data_to_colors(energy_data)

    print(f'Saving {output_filename}')
    write_array_into_image(energy_pixels, output_filename)

