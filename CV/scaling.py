import numpy as np
from PIL import Image
from numpy import array

img1 = Image.open('images/img1.jpg')

img1_mat = array(img1)

print(img1_mat.shape)

img2 = Image.open('images/img4.jpg')

img2_mat = array(img2)

print(img2_mat.shape)

#img = Image.fromarray(img2_mat)
#img.show()

new_mat = np.empty(img1_mat.shape, dtype=np.uint8)

print(new_mat.shape)

for i in range(img1_mat.shape[0]):
    for j in range(img1_mat.shape[1]):
        for k in range(img1_mat.shape[2]):
            new_mat[i,j,k] = img2_mat[i,j,k]

img = Image.fromarray(new_mat)
img.show()

sum_mat = img1_mat + new_mat

img = Image.fromarray(sum_mat)
img.show()