
import openmc

import matplotlib.cm as cm

import plotly.graph_objects as go

import matplotlib.cm as cm
from .utils import get_atoms_from_material, get_atoms_activity_from_material
from .utils import create_base_plot
from .utils import add_stables
from .utils import update_axis_range_partial_chart
from .utils import update_axis_range_full_chart
from .utils import stable_nuclides

# from openmc.data import NATURAL_ABUNDANCE

# stable_nuclides = list(NATURAL_ABUNDANCE.keys())



def plot_material_activity(
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


def plot_material(
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
