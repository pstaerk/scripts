import scipy.spatial as sp
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

class Triangulator:
    """Triangulator base on voronoi tesselation."""
    def __init__(self, points, labels):
        """Initialize class by providing the points in 
        phase space, as well as the associated labels.

        :points: assumed to be a iterable of two dimensional tuples
        :labels: strings associated with the points
        """
        self._points = points
        self._labels = labels
        self._vor = None # scipy voronoi object
        self._polygons = None
        self._regions = None
        self._vertices = None
        self._bverts = None # vertices bordering different regions
        self._fvertices = None # vertices for the finite regions
        self.border_verts = None
        self.triangulate(points, labels)

    def triangulate(self, points, labels):
        """Triangulate the voronoi diagram for the specified points.

        """
        self._vor = sp.Voronoi(points)
        self._vertices = self._vor.vertices
        self._regions, self._fvertices = voronoi_finite_polygons_2d(self._vor)
        self._polygons = [self._fvertices[reg] for reg in self._regions]
        self.border_verts = self.calculate_border_verts()

    def calculate_border_verts(self):
        """Calculate the vertices which border differently labelled
        polygons in the tesselation.

        :returns: list of all vertices which border differently
        labelled regions.

        """
        self._bverts = set()
        for j, p in enumerate(self._polygons):
            cur_lab = self._labels[j] # Current label of polygon
            for i, v in enumerate(p):
                occurence = list(map(lambda x: v[0] in  x[:,0] and v[1] in x[:,1],
                    self._polygons))
                occis = [oc for oc in np.argwhere(occurence) if oc != i]
                for oc in occis:
                    if self._labels[oc[0]] != cur_lab:
                        self._bverts.add(tuple(v))
        return self._bverts

    def plot_triangulation(self):
        """Plot the triangulation.

        """
        plot_voronoi_color(self)
        
def plot_voronoi_color(triangulator_obj, aspect=False):
    """Plot a voronoi tesselation with colored regions.

    :triangulator_obj: Triangulator based class.
    :aspect: Set True if aspect ratio should be the same for both axes.

    """
    # sp.voronoi_plot_2d(triangulator_obj._vor)
    fig, ax = plt.subplots()
    for p, l in zip(triangulator_obj._polygons, triangulator_obj._labels):
        cell = Polygon(p, color=l, alpha=.5)
        ax.add_patch(cell)
    # Also plot the exact location of the data points with label
    for p, l in zip(triangulator_obj._points, triangulator_obj._labels):
        plt.plot(p[0], p[1], 'x', color=l)
    # Also plot the bordering vertices:
    for v in triangulator_obj._vertices:
        plt.plot(v[0], v[1], '.')
    # Plot the vertices bordering differently colored areas:
    for v in triangulator_obj.border_verts:
        plt.plot(v[0], v[1], 's')
    if aspect: ax.set_aspect('equal')

# Taken from https://gist.github.com/pv/8036995
def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()*2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)
