import sys

from energy_image import compute_energy
from seam_identification_vertical import compute_vertical_seam, visualize_seam
from utils import Color, read_image_into_array, write_array_into_image

def identify_object(energy_data,row1,row2,col1,col2,num):

    '''
    Mark the object by changing the corresponding pixels' energy value
    to a very small value so that the vertical energy sum in that path 
    always remains minimum and the seams passing through that object are
    always selected for carving.
    '''

    min_energy_value = -10000000 #Declaring a minimum energy value

    for i in range(row1,row2+1): 
        for j in range(col1,col2+1-num): # Subtracting the 'num' value so as to avoid out of bound exception
            energy_data[i][j]=min_energy_value # Changing the energy values for the corresponding pixels of the object
    
    return energy_data

def remove_seam_from_image(pixels, seam_vertical_path):
    """
    Remove pixels from the image for the specific y-coordinates in the
    'seam_vertical_path' which gives us an output image smaller than the input 
    by one pixel in each row.

    """

    # Getting the number of rows in the image
    rows=len(pixels)
    # Getting the number of columns in the image
    cols=len(pixels[0])

    new_pixels=[] # Declaring a new list to store the image after deleting the pixels in the seam
    for i in range(rows):
        new_list=[]
        for j in range(cols):
            # Appending all the pixels whose col number is not equal to column in seam_path
            if(j!=seam_vertical_path[i]): 
                new_list.append(pixels[i][j])
        new_pixels.append(new_list)

    return new_pixels

def remove_n_seams(pixels, num_seams_to_remove, row1, row2, col1, col2):
    """
    Removing only one seam will not be of much difference to the image. Therefore we
    input a number 'n' to remove n-seams from the image iteratively
    """


    for i in range(num_seams_to_remove):
        print(f'Removing seam {i + 1} out of {num_seams_to_remove}')

        print('  STEP 1: Computing energy...')
        energy_data = compute_energy(pixels)
        print('  STEP 2: Identifying the object to be removed...')
        energy_data = identify_object(energy_data,row1,row2,col1,col2,i)
        print('  STEP 3: Finding the lowest-vertical-energy seam...')
        seam_vertical_path, min_y_coord = compute_vertical_seam(energy_data)
        #print(' Finding the lowest-horzontal-energy seam...')
        #seam_horizontal_path, _ = compute_horizontal_seam(energy_data)
        visualized_pixels = visualize_seam(pixels, seam_vertical_path)
        print(f'  STEP 4: Saving the current vertical seam image to intermediate-{i+1}.jpg...')
        write_array_into_image(visualized_pixels, f'intermediate-{i+1}.jpg')

        print('  STEP 5: Removing the displayed lowest energy seam...')
        pixels = remove_seam_from_image(pixels, seam_vertical_path)

    # We get our final image after performing the 'n' iterations
    return pixels

if __name__ == '__main__':
    if len(sys.argv) != 7:
        print(f'USAGE: {__file__} <input> <num-seams-to-remove> <output>')
        sys.exit(1)

    input_filename = sys.argv[1] # Input image name should be the first argument
    output_filename = sys.argv[2] # Output image name should be the second argument
    row1 = int(sys.argv[3]) # Row from where the object is starting
    row2 = int(sys.argv[4]) # Row where the object is ending
    col1 = int(sys.argv[5]) # Column from where the object is starting
    col2 = int(sys.argv[6]) # Column from where the object is ending
    num_seams_to_remove = col2-col1-1 # Number of iterations to perform seam reduction which is equal the no. of columns to be removed (vertical seam carving)

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)
    seam_carved_image = remove_n_seams(pixels, num_seams_to_remove,row1,row2,col1,col2)
    write_array_into_image(seam_carved_image, output_filename)

    print(f'Completed finding and removing {num_seams_to_remove} vertical seams')
    print(f'Final Image saved to {output_filename}')

