from PIL import Image, ImageDraw
import sys
import cmath

Image.MAX_IMAGE_PIXELS = None


# Max iterations for graph
MAX_ITER = 100

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
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


if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python3 julia_set.py xlimL xlimU ylimL ylimU WIDTH HEIGHT filename")
        exit()
    xlimLower = float(sys.argv[1])
    xlimUpper = float(sys.argv[2])
    ylimLower = float(sys.argv[3])
    ylimUpper = float(sys.argv[4])
    WIDTH     = int(sys.argv[5])
    HEIGHT    = int(sys.argv[6])
    fname = sys.argv[7]

    palette = []


    im = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    print("Working ...")

    pixel_num = WIDTH * HEIGHT
    pixel_cur = 0
    prog = 0

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # Convert pixel coords to complex number
            c = complex(xlimLower + (x / WIDTH) * (xlimUpper - xlimLower),
                        ylimLower + (y / HEIGHT) * (ylimUpper - ylimLower))
            # Compute num of iters
            #m = mandelbrot(c)
            #m = burningship(c)
            m = custom(c)
            # Color depends on number of iters
            hue = int(255 * m / MAX_ITER)
            saturation = 255
            value = 255 if m < MAX_ITER else 0
            # Plot point
            draw.point([x, y], (hue, saturation, value))
            pixel_cur += 1
            if pixel_cur % 1000 == 0:
                prog = pixel_cur / pixel_num
                print("Finished {:.2%}".format(prog), end = "\r")

    if len(sys.argv) == 1:
        im.convert('RGB').save('output.png', 'PNG')
    else:
        im.convert('RGB').save(fname, 'PNG')

