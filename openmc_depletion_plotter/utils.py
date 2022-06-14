from typing import Iterable
import openmc


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
                non_excluded_nucs[key] = value[1]
            else:
                non_excluded_nucs[key] += value[1]

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
                    non_excluded_nucs[key] = value[1]
                else:
                    non_excluded_nucs[key] += value[1]

    sorted_dict = {
        k: v
        for k, v in sorted(
            non_excluded_nucs.items(), key=lambda item: item[1], reverse=True
        )
    }

    return list(sorted_dict.keys())
