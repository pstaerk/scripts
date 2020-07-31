# scripts
Small collection of simple scripts that are too small for a single repository.

## Mandelbrot
A simple mandelbrot renderer written in cpp.
Code is parallelized to allow for faster rendering.
Supports zooming.

## Voronoi sampling
This is useful for creating phase space representations, e.g. from simulation data.
The phase space is interpolated using voronoi tesselation, and colored according to the respective phases one wants to highlight.
The script also automatically identifies points which might be chosen to refine the phase space.
E.g. one might start additional simulations at those points.
