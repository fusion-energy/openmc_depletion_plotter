from typing import Iterable
import openmc

import numpy as np
import openmc
import pint


from openmc.data import ATOMIC_SYMBOL, NATURAL_ABUNDANCE

ureg = pint.UnitRegistry()

def find_most_active_nuclides_in_material(
    material,
    exclude=None,
):

    if exclude is None:
        excluded_isotopes = []
    else:
        if isinstance(exclude, Iterable):
            excluded_isotopes = exclude
        elif isinstance(exclude, openmc.Material):
            excluded_isotopes = exclude.get_nuclides()

    non_excluded_nucs = {}
    for key, value in material.get_nuclide_activity().items():
        if key not in excluded_isotopes:
            if key not in non_excluded_nucs.keys():
                if value != 0.:
                    non_excluded_nucs[key] = value
            else:
                non_excluded_nucs[key] += value

    sorted_dict = {
        k: v
        for k, v in sorted(
            non_excluded_nucs.items(), key=lambda item: item[1], reverse=True
        )
    }
    return list(sorted_dict.keys())



def find_most_active_nuclides_in_materials(
    materials,
    exclude=None,
):
    non_excluded_nucs = {}
    if exclude is None:
        excluded_isotopes = []
    else:
        if isinstance(exclude, Iterable):
            excluded_isotopes = exclude
        elif isinstance(exclude, openmc.Material):
            excluded_isotopes = exclude.get_nuclides()

    for material in materials:
        for key, value in material.get_nuclide_activity().items():
            if key not in excluded_isotopes:
                if key not in non_excluded_nucs.keys():
                    if value != 0.:
                        non_excluded_nucs[key] = value
                else:
                    non_excluded_nucs[key] += value

    sorted_dict = {
        k: v
        for k, v in sorted(
            non_excluded_nucs.items(), key=lambda item: item[1], reverse=True
        )
    }

    return list(sorted_dict.keys())


def find_most_abundant_nuclides_in_material(
    material,
    exclude=None,
):

    if exclude is None:
        excluded_isotopes = []
    else:
        if isinstance(exclude, Iterable):
            excluded_isotopes = exclude
        elif isinstance(exclude, openmc.Material):
            excluded_isotopes = exclude.get_nuclides()
            
    non_excluded_nucs = {}
    for key, value in material.get_nuclide_atom_densities().items():
        if key not in excluded_isotopes:
            if key not in non_excluded_nucs.keys():
                non_excluded_nucs[key] = value
            else:
                non_excluded_nucs[key] += value

    sorted_dict = {
        k: v
        for k, v in sorted(
            non_excluded_nucs.items(), key=lambda item: item[1], reverse=True
        )
    }
    return list(sorted_dict.keys())


def find_most_abundant_nuclides_in_materials(
    materials,
    exclude=None,
):
    non_excluded_nucs = {}
    if exclude is None:
        excluded_isotopes = []
    else:
        if isinstance(exclude, Iterable):
            excluded_isotopes = exclude
        elif isinstance(exclude, openmc.Material):
            excluded_isotopes = exclude.get_nuclides()

    for material in materials:
        for key, value in material.get_nuclide_atom_densities().items():
            if key not in excluded_isotopes:
                if key not in non_excluded_nucs.keys():
                    non_excluded_nucs[key] = value
                else:
                    non_excluded_nucs[key] += value

    sorted_dict = {
        k: v
        for k, v in sorted(
            non_excluded_nucs.items(), key=lambda item: item[1], reverse=True
        )
    }

    return list(sorted_dict.keys())


def get_nuclide_atom_densities_from_materials(nuclides, materials):
    all_nuclides_with_atoms = {}
    for isotope in nuclides:
        all_quants = []
        for material in materials:
            quants = material.get_nuclide_atom_densities()
            if isotope in quants.keys():
                quant = quants[isotope]
            else:
                quant=0.
            all_quants.append(quant)
        all_nuclides_with_atoms[isotope] = all_quants
    return all_nuclides_with_atoms


