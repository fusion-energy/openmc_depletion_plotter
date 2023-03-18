import openmc
from openmc.data import NATURAL_ABUNDANCE
import matplotlib.cm as cm
from .utils import get_atoms_activity_from_material
from .utils import create_base_plot
from .utils import add_stables
from .utils import add_key
from .utils import update_axis_range_partial_chart
from .utils import update_axis_range_full_chart
from .utils import get_atoms_from_material
import plotly.graph_objects as go

stable_nuclides = list(NATURAL_ABUNDANCE.keys())


def plot_isotope_chart_of_atoms(self, show_all=True, title="Numbers of nuclides"):

    xycl = get_atoms_from_material(self)

    y_vals, x_vals, c_vals, l_vals = zip(*xycl)
    
    fig = create_base_plot(title=title, y_title="Protons", x_title="Neutrons")
    fig = add_stables(fig)
    fig = add_key(fig)
    # fig = add_key(fig, key_name='nuclide present in material', color='blue')

    hover_text = []
    for y_val, x_val, c_val, l_val in zip(y_vals, x_vals, c_vals, l_vals):
        hover_text.append(
            f"Nuclide {l_val} <br> Neutrons {x_val} <br> Protons {y_val} <br> Atoms {c_val:.2E}"
        )

    # add scatter points for all the isotopes
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="markers",
            name="material",
            showlegend=False,
            opacity=1,  # makes the scatter invisible
            text=hover_text,
            hoverinfo="text",
            marker=dict(
                color=c_vals,
                colorscale="viridis",
                showscale=True,
                # https://plotly.com/python/reference/#heatmap-colorbar
                colorbar={
                    "title": "Number of nuclides",
                    "len": 0.85,
                    "titleside": "right",
                    "exponentformat": "e",
                },
            ),
        ),
    )

    for entry in xycl:
        y, x, c, l = entry

        color = cm.viridis(c / max(c_vals))[:3]
        scaled_color = (color[0] * 255, color[1] * 255, color[2] * 255)
        text_color = f"rgb{scaled_color}"

        if l in stable_nuclides:
            line_color = "lightgrey"
            line_width = 1
        else:
            line_color = "Black"
            line_width = 1

        fig.add_shape(
            x0=x - 0.5,
            x1=x + 0.5,
            y0=y + 0.5,
            y1=y - 0.5,
            xref="x",
            yref="y",
            fillcolor=text_color,
            line={
                "color": text_color,
                "width": line_width,
                # 'dash':"dashdot",
            },
        )

    if show_all:
        ratio = update_axis_range_full_chart(fig)
    else:
        ratio = update_axis_range_partial_chart(fig, y_vals, x_vals)

    fig.update_layout(
        width=1000,
        height=1000 * ratio,
    )

    return fig


def plot_isotope_chart_of_activity(
    self, show_all=True, title="Activity of nuclides", units="Bq"
):
    xycl = get_atoms_activity_from_material(self, units=units)

    y_vals, x_vals, c_vals, l_vals = zip(*xycl)

    fig = create_base_plot(title=title, y_title="Protons", x_title="Neutrons")
    fig = add_stables(fig)
    fig = add_key(fig)

    hover_text = []
    for y_val, x_val, c_val, l_val in zip(y_vals, x_vals, c_vals, l_vals):
        hover_text.append(
            f"Nuclide {l_val} <br> Neutrons {x_val} <br> Protons {y_val} <br> Activity {c_val:.2E} {units}"
        )

    # add scatter points for all the isotopes
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="markers",
            name="material",
            showlegend=False,
            opacity=1,  # makes the scatter invisible
            text=hover_text,
            hoverinfo="text",
            marker=dict(
                color=c_vals,
                colorscale="viridis",
                showscale=True,
                # https://plotly.com/python/reference/#heatmap-colorbar
                colorbar={
                    "title": f"Activity of nuclides [{units}]",
                    "len": 0.85,
                    "titleside": "right",
                    "exponentformat": "e",
                },
            ),
        ),
    )

    for entry in xycl:
        y, x, c, l = entry
        if c != 0.0:
            color = cm.viridis(c / max(c_vals))[:3]
            scaled_color = (color[0] * 255, color[1] * 255, color[2] * 255)
            text_color = f"rgb{scaled_color}"

            if l in stable_nuclides:
                line_color = "lightgrey"
                line_width = 1
            else:
                line_color = "Black"
                line_width = 1

            fig.add_shape(
                x0=x - 0.5,
                x1=x + 0.5,
                y0=y + 0.5,
                y1=y - 0.5,
                xref="x",
                yref="y",
                fillcolor=text_color,
                line={
                    "color": text_color,
                    "width": line_width,
                },
            )

    if show_all:
        ratio = update_axis_range_full_chart(fig)
    else:
        ratio = update_axis_range_partial_chart(fig, y_vals, x_vals)

    fig.update_layout(
        width=1000,
        height=1000 * ratio,
    )
    return fig


openmc.Material.plot_isotope_chart_of_atoms = plot_isotope_chart_of_atoms
openmc.Material.plot_isotope_chart_of_activity = plot_isotope_chart_of_activity
