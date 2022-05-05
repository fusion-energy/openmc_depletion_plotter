from pydoc import visiblename
import openmc
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import pint
ureg = pint.UnitRegistry()

# PTS_PER_INCH = 72

# w, h = 800, 900
# DPI = 100
# w_in, h_in = w / DPI, h / DPI





ATOMIC_SYMBOL = {0: ' ', 1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C',
                 7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al',
                 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K',
                 20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn',
                 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga',
                 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb',
                 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc',
                 44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In',
                 50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs',
                 56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm',
                 62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho',
                 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta',
                 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au',
                 80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At',
                 86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa',
                 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk',
                 98: 'Cf', 99: 'Es', 100: 'Fm', 101: 'Md', 102: 'No',
                 103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh',
                 108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg', 112: 'Cn',
                 113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts',
                 118: 'Og'}



def get_marker_size(ax, nx, ny):
    """Determine the appropriate marker size (in points-squared) for ax."""

    # Get Axes width and height in pixels.
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    # Spacing between scatter point centres along the narrowest dimension.
    spacing = min(width, height) * PTS_PER_INCH / min(nx, ny)
    # Desired radius of scatter points.
    rref =  spacing / 2 * 0.5
    # Initial scatter point size (area) in pt^2.
    s = np.pi * rref**2
    return s

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.1e}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


def get_atoms_from_material(material):

    if material.volume is None:
        msg = 'material.volume must be set to find the number of atoms present.'
        raise ValueError(msg)

    # in units of atom / ( barn cm2 )
    atoms_per_barn_cm2 = my_mat.get_nuclide_atom_densities()
    volume = my_mat.volume *  ureg.cm ** 3

    # print(atoms_per_barn_cm2)
    isotopes_and_atoms = []
    for key, value in atoms_per_barn_cm2.items():
        # print(key, value[1])
        atoms_per_b_cm = value[1] * ureg.particle / (ureg.barn *  ureg.cm)
        atoms = atoms_per_b_cm * volume
        # print(key, atoms)
        # print(key, atoms.to(ureg.particle))

        atomic_number, mass_number, _ = openmc.data.zam(key)

        isotopes_and_atoms.append((atomic_number,mass_number-atomic_number, atoms.to(ureg.particle).magnitude, key))


    # print(atoms_per_barn_cm2)
    return isotopes_and_atoms

def build_grid_of_nuclides(iterable_of_nuclides):


    # number_of_protons_in_axis = 10
    # number_of_neutrons_in_axis = 8

    # neutrons = range(number_of_neutrons_in_axis)
    # proton = range(number_of_protons_in_axis)

    grid_width = 100  # protons
    grid_height = 100  # neutrons
    grid = np.array([[0]*grid_width]*grid_height, dtype=float)


    for atomic_number, neutron_number, atoms, _ in iterable_of_nuclides:
        # print(atomic_number,neutron_number,atoms )
        grid[atomic_number][neutron_number] = atoms

    return grid

def build_grid_of_stable_nuclides(iterable_of_nuclides):

    # number_of_protons_in_axis = 10
    # number_of_neutrons_in_axis = 8

    # neutrons = range(number_of_neutrons_in_axis)
    # proton = range(number_of_protons_in_axis)

    grid_width = 100  # protons
    grid_height = 100  # neutrons
    grid = np.array([[0]*grid_width]*grid_height, dtype=float)


    for atomic_number, neutron_number in iterable_of_nuclides:
        # print(atomic_number,neutron_number,atoms )
        grid[atomic_number][neutron_number] = 1

    return grid

def build_grid_of_annotations(iterable_of_nuclides):


    # number_of_protons_in_axis = 10
    # number_of_neutrons_in_axis = 8

    # neutrons = range(number_of_neutrons_in_axis)
    # proton = range(number_of_protons_in_axis)

    grid_width = 100  # protons
    grid_height = 100  # neutrons
    grid = np.array([[0]*grid_width]*grid_height, dtype=str)

    for atomic_number, neutron_number, atoms, name in iterable_of_nuclides:
        grid[atomic_number][neutron_number] = name

    return grid


my_mat = openmc.Material()
my_mat.add_element('Fe', 1)
my_mat.add_element('Li', 0.5)
my_mat.set_density('g/cm3', 7.7)
my_mat.volume = 1

