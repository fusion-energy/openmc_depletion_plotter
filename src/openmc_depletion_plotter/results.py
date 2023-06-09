import matplotlib.pyplot as plt
import numpy as np
import openmc
import openmc.deplete
import plotly.graph_objects as go

from .utils import (add_scale_buttons, create_base_plot,
                    find_most_abundant_nuclides_in_materials,
                    find_most_active_nuclides_in_materials,
                    find_total_activity_in_materials,
                    find_total_decay_heat_in_materials,
                    find_total_nuclides_in_materials,
                    get_decay_heat_from_materials,
                    get_nuclide_activities_from_materials,
                    get_nuclide_atoms_from_materials, stable_nuclides)

lots_of_nuclides = []
elements = list(openmc.data.ATOMIC_SYMBOL.values())
for el in elements:
    for atomic_num in range(1, 1000):
        lots_of_nuclides.append(f'{el}{atomic_num}')


def plot_activity_vs_time(
    self,
    excluded_material=None,
    time_units="d",
    show_top=None,
    x_scale="linear",
    y_scale="linear",
    title="Activity of nuclides in material",
    x_axis_title=None,  # defaults to time with time units
    horizontal_lines=[],
    plotting_backend="plotly",
    units="Bq/g",
    threshold=None,
    include_total=True,
    material_index=0,  # zero index is first depletable material in problem
    path="materials.xml",
):

    time_steps = self.get_times(time_units=time_units)

    all_materials = []
    for counter, step in enumerate(time_steps):
        materials = self.export_to_materials(nuc_with_data=lots_of_nuclides,burnup_index=counter, path=path)[
            material_index
        ]
        all_materials.append(materials)

    most_active = find_most_active_nuclides_in_materials(
        materials=all_materials, exclude=excluded_material, units=units
    )

    if show_top is not None:
        nuclides = most_active[:show_top]
    else:
        nuclides = most_active

    all_nuclides_with_atoms = get_nuclide_activities_from_materials(
        nuclides=nuclides, materials=all_materials, units=units
    )

    if x_axis_title is None:
        x_axis_title = f"Time [{time_units}]"

    if plotting_backend == "plotly":
        figure = create_base_plot(
            x_title=x_axis_title,
            y_title=f"Activity [{units}]",
            title=title,
            x_scale=x_scale,
            y_scale=y_scale,
        )

        if threshold:
            total = (
                find_total_activity_in_materials(
                    materials=all_materials,
                    units=units,
                    exclude=excluded_material
                ),
            )
            figure.update_layout(yaxis_range=[threshold, max(total)])
        add_scale_buttons(figure, x_scale, y_scale)

    elif plotting_backend == "matplotlib":
        plt.cla
        fig = plt.figure()
        plt.xlabel(x_axis_title)
        plt.ylabel(f"Activity [{units}]")
        plt.title(title)
        plt.yscale(y_scale)
        plt.xscale(x_scale)
    else:
        msg = 'only "plotly" and "matplotlib" plotting_backend are supported. {plotting_backend} is not an option'
        raise ValueError(msg)

    for key, value in all_nuclides_with_atoms.items():

        if plotting_backend == "plotly":
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=time_steps,
                    y=value,
                    name=key,
                    # line=dict(shape="hv", width=0),
                )
            )
        else:
            plt.plot(time_steps, value, label=key)

    if include_total:
        if plotting_backend == "plotly":
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=time_steps,
                    y=find_total_activity_in_materials(
                        materials=all_materials, units=units, exclude=excluded_material
                    ),
                    name="total",
                    line=dict(dash="longdashdot", color="black"),
                )
            )
        else:

            y=find_total_activity_in_materials(
                materials=all_materials, units=units, exclude=excluded_material
            )
            plt.plot(time_steps, y, 'k--', label='total')

    for name, value in horizontal_lines:
        if plotting_backend == "plotly":
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=[time_steps[0], time_steps[-1]],
                    y=[value, value],
                    name=name,
                    line=dict(dash="dot", color="black"),
                )
            )

    if plotting_backend == "plotly":
        return figure
    else:
        plt.legend(bbox_to_anchor=(1.25, 1.0))
        plt.tight_layout()
        return plt


