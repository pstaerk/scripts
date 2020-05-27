import numpy as np
import matplotlib.pyplot as plt

def main():
    """Render a image from the mandelbrot cpp for testing.
    """
    pic = np.empty((2*500, 2*1000))
    with open('./Myfile2.txt') as f:
        for i, l in enumerate(f):
            pic[:, i] = l.split(';')[:-1]
    plt.matshow(pic, cmap=plt.get_cmap('cividis'))
    plt.show()

if __name__ == "__main__":
    main()
