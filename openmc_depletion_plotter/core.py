
import openmc

import matplotlib.cm as cm

import plotly.graph_objects as go

import matplotlib.cm as cm
from .utils import get_atoms_from_material
from openmc.data import NATURAL_ABUNDANCE

stable_nuclides = list(NATURAL_ABUNDANCE.keys())



def plot_material(
    my_mat,
    show_all=True
    # isotopes_label_size=None,
):

    xycl = get_atoms_from_material(my_mat)

    fig = go.Figure()
    y_vals, x_vals, c_vals, l_vals = zip(*xycl)
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='markers',
            name='material',
        )
    )

    #print(stable_nuclides)
    #print(l_vals)


    for stable in stable_nuclides:
        atomic_number, mass_number, _ = openmc.data.zam(stable)
        y = atomic_number
        x = mass_number - y
        fig.add_shape(
            x0=x-0.5,
            x1=x+0.5,
            y0=y+0.5,
            y1=y-0.5,
            xref='x',
            yref='y',
            fillcolor='lightgrey',
            line_color="lightgrey",
        )

    for entry in xycl:
        y, x, c, l = entry

        color = cm.viridis(c/max(c_vals))[:3]
        scaled_color = (color[0]*255,color[1]*255,color[2]*255)
        text_color = f'rgb{scaled_color}'
        #print(color, text_color)

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

    # fig.update_xaxes(rangemode="tozero")

    if show_all:
        fig.update(layout_yaxis_range = [0, 93])
        fig.update(layout_xaxis_range = [0, 147])

        height = 93
        width = 147
        ratio = height / width

    else:
        fig.update(layout_yaxis_range = [0, max(y_vals)+1])
        fig.update(layout_xaxis_range = [0, max(x_vals)+1])

        height = max(y_vals)+1
        width = max(x_vals)+1
        ratio = height / width

    fig.update_xaxes(title='protons')
    fig.update_yaxes(title='neutrons')
    fig.update_layout(
        # autosize=True
        width=1000,
        height=1000*ratio
        )
    return fig
