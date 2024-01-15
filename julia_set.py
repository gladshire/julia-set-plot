from PIL import Image
import numpy as np
import sys
import cmath
from joblib import Parallel, delayed


# Max iterations for graph
MAX_ITER = 100


def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z * z + c
        n += 1
    return n


def burningship(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        zx = (z.real * z.real) - (z.imag * z.imag) + c.real
        zy = 2 * abs(z.real * z.imag) + c.imag
        z = complex(zx, zy)
        n += 1
    return n


def custom(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = cmath.cos(z) + c
        n += 1
    return n


# Function for splitting image depending on number of threads
def splitImage(numThreads, width, height):
    rowsPerThread = height // numThreads
    splitPoints = []
    for i in range(numThreads):
        startRow = i * rowsPerThread
        if i < numThreads:
            endRow = startRow + rowsPerThread
        else:
            endRow = height
        splitPoints.append((startRow, endRow))
    return splitPoints


def imgThread(juliaFunction, startRow, endRow, width, height):
    imgMatrix = np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)
    imgSection = imgMatrix[startRow:endRow, :]
    for y in range(startRow, endRow):
        for x in range(width):
            pixelCoord = complex(
                xlimLower + (x / width) * (xlimUpper - xlimLower),
                ylimLower + (y / height) * (ylimUpper - ylimLower),
            )
            imgSection[y - startRow, x, 0] = juliaFunction(pixelCoord)
            currNumIter = imgSection[y - startRow, x, 0]
            currHue = itersToHue(currNumIter)
            value = 255 if currNumIter < MAX_ITER else 0
            imgSection[y - startRow, x] = (currHue, 255, value)
    return startRow, endRow, imgSection


def itersToHue(pixelValue):
    hue = int(255 * pixelValue / MAX_ITER)
    return hue


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print(
            "Usage: python3 julia_set.py xlimL xlimU ylimL ylimU WIDTH HEIGHT filename"
        )
        exit()


    # Obtain image specification from arguments
    xlimLower = float(sys.argv[1])
    xlimUpper = float(sys.argv[2])
    ylimLower = float(sys.argv[3])
    ylimUpper = float(sys.argv[4])
    WIDTH = int(sys.argv[5])
    HEIGHT = int(sys.argv[6])
    fname = sys.argv[7]
    numThreads = int(sys.argv[8])
    
    print("Array initialized")
    
    # Obtain image bounds for each thread
    splitPoints = splitImage(numThreads, WIDTH, HEIGHT)
    print(splitPoints)
    print("Thread split indices obtained")
    
    # Set desired function here
    desiredFunction = burningship

    r = Parallel(n_jobs=numThreads, verbose=0,)(
        delayed(imgThread)(
            desiredFunction,
            rowTuple[0],
            rowTuple[1],
            WIDTH,
            HEIGHT,
        )
        for rowTuple in splitPoints
    )
    startRow, endRow, imgSection = zip(*r)
    imgMatrix = np.concatenate(imgSection)
    print("Working ...")
    finalImage = Image.fromarray(imgMatrix, mode="HSV")
    finalImage.convert("RGB").save(fname, "PNG")
