
import matplotlib.pyplot as plt
import numpy as np
import openmc
import pint
import seaborn as sns
# from matplotlib.colors import Normalize
from openmc.data import ATOMIC_SYMBOL, NATURAL_ABUNDANCE
import matplotlib.cm as cm

ureg = pint.UnitRegistry()

stable_nuclides = list(NATURAL_ABUNDANCE.keys())


def get_atoms_from_material(material):

    if material.volume is None:
        msg = 'material.volume must be set to find the number of atoms present.'
        raise ValueError(msg)

    # in units of atom / ( barn cm2 )
    atoms_per_barn_cm2 = material.get_nuclide_atom_densities()
    volume = material.volume *  ureg.cm ** 3

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

def get_neutron_range(material):
    nucs = material.get_nuclides()

    neutrons=[]
    for nuc in nucs:
        proton, proton_plus_neutron, _ = openmc.data.zam(nuc)
        neutron = proton_plus_neutron - proton
        neutrons.append(neutron)
    return [min(neutrons), max(neutrons)]


def get_proton_range(material):
    nucs = material.get_nuclides()

    protons=[]
    for nuc in nucs:
        proton, proton_plus_neutron, _ = openmc.data.zam(nuc)
        protons.append(proton)
    return [min(protons), max(protons)]


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




def plot_material(
    my_mat,
    filename=None,
    neutron_range=None,
    proton_range=None,
    ):

    stable_nuclides_za=[]
    for entry in stable_nuclides:
        atomic_number, mass_number, _ = openmc.data.zam(entry)
        stable_nuclides_za.append((atomic_number,mass_number-atomic_number))
        
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

    if neutron_range is None:
        neutron_range = get_neutron_range(my_mat)
        print('neutron_range', neutron_range)
        neutron_range[0] = max(neutron_range[0]-1,0)
        neutron_range[1] = neutron_range[1]+1+1  # todo remove this extra +1 which is currently needed
        print('neutron_range', neutron_range)
        
    if proton_range is None:
        proton_range = get_proton_range(my_mat)
        print('proton_range', proton_range)
        proton_range[0] = max(proton_range[0]-1,0)
        proton_range[1] = proton_range[1]+1+1  # todo remove this extra +1 which is currently needed
        print('proton_range', proton_range)


    ax.set_xlim(neutron_range[0], neutron_range[1])
    ax.set_ylim(proton_range[0], proton_range[1])
    ax2.set_xlim(neutron_range[0], neutron_range[1])
    ax2.set_ylim(proton_range[0], proton_range[1])

    # ax.set_title("Number of atoms in material")
    ax.set_ylabel("Number of protons")
    ax.set_xlabel("Number of neutrons")
    ax.grid(True)
    # ax.grid(True, which='both')
    # ax.axhline(y=0, color='k')
    # ax.axvline(x=0, color='k')
    # plt.axvline(x=0, color='k')

    # plt.axis('on')
    # ax.axis('on')
    # ax2.axis('on')

    plt.xticks(rotation=0)




    for j in range(grid.shape[1]):
        for i in range(grid.shape[0]):
            # print(i,j, grid[i, j])
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


    plt.axis('on')
    ax.set_axis_on()
    ax2.set_axis_on()
    if filename:
        plt.savefig(filename, dpi=400)
    return plt
    # plt.show()
