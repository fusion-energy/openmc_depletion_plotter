from pydoc import visiblename
import openmc
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from openmc.data import NATURAL_ABUNDANCE, ATOMIC_SYMBOL
import seaborn as sns
import pint

ureg = pint.UnitRegistry()


stable_nuclides = list(NATURAL_ABUNDANCE.keys())



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

    grid_width = 200  # protons
    grid_height = 200  # neutrons
    grid = np.array([[0]*grid_width]*grid_height, dtype=float)


    for atomic_number, neutron_number, atoms, _ in iterable_of_nuclides:
        # print(atomic_number,neutron_number,atoms )
        grid[atomic_number][neutron_number] = atoms

    return grid

def build_grid_of_stable_nuclides(iterable_of_nuclides):


    grid_width = 200  # protons
    grid_height = 200  # neutrons
    grid = np.array([[0]*grid_width]*grid_height, dtype=float)


    for atomic_number, neutron_number in iterable_of_nuclides:
        # print(atomic_number,neutron_number,atoms )
        grid[atomic_number][neutron_number] = 0.2 # sets the grey scale from 0 (white) to 1 (black)

    return grid

def build_grid_of_annotations(iterable_of_nuclides):

    grid_width = 200  # protons
    grid_height = 200  # neutrons
    grid = np.array([[0]*grid_width]*grid_height, dtype=str)

    for atomic_number, neutron_number, atoms, name in iterable_of_nuclides:
        grid[atomic_number][neutron_number] = name

    return grid

stable_nuclides_za=[]
for entry in stable_nuclides:
    atomic_number, mass_number, _ = openmc.data.zam(entry)
    stable_nuclides_za.append((atomic_number,mass_number-atomic_number))

my_mat = openmc.Material()
my_mat.add_element('Fe', 1)
my_mat.add_element('Li', 0.5)
my_mat.add_element('Be', 0.5)
my_mat.add_element('Al', 0.5)
my_mat.add_element('B', 0.5)
my_mat.add_element('Bi', 0.5)
my_mat.add_element('Co', 0.5)
my_mat.set_density('g/cm3', 7.7)
my_mat.volume = 1

nuclides=get_atoms_from_material(my_mat)
grid = build_grid_of_nuclides(nuclides)
annots = build_grid_of_annotations(nuclides)
stable_grid = build_grid_of_stable_nuclides(stable_nuclides_za)




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
def make_unstable_cm():
    colMap = cm.get_cmap('viridis', 256)
    colMap.set_bad(color='white', alpha=100)
    colMap.set_under(color='white', alpha=100)
    return colMap
    
def make_stable_cm():
    colMap = cm.get_cmap('gray_r', 256)
    colMap.set_bad(color='white', alpha=100)
    colMap.set_under(color='white', alpha=100)
    return colMap


ax2 = sns.heatmap(stable_grid,
    square=True,
    cmap=make_stable_cm(),
    cbar=False,
    linewidths=0,
)

ax = sns.heatmap(grid,
    linewidths=.1,
    vmin=2.204575507634703e+20,
    vmax=7.173000749202642e+22,
    square=True,
    cmap=make_unstable_cm(),
    cbar_kws={'label': 'number of atoms'},
    # annot=True,
    # interpolation = 'none',
    # mask=data_masked
)
plt.gca().set_facecolor("white")
plt.gca().invert_yaxis()

grid_width = 40  # neutrons
grid_height = 30  # protons
ax.set_xlim(0, grid_width)
ax.set_ylim(0, grid_height)

ax.set_title("Number of atoms in material")
ax.set_ylabel("Number of protons")
ax.set_xlabel("Number of neutrons")
ax.grid(True)
# ax.grid(True, which='both')
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')


ax2.set_xlim(0, grid_width)
ax2.set_ylim(0, grid_height)



for j in range(grid.shape[1]):
    for i in range(grid.shape[0]):
        print(i,j, grid[i, j])
        # text = ax.text(j, i, isotope_chart[i, j],

        if grid[i, j] > 0:

            text = ax.text(
                j+0.5,
                i+0.66,
                f'{ATOMIC_SYMBOL[i]}{i+j}',
                ha="center",
                va="center",
                color="w",
                fontdict={'size': 3}
            )
            text = ax.text(
                j+0.5,
                i+0.33,
                f'{grid[i, j]:.1e}',
                ha="center",
                va="center",
                color="w",
                fontdict={'size': 2}
            )
        
        if (i, j) in stable_nuclides_za:
            text = ax.text(
                j+0.5,
                i+0.66,
                f'{ATOMIC_SYMBOL[i]}{i+j}',
                ha="center",
                va="center",
                color="w",
                fontdict={'size': 3}
            )


plt.savefig('nuclide-halflifes.png', dpi=200)
# plt.show()