def get_nuclide_activities_from_materials(nuclides, materials):
    all_nuclides_with_atoms = {}
    for isotope in nuclides:
        all_quants = []
        for material in materials:
            quants = material.get_nuclide_activity()
            if isotope in quants.keys():
                quant = quants[isotope]
            else:
                quant=0.
            all_quants.append(quant)
        all_nuclides_with_atoms[isotope] = all_quants
    return all_nuclides_with_atoms


def get_atoms_from_material(material):

    if material.volume is None:
        msg = "material.volume must be set to find the number of atoms present."
        raise ValueError(msg)

    # in units of atom / ( barn cm2 )
    atoms_per_barn_cm2 = material.get_nuclide_atom_densities()
    volume = material.volume * ureg.cm**3

    # print(atoms_per_barn_cm2)
    isotopes_and_atoms = []
    for key, value in atoms_per_barn_cm2.items():
        # print(key, value[1])
        atoms_per_b_cm = value * ureg.particle / (ureg.barn * ureg.cm)
        atoms = atoms_per_b_cm * volume
        # print(key, atoms)
        # print(key, atoms.to(ureg.particle))

        atomic_number, mass_number, _ = openmc.data.zam(key)

        isotopes_and_atoms.append(
            (
                atomic_number,
                mass_number - atomic_number,
                atoms.to(ureg.particle).magnitude,
                key,
            )
        )

    # print(atoms_per_barn_cm2)
    return isotopes_and_atoms


def build_grid_of_nuclides(iterable_of_nuclides):

    grid_width = 200  # protons
    grid_height = 200  # neutrons
    grid = np.array([[0] * grid_width] * grid_height, dtype=float)

    for atomic_number, neutron_number, atoms, _ in iterable_of_nuclides:
        # print(atomic_number,neutron_number,atoms )
        grid[atomic_number][neutron_number] = atoms

    return grid


def build_grid_of_stable_nuclides(iterable_of_nuclides):

    grid_width = 200  # protons
    grid_height = 200  # neutrons
    grid = np.array([[0] * grid_width] * grid_height, dtype=float)

    for atomic_number, neutron_number in iterable_of_nuclides:
        # print(atomic_number,neutron_number,atoms )
        grid[atomic_number][
            neutron_number
        ] = 0.2  # sets the grey scale from 0 (white) to 1 (black)

    return grid


def build_grid_of_annotations(iterable_of_nuclides):

    grid_width = 200  # protons
    grid_height = 200  # neutrons
    grid = np.array([[0] * grid_width] * grid_height, dtype=str)

    for atomic_number, neutron_number, atoms, name in iterable_of_nuclides:
        grid[atomic_number][neutron_number] = name

    return grid


def get_neutron_range(material):
    nucs = material.get_nuclides()

    neutrons = []
    for nuc in nucs:
        proton, proton_plus_neutron, _ = openmc.data.zam(nuc)
        neutron = proton_plus_neutron - proton
        neutrons.append(neutron)
    return [min(neutrons), max(neutrons)]


def get_proton_range(material):
    nucs = material.get_nuclides()

    protons = []
    for nuc in nucs:
        proton, proton_plus_neutron, _ = openmc.data.zam(nuc)
        protons.append(proton)
    return [min(protons), max(protons)]


# Get the colormap and set the under and bad colors
# colMap = cm.gist_rainbow
def make_unstable_cm():
    colMap = cm.get_cmap("viridis", 256)
    colMap.set_bad(color="white", alpha=100)
    colMap.set_under(color="white", alpha=100)
    return colMap


def make_stable_cm():
    colMap = cm.get_cmap("gray_r", 256)
    colMap.set_bad(color="white", alpha=100)
    colMap.set_under(color="white", alpha=100)
    return colMap