def plot_atoms_vs_time(
    self,
    excluded_material=None,
    time_units="d",
    show_top=None,
    x_scale="linear",
    y_scale="linear",
    include_total=False,
    x_axis_title=None,
    plotting_backend="plotly",
    threshold=None,
    title="Number of nuclides in material",
    material_index=0,  # zero index as one material in problem
    path="materials.xml",
):

    time_steps = self.get_times(time_units=time_units)

    all_materials = []
    for counter, step in enumerate(time_steps):
        materials = self.export_to_materials(nuc_with_data=lots_of_nuclides,burnup_index=counter, path=path)[
            material_index
        ]

        all_materials.append(materials)

    most_abundant = find_most_abundant_nuclides_in_materials(
        materials=all_materials, exclude=excluded_material
    )
    if show_top is not None:
        nuclides = most_abundant[:show_top]
    else:
        nuclides = most_abundant

    all_nuclides_with_atoms = get_nuclide_atoms_from_materials(
        nuclides=nuclides, materials=all_materials
    )

    if x_axis_title is None:
        x_axis_title = f"Time [{time_units}]"
    if plotting_backend == "plotly":

        figure = create_base_plot(
            x_title=x_axis_title,
            y_title=f"Number of atoms",
            title=title,
            x_scale=x_scale,
            y_scale=y_scale,
        )

        if threshold:
            total = (
                find_total_nuclides_in_materials(
                    all_materials, exclude=excluded_material
                ),
            )
            figure.update_layout(yaxis_range=[threshold, max(total)])
        add_scale_buttons(figure, x_scale, y_scale)
    elif plotting_backend == "matplotlib":
        plt.cla
        fig = plt.figure()
        plt.xlabel(x_axis_title)
        plt.ylabel("Number of atoms")
        plt.xscale(x_scale)
        plt.yscale(y_scale)
        plt.title(title)
    else:
        msg = 'only "plotly" and "matplotlib" plotting_backend are supported. {plotting_backend} is not an option'
        raise ValueError(msg)

    for key, value in all_nuclides_with_atoms.items():
        if threshold:
            value = np.array(value)
            value[value < threshold] = np.nan
        if key in stable_nuclides:
            name = key + " stable"
        else:
            name = key
        if plotting_backend == "plotly":
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=time_steps,
                    y=value,
                    name=name,
                    # line=dict(shape="hv", width=0),
                )
            )
        else:
            plt.plot(time_steps, value, label=key)

    if include_total:
        total = find_total_nuclides_in_materials(
            all_materials, exclude=excluded_material
        )
        if plotting_backend == "plotly":
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=time_steps,
                    y=total,
                    name="total",
                    line=dict(dash="longdashdot", color="black"),
                )
            )
        else:

            plt.plot(time_steps, total, 'k--', label='total')

    if plotting_backend == "plotly":
        return figure
    else:
        plt.legend(bbox_to_anchor=(1.25, 1.0))
        plt.tight_layout()
        return plt


def plot_decay_heat_vs_time(
    self,
    excluded_material=None,
    time_units="d",
    show_top=None,
    x_scale="linear",
    y_scale="linear",
    include_total=False,
    x_axis_title=None,
    plotting_backend="plotly",
    units="W/g",
    threshold=None,
    title="Decay heat of nuclides in material",
    material_index=0,  # zero index as one material in problem
    path="materials.xml",
):

    time_steps = self.get_times(time_units=time_units)

    all_materials = []
    for counter, step in enumerate(time_steps):
        materials = self.export_to_materials(nuc_with_data=lots_of_nuclides,burnup_index=counter, path=path)[
            material_index
        ]

        all_materials.append(materials)

    most_abundant = find_most_abundant_nuclides_in_materials(
        materials=all_materials, exclude=excluded_material
    )
    if show_top is not None:
        nuclides = most_abundant[:show_top]
    else:
        nuclides = most_abundant

    all_nuclides_with_decay_heat = get_decay_heat_from_materials(
        nuclides=nuclides, materials=all_materials, units=units
    )

    if x_axis_title is None:
        x_axis_title = f"Time [{time_units}]"
    if plotting_backend == "plotly":

        figure = create_base_plot(
            x_title=x_axis_title,
            y_title=f"Decay heat [{units}]",
            title=title,
            x_scale=x_scale,
            y_scale=y_scale,
        )

        if threshold:
            total = (
                find_total_nuclides_in_materials(
                    all_materials, exclude=excluded_material
                ),
            )
            figure.update_layout(yaxis_range=[threshold, max(total)])
        add_scale_buttons(figure, x_scale, y_scale)
    elif plotting_backend == "matplotlib":
        plt.cla
        fig = plt.figure()
        plt.xlabel(x_axis_title)
        plt.ylabel(f"Decay heat [{units}]")
        plt.xscale(x_scale)
        plt.yscale(y_scale)
        plt.title(title)
    else:
        msg = 'only "plotly" and "matplotlib" plotting_backend are supported. {plotting_backend} is not an option'
        raise ValueError(msg)

    for key, value in all_nuclides_with_decay_heat.items():
        if sum(value) != 0:
            if threshold:
                value = np.array(value)
                value[value < threshold] = np.nan
            if key in stable_nuclides:
                name = key + " stable"
            else:
                name = key
            if plotting_backend == "plotly":
                figure.add_trace(
                    go.Scatter(
                        mode="lines",
                        x=time_steps,
                        y=value,
                        name=name,
                        # line=dict(shape="hv", width=0),
                    )
                )
            else:
                plt.plot(time_steps, value, label=key)

    if include_total:
        total = find_total_decay_heat_in_materials(
            materials=all_materials, units=units, exclude=excluded_material
        )
        if plotting_backend == "plotly":
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=time_steps,
                    y=total,
                    name="total",
                    line=dict(dash="longdashdot", color="black"),
                )
            )
        else:
            plt.plot(time_steps, total, 'k--', label='total')

    if plotting_backend == "plotly":
        return figure
    else:
        plt.legend(bbox_to_anchor=(1.25, 1.0))
        plt.tight_layout()
        return plt


openmc.deplete.Results.plot_activity_vs_time = plot_activity_vs_time
openmc.deplete.Results.plot_atoms_vs_time = plot_atoms_vs_time
openmc.deplete.Results.plot_decay_heat_vs_time = plot_decay_heat_vs_time