nuclides=get_atoms_from_material(my_mat)
grid = build_grid_of_nuclides(nuclides)
annots = build_grid_of_annotations(nuclides)
stable_grid = build_grid_of_stable_nuclides([(1,1),(10,10)])



import seaborn as sns
sns.set_theme()
# sns.set_style("whitegrid")
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
# sns.set_style("white")

# masked_array = np.ma.array (grid, mask=np.zeros(grid))
data_masked = np.ma.masked_where(grid != 0, grid)
# plt.imshow(data_masked, interpolation = 'none', vmin = 0)

import matplotlib.cm as cm
# Get the colormap and set the under and bad colors
# colMap = cm.gist_rainbow
def make_cm():
    colMap = cm.get_cmap('viridis', 256)
    colMap.set_bad(color='white')
    colMap.set_under(color='white')
    return colMap

ax = sns.heatmap(grid,
    linewidths=.1,
    vmin=2.204575507634703e+20,
    vmax=7.173000749202642e+22,
    square=True,
    cmap=make_cm(),
    cbar_kws={'label': 'number of atoms'},
    # annot=True,
    # interpolation = 'none',
    # mask=data_masked
)

ax2 = sns.heatmap(stable_grid,
    square=True,
    cmap=make_cm(),
    cbar_kws={'label': 'number of atoms'},
    # annot=True,
    # interpolation = 'none',
    # mask=data_masked
)

plt.gca().set_facecolor("white")
plt.gca().invert_yaxis()

grid_width = 40  # neutrons
grid_height = 30  # protons
ax.set_xlim(0,grid_width)
ax.set_ylim(0,grid_height)

ax.set_title("Number of atoms in material")
ax.set_ylabel("Number of protons")
ax.set_xlabel("Number of neutrons")
ax.grid(True)
# ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')



counter = 0
for j in range(grid.shape[1]):
    for i in range(grid.shape[0]):
        # print(i,j, grid[i, j])
        # text = ax.text(j, i, isotope_chart[i, j],

        if grid[i, j] > 0:

            text = ax.text(
                j+0.5,
                i+0.66,
                f'{ATOMIC_SYMBOL[j]}{i+j}',
                ha="center",
                va="center",
                color="w",
                fontdict={'size':6}
            )
            text = ax.text(
                j+0.5,
                i+0.33,
                f'{grid[i, j]:.1e}',
                ha="center",
                va="center",
                color="w",
                fontdict={'size':5}
            )
        counter = counter +1

plt.savefig('nuclide-halflifes.png', dpi=200)
# plt.show()




# print(grid)
# input()
# stables=['H1','H2','He3','He4','Li6','Li7','Be9','B10','B11','C12','C13','C14','N14','N15','O16','F19','Ne20','Ne21','Ne22','Na23','Mg24','Mg25','Mg26','Al27','Si28','Si29','Si30','P31','S32','S33','S34','S36','Cl35','Cl37','Ar36','Ar38','Ar40','K39','K40','K41','Ca40','Ca42','Ca43','Ca44','Ca46','Ca48','Sc45','Ti46','Ti47','Ti48','Ti49','Ti50','V50','V51','Cr50','Cr52','Cr53','Cr54','Mn55','Fe54','Fe56','Fe57','Fe58','Co59','Ni58','Ni60','Ni61','Ni62','Ni64','Cu63','Cu65','Zn64','Zn66','Zn67','Zn68','Zn70','Ga69','Ga71','Ge70','Ge72','Ge73','Ge74','Ge76','As75','Se74','Se76','Se77','Se78','Se80','Se82','Br79','Br81','Kr78','Kr80','Kr82','Kr83','Kr84','Kr86','Rb85','Rb87','Sr84','Sr86','Sr87','Sr88','Y89','Zr90','Zr91','Zr92','Zr94','Zr96','Nb93','Mo92','Mo94','Mo95','Mo96','Mo97','Mo98','Mo100','Ru96','Ru98','Ru99','Ru100','Ru101','Ru102','Ru104','Rh103','Pd102','Pd104','Pd105','Pd106','Pd108','Pd110','Ag107','Ag109','Cd106','Cd108','Cd110','Cd111','Cd112','Cd113','Cd114','Cd116','In113','In115','Sn112','Sn114','Sn115','Sn116','Sn117','Sn118','Sn119','Sn120','Sn122','Sn124','Sb121','Sb123','Te120','Te122','Te123','Te124','Te125','Te126','Te128','Te130','I127','Xe124','Xe126','Xe128','Xe129','Xe130','Xe131','Xe132','Xe134','Xe136','Cs133','Ba130','Ba132','Ba134','Ba135','Ba136','Ba137','Ba138','La138','La139','Ce136','Ce138','Ce140','Ce142','Pr141','Nd142','Nd143','Nd144','Nd145','Nd146','Nd148','Nd150','Sm144','Sm147','Sm148','Sm149','Sm150','Sm152','Sm154','Eu151','Eu153','Gd152','Gd154','Gd155','Gd156','Gd157','Gd158','Gd160','Tb159','Dy156','Dy158','Dy160','Dy161','Dy162','Dy163','Dy164','Ho165','Er162','Er164','Er166','Er167','Er168','Er170','Tm169','Yb168','Yb170','Yb171','Yb172','Yb173','Yb174','Yb176','Lu175','Lu176','Hf174','Hf176','Hf177','Hf178','Hf179','Hf180','Ta180','Ta181','W180','W182','W183','W184','W186','Re185','Re187','Os184','Os186','Os187','Os188','Os189','Os190','Os192','Ir191','Ir193','Pt190','Pt192','Pt194','Pt195','Pt196','Pt198','Au197','Hg196','Hg198','Hg199','Hg200','Hg201','Hg202','Hg204','Tl203','Tl205','Pb204','Pb206','Pb207','Pb208','Bi209','Th232','Pa231','U234','U235','U238']


