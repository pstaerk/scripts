# scripts
Small collection of simple scripts that are too small for a single repository.

## Fractal Noise
Simple fractal noise generator.
Wrote this to see if I could write something like it in a short amount of time.

## Mandelbrot
A simple mandelbrot renderer written in cpp.
Code is parallelized to allow for faster rendering.
Supports zooming.

## Voronoi sampling
This is useful for creating phase space representations, e.g. from simulation data.
The phase space is interpolated using voronoi tesselation, and colored according to the respective phases one wants to highlight.
The script also automatically identifies points which might be chosen to refine the phase space.
E.g. one might start additional simulations at those points.

## Vim-Zettel
Using the [vim-zettel](https://github.com/michal-h21/vim-zettel) plugin makes it possible to use the [Zettelkasten mehtod](https://en.wikipedia.org/wiki/Zettelkasten) for notetaking.
Using markdown is the best option in my opinion, but that requires to use pandoc for the html conversion.
This (super hacked together) script folder in this repository enables one to convert the vimwiki syntax into html with correct styling and options.
