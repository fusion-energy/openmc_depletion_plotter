
import openmc

import matplotlib.cm as cm

import plotly.graph_objects as go

import matplotlib.cm as cm
from .utils import get_atoms_from_material
from .utils import get_atoms_activity_from_material
from .utils import create_base_plot
from .utils import add_stables
from .utils import update_axis_range_partial_chart
from .utils import update_axis_range_full_chart
from .utils import stable_nuclides
from .utils import find_most_abundant_nuclides_in_materials
from .utils import find_most_active_nuclides_in_materials
from .utils import find_total_nuclides_in_materials
from .utils import get_nuclide_atom_densities_from_materials
from .utils import get_nuclide_activities_from_materials
from .utils import get_nuclide_specific_activities_from_materials
from .utils import add_scale_buttons

# from openmc.data import NATURAL_ABUNDANCE

# stable_nuclides = list(NATURAL_ABUNDANCE.keys())

def plot_activity_vs_time(
    materials,
    excluded_material,
    time_steps,
    show_top=None,
    x_scale ='log',
    y_scale='log',
    ):

    most_active = find_most_active_nuclides_in_materials(
        materials=materials,
        exclude=excluded_material
    )

    if show_top is not None:
        nuclides=most_active[:show_top]
    else:
        nuclides=most_active

    all_nuclides_with_atoms = get_nuclide_activities_from_materials(
        nuclides=nuclides,
        materials=materials
    )

    figure = go.Figure()
    figure.update_layout(
        title='Activity of nuclides in material',
        xaxis={"title": "Time [days]", "type": x_scale},
        yaxis={"title": "Activity [Bq]", "type": y_scale},
    )

    add_scale_buttons(figure, x_scale, y_scale)

    for key, value in all_nuclides_with_atoms.items():
        figure.add_trace(
            go.Scatter(
                mode="lines",
                x=time_steps,
                y=value,
                name=key,
                # line=dict(shape="hv", width=0),
            )
        )
    
    return figure

def plot_specific_activity_vs_time(
    materials,
    excluded_material,
    time_steps,
    show_top=None,
    x_scale ='log',
    y_scale='log',
    horizontal_lines = []
    ):

    most_active = find_most_active_nuclides_in_materials(
        materials=materials,
        exclude=excluded_material,
        specific_activity=True
    )

    if show_top is not None:
        nuclides=most_active[:show_top]
    else:
        nuclides=most_active

    all_nuclides_with_atoms = get_nuclide_specific_activities_from_materials(
        nuclides=nuclides,
        materials=materials
    )

    figure = go.Figure()
    figure.update_layout(
        title='Specific activity of nuclides in material',
        xaxis={"title": "Time [days]", "type": x_scale},
        yaxis={"title": "Activity [Bq/g]", "type": y_scale},
    )

    add_scale_buttons(figure, x_scale, y_scale)

    for key, value in all_nuclides_with_atoms.items():
        figure.add_trace(
            go.Scatter(
                mode="lines",
                x=time_steps,
                y=value,
                name=key,
                # line=dict(shape="hv", width=0),
            )
        )

    for name, value in horizontal_lines:
        figure.add_trace(
            go.Scatter(
                mode="lines",
                x=[time_steps[0], time_steps[-1]],
                y=[value, value],
                name=name,
                line=dict(dash='dot', color='black'),
            )
        )
    
    return figure


def plot_atoms_vs_time(
    materials,
    excluded_material,
    time_steps,
    show_top=None,
    x_scale ='log',
    y_scale='log',
    include_total = True
):

    most_abundant = find_most_abundant_nuclides_in_materials(
        materials=materials,
        exclude=excluded_material
    )
    if show_top is not None:
        nuclides=most_abundant[:show_top]
    else:
        nuclides=most_abundant

    all_nuclides_with_atoms = get_nuclide_atom_densities_from_materials(
        nuclides=nuclides,
        materials=materials
    )

    figure = go.Figure()
    figure.update_layout(
        title='Number of of nuclides in material',
        xaxis={"title": "Time [days]", "type": x_scale},
        yaxis={"title": "Number of atoms", "type": y_scale},
    )

    add_scale_buttons(figure, x_scale, y_scale)

    for key, value in all_nuclides_with_atoms.items():
        figure.add_trace(
            go.Scatter(
                mode="lines",
                x=time_steps,
                y=value,
                name=key,
                # line=dict(shape="hv", width=0),
            )
        )

    if include_total:
        figure.add_trace(
            go.Scatter(
                mode="lines",
                x=time_steps,
                y=find_total_nuclides_in_materials(materials, exclude=excluded_material),
                name='total',
            )
        )

    return figure

def plot_isotope_chart_of_activity(
    my_mat,
    show_all=True
):
    xycl = get_atoms_activity_from_material(my_mat)

    y_vals, x_vals, c_vals, l_vals = zip(*xycl)

    fig = create_base_plot(title='Activity of nuclides')
    fig = add_stables(fig)

    for entry in xycl:
        y, x, c, l = entry
        if c != 0.:
            color = cm.viridis(c/max(c_vals))[:3]
            scaled_color = (color[0]*255,color[1]*255,color[2]*255)
            text_color = f'rgb{scaled_color}'

            if l in stable_nuclides:
                line_color = "lightgrey"
                line_width = 1
            else:
                line_color = "Black"
                line_width = 1

            fig.add_shape(
                x0=x-0.5,
                x1=x+0.5,
                y0=y+0.5,
                y1=y-0.5,
                xref='x',
                yref='y',
                fillcolor=text_color,
                # line_color="LightSeaGreen",
                line={
                    'color':line_color,
                    'width':line_width,
                    # 'dash':"dashdot",
                }
            )


    if show_all:
        ratio = update_axis_range_full_chart(fig)
    else:
        ratio = update_axis_range_partial_chart(fig, y_vals, x_vals)

    fig.update_layout(
        # autosize=True
        width=1000,
        height=1000*ratio
        )
    return fig


def plot_isotope_chart_of_atoms(
    my_mat,
    show_all=True
    # neutron_proton_axis=True
    # isotopes_label_size=None,
):

    xycl = get_atoms_from_material(my_mat)

    y_vals, x_vals, c_vals, l_vals = zip(*xycl)

    # add scatter points for all the isotopes
    # fig.add_trace(
    #     go.Scatter(
    #         x=x_vals,
    #         y=y_vals,
    #         mode='markers',
    #         name='material',
    #     )
    # )

    fig = create_base_plot(title='Numbers of nuclides')
    fig = add_stables(fig)

    for entry in xycl:
        y, x, c, l = entry

        color = cm.viridis(c/max(c_vals))[:3]
        scaled_color = (color[0]*255,color[1]*255,color[2]*255)
        text_color = f'rgb{scaled_color}'

        if l in stable_nuclides:
            line_color = "lightgrey"
            line_width = 1
        else:
            line_color = "Black"
            line_width = 1

        fig.add_shape(
            x0=x-0.5,
            x1=x+0.5,
            y0=y+0.5,
            y1=y-0.5,
            xref='x',
            yref='y',
            fillcolor=text_color,
            # line_color="LightSeaGreen",
            line={
                'color':line_color,
                'width':line_width,
                # 'dash':"dashdot",
            }
        )


    if show_all:
        ratio = update_axis_range_full_chart(fig)
    else:
        ratio = update_axis_range_partial_chart(fig, y_vals, x_vals)

    fig.update_layout(
        # autosize=True
        width=1000,
        height=1000*ratio
        )
    return fig
