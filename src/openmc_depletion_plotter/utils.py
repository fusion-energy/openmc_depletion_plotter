# from turtle import color
from typing import Iterable

import numpy as np
import openmc
import pint
import plotly.graph_objects as go
from openmc.data import ATOMIC_SYMBOL, NATURAL_ABUNDANCE

stable_nuclides = list(NATURAL_ABUNDANCE.keys())


ureg = pint.UnitRegistry()


def add_scale_buttons(figure, x_scale, y_scale):
    if x_scale == "log":
        not_x_scale = "lin"
    else:
        not_x_scale = "log"

    if y_scale == "log":
        not_y_scale = "lin"
    else:
        not_y_scale = "log"
    buttons_list = []
    for xscale in [x_scale, not_x_scale]:
        for yscale in [y_scale, not_y_scale]:
            buttons_list.append(
                {
                    "args": [
                        {
                            "xaxis.type": xscale,
                            "yaxis.type": yscale,
                        }
                    ],
                    "label": f"{xscale}(x) , {yscale}(y)",
                    "method": "relayout",
                }
            )

    # this adds the dropdown box for log and lin axis selection
    figure.update_layout(
        updatemenus=[
            go.layout.Updatemenu(
                buttons=buttons_list,
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.5,
                xanchor="left",
                y=1.1,
                yanchor="top",
            ),
        ]
    )
    return figure


def create_base_plot(x_title, y_title, title="", x_scale="linear", y_scale="linear"):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        xaxis={"title": x_title, "type": x_scale},
        yaxis={
            "title": y_title,
            "type": y_scale,
            "exponentformat": "e",
        },
    )
    return fig


def add_key(fig, key_name="Stable nuclides", color="lightgrey"):

    fig.add_trace(
        go.Scatter(
            x=[-10],  #
            y=[-10],
            mode="markers",
            name=key_name,
            line={"color": color},
            marker_symbol="square",
            marker={"size": 30},
        )
    )
    return fig


def add_stables(fig):

    for stable in stable_nuclides:
        atomic_number, mass_number, _ = openmc.data.zam(stable)
        y = atomic_number
        x = mass_number - y
        fig.add_shape(
            x0=x - 0.5,
            x1=x + 0.5,
            y0=y + 0.5,
            y1=y - 0.5,
            xref="x",
            yref="y",
            fillcolor="lightgrey",
            line_color="lightgrey",
            # opacity=0.5
        )

    return fig


def update_axis_range_partial_chart(fig, y_vals, x_vals):
    fig.update(layout_yaxis_range=[0, max(y_vals) + 1])
    fig.update(layout_xaxis_range=[0, max(x_vals) + 1])

    height = max(y_vals) + 1
    width = max(x_vals) + 1
    ratio = height / width
    return ratio


def update_axis_range_full_chart(fig):

    fig.update(layout_yaxis_range=[0, 93])
    fig.update(layout_xaxis_range=[0, 147])

    height = 93
    width = 147
    ratio = height / width
    return ratio


