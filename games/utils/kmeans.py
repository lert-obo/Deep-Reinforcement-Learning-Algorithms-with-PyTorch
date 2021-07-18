import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# from scipy.io import loadmat
from scipy import misc
from PIL import Image
import os

def read_image(filepath):
    
    # loading the png image as a 3d matrix
    # img = misc.imread(filepath)
    
    img = mpimg.imread(filepath)

    # uncomment the below code to view the loaded image
    plt.imshow(img) # plotting the image
    plt.show()
    
    # # scaling it so that the values are small
    img = img / 255

    return img

def initialize_means(img, clusters):
    
    # reshaping it or flattening it into a 2d matrix
    points = np.reshape(img, (img.shape[0] * img.shape[1],
                                            img.shape[2]))
    m, n = points.shape

    # clusters is the number of clusters
    # or the number of colors that we choose.
    
    # means is the array of assumed means or centroids.
    means = np.zeros((clusters, n))

    # random initialization of means.
    for i in range(clusters):
        print(f"clusters i : {i}")
        rand1 = int(np.random.random(1)*10)
        rand2 = int(np.random.random(1)*8)
        means[i, 0] = points[rand1, 0]
        means[i, 1] = points[rand2, 1]

    return points, means


# Function to measure the euclidean
# distance (distance formula)
def distance(x1, y1, x2, y2):
    
    dist = np.square(x1 - x2) + np.square(y1 - y2)
    dist = np.sqrt(dist)

    return dist


def k_means(points, means, clusters):

    iterations = 10 # the number of iterations
    m, n = points.shape
    
    # these are the index values that
    # correspond to the cluster to
    # which each pixel belongs to.
    index = np.zeros(m)

    # k-means algorithm.
    while(iterations > 0):
        print(f"iterations : {iterations}")
        for j in range(len(points)):
            
            # initialize minimum value to a large value
            minv = 1000
            temp = None
            
            for k in range(clusters):
                
                x1 = points[j, 0]
                y1 = points[j, 1]
                x2 = means[k, 0]
                y2 = means[k, 1]
                
                if(distance(x1, y1, x2, y2) < minv):        
                    minv = distance(x1, y1, x2, y2)
                    temp = k
                    index[j] = k
        
        for k in range(clusters):
            
            sumx = 0
            sumy = 0
            count = 0
            
            for j in range(len(points)):
                
                if(index[j] == k):
                    sumx += points[j, 0]
                    sumy += points[j, 1]
                    count += 1
            
            if(count == 0):
                count = 1    
            
            means[k, 0] = float(sumx / count)
            means[k, 1] = float(sumy / count)    
            
        iterations -= 1

    return means, index


def compress_image(means, index, img, clusters):

    # recovering the compressed image by
    # assigning each pixel to its corresponding centroid.
    centroid = np.array(means)
    recovered = centroid[index.astype(int), :]
    
    # getting back the 3d matrix (row, col, rgb(3))
    recovered = np.reshape(recovered, (img.shape[0], img.shape[1],
                                                    img.shape[2]))

    # plotting the compressed image.
    plt.imshow(recovered)
    plt.show()

    savefile = 'compressed_' + str(clusters) + '_colors.png'
    # saving the compressed image.
    # misc.imsave('compressed_' + str(clusters) +
    #                     '_colors.png', recovered)
    print(saveFile)
    cv2.imwrite(saveFile,recovered)



def resizeImage(infile):
    basewidth = 128
    img = Image.open(infile)
    print(img)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    size = basewidth, hsize

    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    print(outfile)
    if infile != outfile:
        try:
            img.thumbnail(size, Image.ANTIALIAS)
            # im.save(outfile, "JPEG")
            plt.imshow(img) # plotting the image
            plt.show()
        except IOError:
            print (f"cannot create thumbnail filepath: {infile}")

    img = np.asarray(img)
    img = img / 255
    return img

def doCompress(filepath):

    # img = read_image(filepath)
    img = resizeImage(filepath)

    clusters = 128
    # clusters = int(input('Enter the number of colors in the compressed image. default = 16\n'))

    points, means = initialize_means(img, clusters)
    means, index = k_means(points, means, clusters)
    compress_image(means, index, img, clusters)
