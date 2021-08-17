import sys

from energy_image import compute_energy
from seam_identification_horizontal import compute_horizontal_seam, visualize_seam
from utils import Color, read_image_into_array, write_array_into_image


def remove_seam_from_image(pixels, seam_horizontal_path):
    """
    Remove pixels from the image for the specific x-coordinates in the
    'seam_horizontal_path' which gives us an output image smaller than the input 
    by one pixel in each column.
    
    """

    # Getting the number of rows in the image
    rows=len(pixels)
    # Getting the number of columns in the image
    cols=len(pixels[0])

    new_pixels=[] # Declaring a new list to store the image after deleting the pixels in the seam
    for i in range(cols):
        new_list=[]
        for j in range(rows):
            # Appending all the pixels whose row number is not equal to row in seam_path
            if(j!=seam_horizontal_path[i]): 
                new_list.append(pixels[j][i])
        new_pixels.append(new_list)

    # Rotating the image by 90 degrees as we get a rotated image as output as we are iterating
    # and filling the 'new_pixels' column wise
    new_pixels = list(reversed(list(zip(*new_pixels))))[::-1]

    return new_pixels

def remove_n_seams(pixels, num_seams_to_remove):
    """
    Removing only one seam will not be of much difference to the image. Therefore we
    input a number 'n' to remove n-seams from the image iteratively
    """


    for i in range(num_seams_to_remove):
        print(f'Removing seam {i + 1} out of {num_seams_to_remove}')

        print('  STEP 1: Computing energy...')
        energy_data = compute_energy(pixels)
        print('  STEP 2: Finding the lowest-horizontal-energy seam...')
        seam_horizontal_path, min_x_coord = compute_horizontal_seam(energy_data)
        visualized_pixels = visualize_seam(pixels, seam_horizontal_path)
        print(f'  STEP 3: Saving the current horizontal seam image to intermediate-{i+1}.png...')
        write_array_into_image(visualized_pixels, f'intermediate-{i+1}.png')

        print('  STEP 4: Removing the displayed lowest energy seam...')
        pixels = remove_seam_from_image(pixels, seam_horizontal_path)

    # We get our final image after performing the above iterations for 'n' times
    return pixels

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'USAGE: {__file__} <input> <num-seams-to-remove> <output>')
        sys.exit(1)

    input_filename = sys.argv[1] # Input image name should be the first argument
    output_filename = sys.argv[2] # Output image name should be the second argument
    num_seams_to_remove = int(sys.argv[3]) # Number of iterations to perform seam reduction should be the third argument

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)
    seam_carved_image = remove_n_seams(pixels, num_seams_to_remove)
    write_array_into_image(seam_carved_image, output_filename)

    print(f'Completed finding and removing {num_seams_to_remove} horizontal seams')
    print(f'Final Image saved to {output_filename}')