def find_most_active_nuclides_in_material(
    units,
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
    for key, value in material.get_activity(by_nuclide=True, units=units).items():
        if key not in excluded_isotopes:
            if key not in non_excluded_nucs.keys():
                if value != 0.0:
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
    units,
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

        activities = material.get_activity(by_nuclide=True, units=units).items()

        for key, value in activities:
            if key not in excluded_isotopes:
                if key not in non_excluded_nucs.keys():
                    if value != 0.0:
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


def find_total_activity_in_materials(
    units,
    materials,
    exclude=None,
):

    if exclude is None:
        excluded_isotopes = []
    else:
        if isinstance(exclude, Iterable):
            excluded_isotopes = exclude
        elif isinstance(exclude, openmc.Material):
            excluded_isotopes = exclude.get_nuclides()

    materials_activities = []
    for material in materials:
        material_activity = 0
        activities = material.get_activity(by_nuclide=True, units=units)

        for key, value in activities.items():
            if key not in excluded_isotopes:
                material_activity += value

        materials_activities.append(material_activity)

    return materials_activities


def find_total_decay_heat_in_materials(
    units,
    materials,
    exclude=None,
):

    if exclude is None:
        excluded_isotopes = []
    else:
        if isinstance(exclude, Iterable):
            excluded_isotopes = exclude
        elif isinstance(exclude, openmc.Material):
            excluded_isotopes = exclude.get_nuclides()

    materials_decay_heat = []
    for material in materials:
        material_activity = 0
        heat = material.get_decay_heat(by_nuclide=True, units=units)

        for key, value in heat.items():
            if key not in excluded_isotopes:
                material_activity += value

        materials_decay_heat.append(material_activity)

    return materials_decay_heat


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
    # get_nuclide_atom_densities does not need volume and can be used instead
    # of get_nuclide_atoms here as have a single material
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


def find_total_nuclides_in_materials(
    materials,
    exclude=None,
):

    if exclude is None:
        excluded_isotopes = []
    else:
        if isinstance(exclude, Iterable):
            excluded_isotopes = exclude
        elif isinstance(exclude, openmc.Material):
            excluded_isotopes = exclude.get_nuclides()

    materials_atom_densities = []

    for material in materials:
        material_atom_densities = 0
        for key, value in material.get_nuclide_atoms().items():
            if key not in excluded_isotopes:
                material_atom_densities += value
        materials_atom_densities.append(material_atom_densities)

    return materials_atom_densities


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
        for key, value in material.get_nuclide_atoms().items():
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


def get_decay_heat_from_materials(nuclides, materials, units):
    all_nuclides_with_decay_heat = {}
    for isotope in nuclides:
        all_quants = []
        for material in materials:
            quants = material.get_decay_heat(
                units=units,
                by_nuclide=True
            )
            if isotope in quants.keys():
                quant = quants[isotope]
            else:
                quant = 0.0
            all_quants.append(quant)
        all_nuclides_with_decay_heat[isotope] = all_quants
    return all_nuclides_with_decay_heat


def get_nuclide_atoms_from_materials(nuclides, materials):
    all_nuclides_with_atoms = {}
    for isotope in nuclides:
        all_quants = []
        for material in materials:
            quants = material.get_nuclide_atoms()
            if isotope in quants.keys():
                quant = quants[isotope]
            else:
                quant = 0.0
            all_quants.append(quant)
        all_nuclides_with_atoms[isotope] = all_quants
    return all_nuclides_with_atoms


def get_nuclide_activities_from_materials(nuclides, materials, units):
    all_nuclides_with_atoms = {}
    for isotope in nuclides:
        all_quants = []
        for material in materials:
            quants = material.get_activity(
                by_nuclide=True,  # units in Bq
                units=units
            )
            if isotope in quants.keys():
                quant = quants[isotope]
            else:
                quant = 0.0
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

    isotopes_and_atoms = []
    for key, value in atoms_per_barn_cm2.items():
        atoms_per_b_cm = value * ureg.particle / (ureg.barn * ureg.cm)
        atoms = atoms_per_b_cm * volume

        atomic_number, mass_number, _ = openmc.data.zam(key)

        isotopes_and_atoms.append(
            (
                atomic_number,
                mass_number - atomic_number,
                atoms.to(ureg.particle).magnitude,
                key,
            )
        )

    return isotopes_and_atoms


def get_atoms_activity_from_material(material: openmc.Material, units="Bq"):

    if units == "Bq" and material.volume is None:
        msg = "material.volume must be set to find the activity."
        raise ValueError(msg)

    isotopes_and_activity = material.get_activity(by_nuclide=True, units=units)
    isotopes_and_atoms = []
    for key, activity in isotopes_and_activity.items():

        atomic_number, mass_number, _ = openmc.data.zam(key)

        isotopes_and_atoms.append(
            (
                atomic_number,
                mass_number - atomic_number,
                activity,
                key,
            )
        )

    return isotopes_and_atoms


def build_grid_of_nuclides(iterable_of_nuclides):

    grid_width = 200  # protons
    grid_height = 200  # neutrons
    grid = np.array([[0] * grid_width] * grid_height, dtype=float)

    for atomic_number, neutron_number, atoms, _ in iterable_of_nuclides:
        grid[atomic_number][neutron_number] = atoms

    return grid


def build_grid_of_stable_nuclides(iterable_of_nuclides):

    grid_width = 200  # protons
    grid_height = 200  # neutrons
    grid = np.array([[0] * grid_width] * grid_height, dtype=float)

    for atomic_number, neutron_number in iterable_of_nuclides:
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
