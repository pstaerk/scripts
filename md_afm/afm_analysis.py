"""
This file tries to do atomic force microscopy style analysis of
the structures ./ptfe_slab.gro and ./kapton_slab.gro which are
loaded using MDAnalysis.
"""
import MDAnalysis as md
import numpy as np
import matplotlib.pyplot as plt
import tikzplotlib
import pickle
import click

# this function does atomic force microscopy in one direction
def afm_analysis(atom_group, sigma_tip=1., grid_spacing=(100,100), atom_sigma=1.):
    # radius of the afm tip:
    r_tip = sigma_tip/2

    # Create a 2d grid
    x_grid = np.linspace(np.min(atom_group.positions[:,0]),
                         np.max(atom_group.positions[:,0]),
                         grid_spacing[0])
    y_grid = np.linspace(np.min(atom_group.positions[:,1]),
                         np.max(atom_group.positions[:,1]),
                         grid_spacing[1])
    # create the grid
    grid = np.zeros((grid_spacing[0], grid_spacing[1]))

    # Precalculate the tip-particle distance:
    sig_sq = ((sigma_tip+atom_sigma)/2)**2

    # Loop over x, y pairs, and determine the the atoms which fall in the bin of (x, x+1)
    for i, x in enumerate(x_grid):
        for j, y in enumerate(y_grid):
            # determine which atoms are in the bin
            mask_radially = circular_mask(atom_group, x, y, radius=sigma_tip)
            bin_atoms = atom_group[mask_radially]

            # Determine the maximum atom along the z-axis in the bin_atoms
            if len(bin_atoms) > 0:
                # Find out the highest atom in that bin
                # atom_max = bin_atoms[np.argmax(bin_atoms.positions[:,2])]
                candidate = 0 # Update
                for atom in bin_atoms:
                    # Calculate the z-coordinate that the tip would have touching the nearest atom
                    tmp = (ARBITRARY_HEIGHT + sig_sq - (atom.position[0] - x)**2 - \
                            (atom.position[1] - y)**2)**.5 - atom.position[2]
                    if tmp > candidate: candidate = tmp
                # The highest z is the one that the tip would touch
                grid[i, j] = candidate
            else:
                grid[i, j] = np.nan
    # Zero the grid according to its smallest value:
    grid -= np.nanmin(grid)
    return grid

# This function returns a boolean mask for all atoms which are radially within radius
# of the position x, y
def circular_mask(atom_group, x, y, radius=1):
    # calculate the distance of all atoms from the point (x,y)
    dist = np.sqrt((atom_group.positions[:,0]-x)**2 + (atom_group.positions[:,1]-y)**2)
    # return a boolean mask of all atoms within the radius
    return dist < radius
