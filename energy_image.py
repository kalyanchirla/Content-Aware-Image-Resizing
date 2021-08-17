"""
This is the primary step in the seam carving algorithm. we find the seam
based on the energy of an image. If we run this module in isolation, the energy 
of an image will be visualized as a grayscale heat map, with brighter spots
representing pixels

"""


import sys

from utils import Color, read_image_into_array, write_array_into_image


def energy_cal(pixels, x, y):
    """
    Compute the energy of the image at the given (x, y) position.

    The energy of the pixel is determined by looking at the pixels surrounding
    the requested position. In the case the requested position is at the edge
    of the image, the current position is used whenever a "surrounding position"
    would go out of bounds.

    """
    # Finding out the number of rows in the image
    rows = len(pixels)
    # Finding out the number of columns in the image
    col = len(pixels[0])

    #x_above=0,x_below=0,y_left=0,y_right=0
    '''
    Setting the neighboring bounds for current pixel [x][y].

    'x_above' represents the top neighboring bound for x
    'x_below' represents the below neighboring bound for x
    'y_left' represents the left neighboring bound for y
    'y_right' represents the right neighboring bound for y
    '''
    if(x==0):
        x_above = x # When x=0, as we do not have a top row, we consider x_above = x
    else:
        x_above = x-1 
    if(x==rows-1):
        x_below = x # When x=rows-1, as it is the last row, we consider x_below = x
    else:
        x_below = x+1
    if(y==0):
        y_left = y # When y=0, as it it is the left most column, we consider y_left=y 
    else:
        y_left = y-1
    if(y==col-1):
        y_right = y # When y=col-1, as it is the right most column, we consider y_right=y
    else:
        y_right = y+1

    '''
    We are defining the energy of the pixel as the magnitude of the rate of change of colors (R,G,B)
    at that pixel. 
    '''
    #'delta_red' represents the magnitude of change of red color with its neighboring pixels for the current pixel
    delta_red = ((pixels[x_below][y].r-pixels[x_above][y].r)*(pixels[x_below][y].r-pixels[x_above][y].r))+((pixels[x][y_left].r-pixels[x][y_right].r)*(pixels[x][y_left].r-pixels[x][y_right].r))
    #'delta_red' represents the magnitude of change of green color with its neighboring pixels for the current pixel
    delta_green = ((pixels[x_below][y].g-pixels[x_above][y].g)*(pixels[x_below][y].g-pixels[x_above][y].g))+((pixels[x][y_left].g-pixels[x][y_right].g)*(pixels[x][y_left].g-pixels[x][y_right].g))
    #'delta_red' represents the magnitude of change of blue color with its neighboring pixels for the current pixel
    delta_blue = ((pixels[x_below][y].b-pixels[x_above][y].b)*(pixels[x_below][y].b-pixels[x_above][y].b))+((pixels[x][y_left].b-pixels[x][y_right].b)*(pixels[x][y_left].b-pixels[x][y_right].b))
    
    # Energy at current pixel = delta_red+delta_blue+delta_green
    return delta_red+delta_blue+delta_green

def compute_energy(pixels):
    """
    This function is to calculate the energy values at every pixel in the image
    and return the 2D array of numbers represents the corresponding energies for 
    every pixel as output

    """
    # Finding the number of rows in the image
    rows = len(pixels)
    # Finding the number of columns in the image
    col = len(pixels[0])

    # Initializing a list which finally stores the energy values of the image
    energy = []
    for i in range(0,rows):
        temp = []
        for j in range(0,col):
            curr = energy_cal(pixels,i,j) # Using the 'energy_cal' function to calculate the energy of every pixel
            temp.append(curr)
        energy.append(temp)
    
    # After calculating the energies of all pixels in the image, return the 2D list of numbers stores in 'energy'
    return energy


def energy_image(energy_data):
    """
    Convert the energy values at each pixel into colors that can be used to
    visualize the energy of the image. The steps to do this conversion are:

      1. Normalize the energy values to be between 0 and 255.
      2. Convert these values into grayscale colors, where the RGB values are
         all the same for a single color.

    """

    # Initializing the 'grayscale_image' 2D list to save the energy_image into it.
    grayscale_image = [[0 for _ in row] for row in energy_data]

    # Finding the maximum energy value in the image to normalize energy at every pixel later
    max_energy= (-1)*(sys.maxsize)
    for x in range(len(grayscale_image)):
        for y in range(len(grayscale_image[0])):
            max_energy = max(max_energy,energy_data[x][y])

    #print(energy_data[0][0])

    for x in range(len(energy_data)):
        for y in range(len(energy_data[0])):
            energy = energy_data[x][y]
            
            # Normalizing energy at every pixel by diving (energy_at_current_pixel)/(max_energy)
            # and multiplyinh it with 255 to color the image in grayscale
            energy_normalized = round(energy / max_energy * 255)
            grayscale_image[x][y] = Color(
                energy_normalized,
                energy_normalized,
                energy_normalized
            )
    # Returning the grayscale enrgy image
    return grayscale_image


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1] # The input filename will be given as 1st argument
    output_filename = sys.argv[2] # The output filename will be given as 2nd argument

    # STEP 1: Reading  the input image
    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    # STEP 2: Computing the energy of every pixel in the input image
    print('Computing the energy...')
    energy_data = compute_energy(pixels)
    energy_pixels = energy_image(energy_data)

    # STEP 3: Save the image to the output file name
    print(f'Saving {output_filename}')
    write_array_into_image(energy_pixels, output_filename)