# x=[lst[1] for lst in nuclides if lst[2] > 0.1]
# y=[lst[0] for lst in nuclides if lst[2] > 0.1]
# data=[lst[2] for lst in nuclides if lst[2] > 0.1]
# # print(x)
# fig, ax = plt.subplots()

# log_thalf = np.log(data)

# cmap = plt.get_cmap('viridis')
# norm = Normalize(vmin=min(data), vmax=max(data))
# colours = cmap(norm(log_thalf))

# s = get_marker_size(ax, 120, 180)
# print(f'marker size {s}')
# # cm = 'RdBu'
# sc1 = ax.scatter(
#     x=x,y=y,data=data, marker='s',s=s
# )
# ax.set_xlim(0,6)
# ax.set_ylim(0,4)

# fig.tight_layout()
# ax.set_aspect('equal')

# for j in range(grid.shape[1]):
#     for i in range(grid.shape[0]):
#         # print(i,j, grid[i, j])
#         # text = ax.text(j, i, isotope_chart[i, j],

#         if grid[i, j] > 0:

#             text = plt.text(j, i, f'{ATOMIC_SYMBOL[j]}{i+j} \n  {grid[i, j]}',
#                         ha="center", va="center", color="b")
        # counter = counter +1



# def on_resize(event):
#     """Callback function on interactive plot window resize."""
#     # Resize the scatter plot markers to keep the plot looking good.
#     s = get_marker_size(ax, maxZ, maxN)
#     sc1.set_sizes([s]*len(Z))
#     # sc2.set_sizes([s]*len(stables))

# cid = fig.canvas.mpl_connect('resize_event', on_resize)


# plt.show()
# plt.savefig('nuclide-halflifes.png', dpi=DPI)










# # Show all ticks and label them with the respective list entries
# ax.set_xticks(np.arange(grid.shape[1]), labels=range(grid.shape[1]))
# ax.set_yticks(np.arange(grid.shape[0]), labels=range(grid.shape[0]))

# # Loop over data dimensions and create text annotations.
# counter= 0
# anotations = []
# for j in range(grid.shape[1]):
#     for i in range(grid.shape[0]):
#         print(i,j, grid[i, j])
#         # text = ax.text(j, i, isotope_chart[i, j],

#         if grid[i, j] > 0:

#             text = ax.text(j, i, f'{ATOMIC_SYMBOL[j]}{i+j} \n\n  {grid[i, j]}',
#                         ha="center", va="center", color="w")
#         counter = counter +1

# # plt.gca().invert_yaxis()




# # trim the axis to desired elements, bounding box
# ax.set_xlim(0,4)

# fig.tight_layout()
# plt.show()
