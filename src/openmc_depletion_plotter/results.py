import openmc
import openmc.deplete
from .utils import add_scale_buttons
from .utils import find_most_active_nuclides_in_materials
from .utils import get_nuclide_activities_from_materials
from .utils import get_nuclide_activities_from_materials
from .utils import find_total_activity_in_materials
from .utils import stable_nuclides
from .utils import get_nuclide_atom_densities_from_materials
from .utils import find_most_abundant_nuclides_in_materials
from .utils import find_total_nuclides_in_materials
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


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
):

    time_steps = self.get_times(time_units=time_units)

    all_materials = []
    for counter, step in enumerate(time_steps):
        materials = self.export_to_materials(counter)[
            0
        ]  # zero index as one material in problem
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
        figure = go.Figure()
        figure.update_layout(
            title=title,
            xaxis={"title": x_axis_title, "type": x_scale},
            yaxis={
                "title": f"Activity [{units}]",
                "type": y_scale,
                "exponentformat": "e",
            },
        )

        if threshold:
            total = (
                find_total_activity_in_materials(
                    materials=all_materials, units=units, exclude=excluded_material
                ),
            )
            figure.update_layout(yaxis_range=[threshold, max(total)])
        add_scale_buttons(figure, x_scale, y_scale)
    elif plotting_backend == "matplotlib":
        plt.cla
        fig = plt.figure()
        plt.xlabel(x_axis_title)
        plt.ylabel("Number of atoms")
        plt.title(title)
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
            print("include_total not supported for this plotting_backend")

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
        plt.legend(bbox_to_anchor=(1.25, 1.))
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
    title="Number of of nuclides in material",
):

    time_steps = self.get_times(time_units=time_units)

    all_materials = []
    for counter, step in enumerate(time_steps):
        materials = self.export_to_materials(counter)[
            0
        ]  # zero index as one material in problem
        all_materials.append(materials)

    most_abundant = find_most_abundant_nuclides_in_materials(
        materials=all_materials, exclude=excluded_material
    )
    if show_top is not None:
        nuclides = most_abundant[:show_top]
    else:
        nuclides = most_abundant

    all_nuclides_with_atoms = get_nuclide_atom_densities_from_materials(
        nuclides=nuclides, materials=all_materials
    )

    if x_axis_title is None:
        x_axis_title = f"Time [{time_units}]"
    if plotting_backend == "plotly":
        figure = go.Figure()
        figure.update_layout(
            title=title,
            xaxis={"title": x_axis_title, "type": x_scale},
            yaxis={"title": "Number of atoms", "type": y_scale, "exponentformat": "e"},
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
        if plotting_backend == "plotly":
            figure.add_trace(
                go.Scatter(
                    mode="lines",
                    x=time_steps,
                    y=find_total_nuclides_in_materials(
                        all_materials, exclude=excluded_material
                    ),
                    name="total",
                    line=dict(dash="longdashdot", color="black"),
                )
            )
        else:
            print("include_total not supported for this plotting_backend")

    if plotting_backend == "plotly":
        return figure
    else:
        plt.legend(bbox_to_anchor=(1.25, 1.))
        plt.tight_layout()
        return plt


openmc.deplete.Results.plot_activity_vs_time = plot_activity_vs_time
openmc.deplete.Results.plot_atoms_vs_time = plot_atoms_vs_time
