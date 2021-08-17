"""

Implementing the horizontal seam carving algorithm to reduce the width of the image finding the
lowest-energy seam path horizontally in the image. The entire seam is reconstructed here.

"""

import sys

from energy_image import compute_energy
from utils import Color, read_image_into_array, write_array_into_image


class SeamEnergyWithBackPointer:
    
    """

    Represents the total energy of a seam along with a back pointer where the
    back pointer represents the parent

    """
    def __init__(self,energy,parent=None):

        #Updating the grid to store both its respective energy value and also the backpointer from it got its energy
        #Initialized 'parent' as None because the cells at row 0 will have default energy value and no backpointer it points to.
        self.energy = energy
        self.parent = parent
    

'''
 Function defined to find the min. total energy horizontal seam path
'''
def compute_horizontal_seam(energy_data):
    
    """
    
    Finding the lowest-horizontal energy seam considering the energy of each pixel in the 
    input image

    """
    # Getting the number of rows in the image
    rows = len(energy_data)
    # Getting the number of columns in the image
    col = len(energy_data[0])

    # Initializing a memoizing to calculate the energy sums horizontally (using DP)
    # This memoizing table represents the optimal cost to reach each cell (pixel) in the image 
    updated_grid = [[None for _ in rows]for rows in energy_data]

    # Initializing the 0th column of the 'updated_grid' to the same that of the 0th column of image energy data
    for i in range(rows):
        updated_grid[i][0] = SeamEnergyWithBackPointer(energy_data[i][0])
    
    # We are using the concept of dynamic programming to find the minimum total energy path horizontally
    for i in range(1,col):
        for j in range(rows):
            # Initializing a variable to find the minimum energy for the current cell
            minimum_element_energy = 0;
            # Initializing a variable to point the parent
            minimum_element_parent = -1;

            # If the current cell is not an edge cell (pixel) then we have 3 cells above to add energy from
            # the left cell (or) moving left and top (or) moving left and bottom
            if(j>0 and j<rows-1):
                if(updated_grid[j][i-1].energy<updated_grid[j-1][i-1].energy):
                    minimum_element_energy = updated_grid[j][i-1].energy
                    minimum_element_parent = j
                else:
                    minimum_element_energy = updated_grid[j-1][i-1].energy
                    minimum_element_parent = j-1
                if(updated_grid[j+1][i-1].energy<minimum_element_energy):
                    minimum_element_energy = updated_grid[j+1][i-1].energy
                    minimum_element_parent = j+1
            elif j==0: # If the current cell is in the 0th row then we can only add energy from the left cell or moving left and down
                if(updated_grid[j][i-1].energy<updated_grid[j+1][i-1].energy):
                    minimum_element_energy = updated_grid[j][i-1].energy
                    minimum_element_parent = j
                else:
                    minimum_element_energy = updated_grid[j+1][i-1].energy
                    minimum_element_parent = j+1
            elif j==rows-1: # If the current cell is in the (rows-1)th row then we can only add energy from the left cell or moving left and up
                if(updated_grid[j][i-1].energy<updated_grid[j-1][i-1].energy):
                    minimum_element_energy = updated_grid[j][i-1].energy
                    minimum_element_parent = j
                else:
                    minimum_element_energy = updated_grid[j-1][i-1].energy
                    minimum_element_parent = j-1
            # Updating the current cell of the memoization table with the minimum energy value and its parent
            updated_grid[j][i]=SeamEnergyWithBackPointer(
                energy_data[j][i]+minimum_element_energy,
                minimum_element_parent
            )
    '''
    Now, we have the memoization table representing the horizontal sum of energies for
    every row and parents corresponding to every cell (pixel).

    So, our main task is to find the minimum horizontal energy path from the given memoization
    table

    By looking at the last column of the memoization table, we can find the out the minimum total horizontal
    energy and from there we can backtrack to the first column taking the help of parents' data store 
    at every cell in the memoization table to get the seam_path
    '''

    # Initializing the min_x_coord to find the x-coord with the minimum energy sum 
    # as we already know that the y-coord is `col-1`
    min_x_coord=0
    
    # Initialzing a variable to store the current minimum horizontal energy sum 
    min_hseam_energy = sys.maxsize
    for x in range(rows):
        if(min_hseam_energy>updated_grid[x][col-1].energy):
            min_x_coord=x
            min_hseam_energy=updated_grid[x][col-1].energy

    # Now we have min. horizontal seam energy in min_hseam_energy and the x-coord in min_x_coord

    # Declaring a list to store the path of pixels in the corresponding horizontal seam line
    minimum_horizontal_seam_path=[]
    #print(f'The min. vseam energy: {min_hseam_energy}')
    #print(f'The min. ycoord vseam: {min_x_coord}')
    
    # Finding the horizontal energy seam path backtracking the parents' data
    for i in range(col-1,-1,-1):
        minimum_horizontal_seam_path.append(min_x_coord)
        min_x_coord = updated_grid[min_x_coord][i].parent
    
    # As we are appending the list from the last row to the first, we need to reverse the list to align the path
    minimum_horizontal_seam_path.reverse()

    '''
    Returning the lowest-energy seam path (x-coordinates) to get the minimum horizontal seam energy 
    path in the current input image and also the total energy of this minimum seam. 
    
    We return a tuple (minimum_horizontal_seam_path, total_energy_of_path)

    It is not mandatory to return 'total_energy_path'. I have just used this variable to check the working
    of my code.
    '''
    return(minimum_horizontal_seam_path,min_hseam_energy)

# Creating a function to draw a horizontal path on the image where the minimum seam is found so as to visualize
def visualize_seam(pixels, seam_horizontal_path):
    
    """
    
    Draws a green line on the image along the given seam (To visualize where the seam is)

    """

    rows = len(pixels)
    cols = len(pixels[0])

    # Initializing a new 2D list to visualize our line drawn image to
    new_pixels = [[p for p in row] for row in pixels]

    # Iterating through the seam_horizontal_path list to mark the cell with green color
    for y, seam_x in enumerate(seam_horizontal_path):
        '''
        If we color only the pixels that are in `seam_horizontal_path` then the seam would not be
        visible enough. Therefore, we color 2 cells left and 2 cells right to the pixel which is in the seam
        for visibility.
        '''

        min_x = max(seam_x-2,0)
        max_x = min(seam_x+2,rows-1)

        for x in range(min_x,max_x+1):
            new_pixels[x][y] = Color(0,255,0)  #Changing the color of pixels to GREEN (RGB)

    return new_pixels


if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1] # We provide the input file in the 1st argument
    output_filename = sys.argv[2] # We provide the output file in the 2nd argument

    '''
    STEP 1: Read the input image
    '''
    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    '''
    STEP 2: Calculate the energy of image
    '''
    print('Computing the energy...')
    energy_data = compute_energy(pixels) 

    '''
    STEP 3: Finding the min. horizontal seam path to eliminate the pixels
    '''
    print('Finding the lowest-horizontal-energy seam...')
    seam_horizontal_path, min_hseam_energy = compute_horizontal_seam(energy_data)
    print(f'Computation Completed')
    visualized_pixels = visualize_seam(pixels, seam_horizontal_path)
    '''
    STEP 4: Saving the output 
    '''
    print(f'Saving the output image to {output_filename}')
    write_array_into_image(visualized_pixels, output_filename)
    print()
    # Printing the minimum horizontal seam energy to verify the correctness. The below statement can be commented
    print(f'Minimum horizontal seam energy was {min_hseam_energy} at y = {seam_horizontal_path[-1]}')
    print()
