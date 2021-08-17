"""

Implementing the vertical seam carving algorithm to reduce the width of the image finding the
lowest-energy seam path vertically in the image. The entire seam is reconstructed here.

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
 Function defined to find the total min. energy vertical seam path
'''
def compute_vertical_seam(energy_data):
    
    """
    
    Finding the lowest-vertical energy seam considering the energy of each pixel in the 
    input image

    """
    # Getting the number of rows in the image
    rows = len(energy_data)
    # Getting the number of columns in the image
    col = len(energy_data[0])

    # Initializing a memoizing to calculate the energy sums vertically (using DP)
    # This memoizing table represents the optimal cost to reach each cell (pixel) in the image 
    updated_grid = [[None for _ in rows]for rows in energy_data]

    # Initializing the 0th row of the 'updated_grid' to the same that of the 0th row of image energy data
    for i in range(col):
        updated_grid[0][i] = SeamEnergyWithBackPointer(energy_data[0][i])
    
    # We are using the concept of dynamic programming to find the minimum energy path vertically
    for i in range(1,rows):
        for j in range(col):
            # Initializing a variable to find the minimum energy for the current cell
            minimum_element_energy = 0;
            # Initializing a variable to point the parent
            minimum_element_parent = -1;
            
            # If the current cell is not an edge cell (pixel) then we have 3 cells above to add energy from
            # the above cell (or) moving top and left (or) moving top and right
            if(j>0 and j<col-1):
                if(updated_grid[i-1][j].energy<updated_grid[i-1][j-1].energy):
                    minimum_element_energy = updated_grid[i-1][j].energy
                    minimum_element_parent = j
                else:
                    minimum_element_energy = updated_grid[i-1][j-1].energy
                    minimum_element_parent = j-1
                if(updated_grid[i-1][j+1].energy<minimum_element_energy):
                    minimum_element_energy = updated_grid[i-1][j+1].energy
                    minimum_element_parent = j+1
            elif j==0: # If the current cell is in the 0th column then we can only add energy from the above cell or moving top and right
                if(updated_grid[i-1][j].energy<updated_grid[i-1][j+1].energy):
                    minimum_element_energy = updated_grid[i-1][j].energy
                    minimum_element_parent = j
                else: 
                    minimum_element_energy = updated_grid[i-1][j+1].energy
                    minimum_element_parent = j+1
            elif j==col-1: # If the current cell is in the (col-1)th column then we can only add energy from the above cell or moving top and left
                if(updated_grid[i-1][j].energy<updated_grid[i-1][j-1].energy):
                    minimum_element_energy = updated_grid[i-1][j].energy
                    minimum_element_parent = j
                else:
                    minimum_element_energy = updated_grid[i-1][j-1].energy
                    minimum_element_parent = j-1
            
            # Updating the current cell of the memoization table with the minimum energy value and its parent
            updated_grid[i][j]=SeamEnergyWithBackPointer(
                energy_data[i][j]+minimum_element_energy,
                minimum_element_parent
            )
    '''
    Now, we have the memoization table representing the vertical sum of energies for
    every column and parents corresponding to every cell (pixel).

    So, our main task is to find the minimum vertical energy path from the given memoization
    table

    By looking at the last row of the memoization table, we can find the out the minimum total vertical
    energy and from there we can backtrack to the first row taking the help of parents' data store 
    at every cell in the memoization table to get the seam_path
    '''

    # Initializing the min_y_coord to find the y-coord with the minimum energy sum 
    # as we already know that the x-coord is `row-1`
    min_y_coord=0
    
    # Initialzing a variable to store the current minimum vertical energy sum 
    min_vseam_energy = sys.maxsize
    for y in range(col):
        if(min_vseam_energy>updated_grid[rows-1][y].energy):
            min_y_coord=y
            min_vseam_energy=updated_grid[rows-1][y].energy

    # Now we have min. vertical seam energy in min_vseam_energy and the y-coord in min_y_coord

    # Declaring a list to store the path of pixels in the corresponding vertical seam line
    minimum_vertical_seam_path=[]
    #print(f'The min. vseam energy: {min_vseam_energy}')
    #print(f'The min. ycoord vseam: {min_y_coord}')
    
    # Finding the vertical energy seam path backtracking the parents' data
    for i in range(rows-1,-1,-1):
        minimum_vertical_seam_path.append(min_y_coord)
        min_y_coord = updated_grid[i][min_y_coord].parent
    
    # As we are appending the list from the last row to the first, we need to reverse the list to align the path
    minimum_vertical_seam_path.reverse()

    '''
    Returning the lowest-energy seam path (y-coordinates) to get the minimum vertical seam energy 
    path in the current input image and also the total energy of this minimum seam. 
    
    We return a tuple (minimum_vertical_seam_path, total_energy_of_path)

    It is not mandatory to return 'total_energy_path'. I have just used this variable to check the working
    of my code.
    '''
    return(minimum_vertical_seam_path,min_vseam_energy)

# Creating a function to draw a vertical path on the image where the minimum seam is found so as to visualize
def visualize_seam(pixels, seam_vertical_path):
    
    """
    
    Draws a red line on the image along the given seam (To visualize where the seam is)

    """

    rows = len(pixels)
    cols = len(pixels[0])

    # Initializing a new 2D list to save our line drawn image to
    new_pixels = [[p for p in row] for row in pixels]

    # Iterating through the seam_vertical_path list to mark the cell with red color
    for x, seam_y in enumerate(seam_vertical_path):
        '''
        If we color only the pixels that are in `seam_vertical_path` then the seam would not be
        visible enough. Therefore, we color 2 cells above and 2 cells below to the pixel which is in the seam
        for visibility.
        '''
        min_y = max(seam_y - 2, 0) 
        max_y = min(seam_y + 2, cols - 1)

        for y in range(min_y, max_y + 1):
            new_pixels[x][y] = Color(255, 0, 0) #Changing the color of pixels to RED (RGB)

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
    STEP 3: Finding the min. vertical seam path to eliminate the pixels
    '''
    print('Finding the lowest-vertical-energy seam...')
    seam_vertical_path, min_vseam_energy = compute_vertical_seam(energy_data)
    #print(seam_vertical_path)
    print(f'Computation Completed')
    visualized_pixels = visualize_seam(pixels, seam_vertical_path)
    '''
    STEP 4: Saving the output 
    '''
    print(f'Saving the output image to {output_filename}')
    write_array_into_image(visualized_pixels, output_filename)
    print()
    # Printing the minimum vertical seam energy to verify the correctness. The below statement can be commented
    print(f'Minimum vertical seam energy was {min_vseam_energy} at y = {seam_vertical_path[-1]}')
    #print(f'Minimum horizontal seam energy was {min_hseam_energy} at x = {seam_horizontal_path[-1]}')
    print()
