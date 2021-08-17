# Content-aware image resizing

Now a days, images are being viewed on various electronic devices. Therefore, the images must be resized to fit the screen according the resolution of the electronic device. There are various techniques to resize images like `cropping the image` and `scaling` but there are some issues with these techniques. Scaling the image can reduce the important objects being cropped. Cropping cannot be a good technique for some images where we do not want to loose content in the image. This is now a feature in Adobe Photoshop to resize images.

The below project is an implementation of the seam carving technique described in the paper - [Seam Carving for Content-Aware Image Resizing](http://www.cs.utexas.edu/~grauman/courses/spring2011/slides/a10-avidan.pdf)

### Examples

Let us look at an example below to get a clear understanding of the problem
\
\
**Reducing the width of the original image**
\
\
<img align="left" src="https://i.imgur.com/01hMY9U.jpg">
<img align="right" src="https://i.imgur.com/suu2qHW.png">
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

In the example above, we can see how the original image's(left image) width has been reduced to get the output image (right image). In this example, the original image has been reduced by 75 pixels.

We can also reduce the height of the image similarly using horizontal seam carving

### Process

There are multiple steps involved to implement the following.

#### STEP 1: Finding the energy of every pixel in the image

The overall idea of seam carving is to find a number of lowest energy seam (either vertical or horizontal) and remove the pixels in the corresponding seam. Here, **ENERGY** is of every pixel is calculated to find the importance of every pixel. The energy is calculated as the sum of squares of difference of colors (RGB) of current pixel with its neighboring ones. This energy function is called as the *Dual Gradient Energy function*. The higher the energy value, the less likely that pixel will be included in the seam (depends on the number of iterations). 

*There are many energy functions that we can use to find the energy at every pixel. For images with a plain and unchanging background, we can use the above dual gradient energy function which would work perfectly good. When the image has many different elements then we have go with energy functions like HoG which is not as computationally fast as gradient energy function*

After finding the energies at every pixel of the image, we can map to a gray-scale heatmap in which the important features of the image are shown in white and less important features which can be removed are shown in black color. Let us look at an example down below:

<img align="left" src="https://i.imgur.com/01hMY9U.jpg">
<img align="ight" src="https://i.imgur.com/8ghf9sM.png">

Looking at the images above, the energy-image(right image) which is a gray-scale heatmap clearly depicts the important features of the original image (left image). 

#### STEP 2: Seam Identification

The next step is to find the seam of minimum total energy. If our aim is to *reduce the width* of the image then we have to find the vertical seam of minimum total energy and if our aim is to *reduce the height* of the image then we have to find the horizontal seam of minimum total energy.

I have used the *dynamic programming* technique to find the seam of minimum total energy. If we want to find out the vertical seam of minimum total energy, we need to sum up the energies of pixels vertically from 0th row to last row (or) last row to 0th row in reverse order. Let us look at the steps below:
\
1. The energies of the 0th row pixels will remain unchanged as we start from here.
2. Let us say we want to update the energy at position x,y in the image, as the seam is vertical, `energy(x,y)= min(energy(x-1,y-1),energy(x-1,y),energy(x-1,y+1))` as we are finding the minimum total energy seam path.
3. We have to take care of edges i.e, when `x=0 and x=last_row` and `y=0 and y=last_column`.

Running the above steps for all the pixels of the image will give us a 2D array of numbers in which the last row cells contains the minimum total energy sum of its corresponding path from 0th row. We can also store the parent i.e, from which cell in the (x-1)th row are we getting the energy sum for x,y. The parent can be x-1,y-1 (or) x-1,y (or) x-1,y+1. This can be done by creating an another class to store the parent and energy.

We can even display the minimum energy seam path of the image by modifying those minimum energy pixels to any one color that we want. I have used red (255,0,0) to display vertical seam and green (0,255,0) to display horizontal seam although the colors can be of personal choice

**NOTE: The process is similar to find out the horizontal seam of minimum total energy where we start from 0th column to last column instead of starting from 0th row**
\
<img align="left" src="https://i.imgur.com/01hMY9U.jpg">
<img align="right" src="https://i.imgur.com/7esvCc7.png">
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
In the images shown above, we can see the minimum vertical seam path as a red line drawn (right image) in the first iteration. The next step is to remove the pixels in that seam.

#### STEP 3: Seam Removal

After identifying the seam in the image (either vertical or horizontal), the next step is to remove the pixels in the seam from the last row to the 0th row backtracking through the parent stored in the current cell. We perform this seam removal step iteratively for N times finding out 'N' minimum seams of total energy and removing those 'N' seams to reduce the width or height of the image by 'N' pixels

**Reducing the width of the image by 75 pixels**
\
<img align="left" width="400" height="400" src="https://i.imgur.com/tO1RnOt.gif">
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
We can see how the above image width is getting reduced by finding out 75 vertical seams of minimum total energy in this case. It can be observed that the pixels are being removed without actually affecting the content of the image. This is the main idea of **Content-aware image resizing**
