import numpy as np
import matplotlib.pyplot as plt
import click

@click.command()
@click.option('-i', default='Render0.out')
def render_file(i):
    """Render a image from the mandelbrot cpp for testing.
    """
    pic = np.empty((2*500, 2*1000))
    with open(i) as f:
        for i, l in enumerate(f):
            pic[:, i] = l.split(';')[:-1]
    plt.matshow(pic, cmap=plt.get_cmap('cividis'))
    plt.show()

def main():
    """Main code.

    """
    render_file()

if __name__ == "__main__":
    main()
