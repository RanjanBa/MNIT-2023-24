import numpy as np
from PIL import Image
from numpy import array

img1 = Image.open('images/img3.jpg')

img1_mat = array(img1)

new_mat = np.empty(img1_mat.shape, dtype=np.uint8)

for i in range(img1_mat.shape[0]):
    for j in range(img1_mat.shape[1]):
        #for k in range(img1_mat.shape[2]):
            #new_mat[i,j,k] = img1_mat[i,j,k] if img1_mat[i,j,k] > 100 else 0
        new_mat[i,j,0] = 255 if img1_mat[i,j,0] > 127 else 0
        new_mat[i,j,1] = 255 if img1_mat[i,j,1] > 127 else 0
        new_mat[i,j,2] = 255 if img1_mat[i,j,2] > 127 else 0
        
img = Image.fromarray(new_mat)
img.show()