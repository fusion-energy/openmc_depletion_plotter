import xml.etree.ElementTree as ET
from pathlib import Path
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import openmc
import streamlit as st
from matplotlib import colors
from pylab import cm, colormaps  # *
import numpy as np

# import dagmc_h5m_file_inspector as di

import openmc_depletion_plotter  # adds extra functions to openmc.Results and other classes


def save_uploadedfile(uploadedfile):
    with open(uploadedfile.name, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"Saved File to {uploadedfile.name}")


def header():
    """This section writes out the page header common to all tabs"""

    st.set_page_config(
        page_title="OpenMC Depletion Plotter",
        page_icon="⚛",
        layout="wide",
    )

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {
                    visibility: hidden;
                    }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.write(
        """
            # OpenMC Depletion Plotter

            ### ⚛ A plotting user interface for OpenMC depletion simulations.

            🐍 Run this app locally with Python ```pip install openmc_depletion_plottter``` then run with ```openmc_depletion_plottter```

            ⚙ Produce MatPlotLib or Plotly plots in batch with the 🐍 [Python API](https://github.com/fusion-energy/openmc_depletion_plottter/tree/master/examples)

            💾 Raise a feature request, report and issue or make a contribution on [GitHub](https://github.com/fusion-energy/openmc_depletion_plottter)

            📧 Email feedback to mail@jshimwell.com

            🔗 This package forms part of a more [comprehensive openmc plotting](https://github.com/fusion-energy/openmc_plot) package where geometry, tallies, slices, etc can be plotted and is hosted on [xsplot.com](https://www.xsplot.com/) .
        """
    )
    st.write("<br>", unsafe_allow_html=True)


def main():
    header()

    
    st.write(
        """
            👉 Carry out an OpenMC depletion simulation to generate ```depletion_results.h5``` file.


        """
            # Not got a h5 file handy, right mouse 🖱️ click and save these links 
            # [ example 1 ](https://fusion-energy.github.io/openmc_depletion_plottter/examples/csg_tokamak/geometry.xml),
            # [ example 2 ](https://fusion-energy.github.io/openmc_depletion_plottter/examples/csg_cylinder_box/geometry.xml)
    )


    depletion_file = st.file_uploader("Upload your depletion results h5 file", type=["h5"])

    my_geometry = None

    if dagmc_file is None and geometry_xml_file is None:
        new_title = '<center><p style="font-family:sans-serif; color:Red; font-size: 30px;">Upload your geometry.xml or DAGMC h5m file</p></center>'
        st.markdown(new_title, unsafe_allow_html=True)

        sub_title = '<center><p> Not got geometry files handy? Download an example <a href="https://raw.githubusercontent.com/fusion-energy/openmc_plot/main/examples/tokamak/geometry.xml" download>geometry.xml</a> or DAGMC h5m file</p></center>'
        st.markdown(sub_title, unsafe_allow_html=True)

    # DAGMC route
    elif dagmc_file is not None and geometry_xml_file is not None:

        save_uploadedfile(dagmc_file)
        save_uploadedfile(geometry_xml_file)

        bound_dag_univ = openmc.DAGMCUniverse(
            filename=dagmc_file.name
        ).bounded_universe()
        my_geometry = openmc.Geometry(root=bound_dag_univ)

        dag_universe = my_geometry.get_dagmc_universe()

        mat_ids = range(0, len(dag_universe.material_names) + 1)
        # mat_names = dag_universe.material_names

        if len(mat_ids) >= 1:
            set_mat_ids = set(mat_ids)
        else:
            set_mat_ids = ()

        # set_cell_ids = set(di.get_volumes_from_h5m(dagmc_file.name))
        set_cell_ids = list(range(1, dag_universe.n_cells + 1))
        set_mat_names = set(dag_universe.material_names)
        all_cell_names = set_cell_ids
        set_cell_names = set(all_cell_names)

    elif dagmc_file is not None and geometry_xml_file is None:

        save_uploadedfile(dagmc_file)

        # make a basic openmc geometry
        bound_dag_univ = openmc.DAGMCUniverse(
            filename=dagmc_file.name
        ).bounded_universe()
        my_geometry = openmc.Geometry(root=bound_dag_univ)

        dag_universe = my_geometry.get_dagmc_universe()

        # find all material names
        mat_ids = range(0, len(dag_universe.material_names) + 1)

        if len(mat_ids) >= 1:
            set_mat_ids = set(mat_ids)
        else:
            set_mat_ids = ()

        # set_cell_ids = set(di.get_volumes_from_h5m(dagmc_file.name))
        set_cell_ids = list(range(1, dag_universe.n_cells + 1))
        set_mat_names = set(dag_universe.material_names)
        all_cell_names = set_cell_ids
        set_cell_names = set(all_cell_names)

    # CSG route
    elif dagmc_file is None and geometry_xml_file is not None:
        save_uploadedfile(geometry_xml_file)

        tree = ET.parse(geometry_xml_file.name)

        root = tree.getroot()
        all_cells = root.findall("cell")
        mat_ids = []

        for cell in all_cells:
            if "material" in cell.keys():
                if cell.get("material") == "void":
                    mat_ids.append(0)
                    print(f"material for cell {cell} is void")
                else:
                    mat_ids.append(int(cell.get("material")))

        if len(mat_ids) >= 1:
            set_mat_ids = set(mat_ids)
        else:
            set_mat_ids = ()

        set_mat_names = set_mat_ids  # can't find material names in CSG with just the geometry xml as we don't have material names

        my_mats = openmc.Materials()
        for mat_id in set_mat_ids:
            new_mat = openmc.Material()
            new_mat.id = mat_id
            new_mat.add_nuclide("He4", 1)
            # adds a single nuclide that is in minimal cross section xml to avoid material failing
            my_mats.append(new_mat)

        my_geometry = openmc.Geometry.from_xml(
            path=geometry_xml_file.name, materials=my_mats
        )
        all_cell_ids = []
        all_cell_names = []
        all_cells = my_geometry.get_all_cells()
        for cell_id, cell in all_cells.items():
            all_cell_ids.append(cell.id)
            all_cell_names.append(cell.name)
        set_cell_ids = set(all_cell_ids)
        set_cell_names = set(all_cell_names)

    if my_geometry:
        print("geometry is set to something so attempting to plot")
        bb = my_geometry.bounding_box

        col1, col2 = st.columns([1, 3])

        view_direction = col1.selectbox(
            label="View direction",
            options=("z", "x", "y"),
            index=0,
            key="geometry_view_direction",
            help="Setting the direction of view automatically sets the horizontal and vertical axis used for the plot.",
        )
        backend = col1.selectbox(
            label="Ploting backend",
            options=("matplotlib", "plotly"),
            index=0,
            key="geometry_ploting_backend",
            help="Create png images with MatPlotLib or HTML plots with Plotly",
        )
        outline = col1.selectbox(
            label="Outline",
            options=("materials", "cells", None),
            index=0,
            key="outline",
            help="Allows an outline to be drawn around the cells or materials, select None for no outline",
        )
        color_by = col1.selectbox(
            label="Color by",
            options=("materials", "cells"),
            index=0,
            key="color_by",
            help="Should the plot be colored by material or by cell",
        )
        plot_left, plot_right = None, None
        plot_bottom, plot_top = None, None
        x_min, x_max = None, None
        y_min, y_max = None, None

        x_index = {"z": 0, "y": 0, "x": 1}[view_direction]
        y_index = {"z": 1, "y": 2, "x": 2}[view_direction]
        slice_index = {"z": 2, "y": 1, "x": 0}[view_direction]

        if np.isinf(bb[0][x_index]) or np.isinf(bb[1][x_index]):
            x_min = col1.number_input(label="minimum vertical axis value", key="x_min")
            x_max = col1.number_input(label="maximum vertical axis value", key="x_max")
        else:
            x_min = float(bb[0][x_index])
            x_max = float(bb[1][x_index])

        # y axis is y values
        if np.isinf(bb[0][y_index]) or np.isinf(bb[1][y_index]):
            y_min = col1.number_input(label="minimum vertical axis value", key="y_min")
            y_max = col1.number_input(label="maximum vertical axis value", key="y_max")
        else:
            y_min = float(bb[0][y_index])
            y_max = float(bb[1][y_index])

        # slice axis is z
        if np.isinf(bb[0][slice_index]) or np.isinf(bb[1][slice_index]):
            slice_min = col1.number_input(label="minimum slice value", key="slice_min")
            slice_max = col1.number_input(label="maximum slice value", key="slice_max")
        else:
            slice_min = float(bb[0][slice_index])
            slice_max = float(bb[1][slice_index])

        if isinstance(x_min, float) and isinstance(x_max, float):
            plot_right, plot_left = col1.slider(
                label="Left and right values for the horizontal axis",
                min_value=x_min,
                max_value=x_max,
                value=(x_min, x_max),
                key="left_right_slider",
                help="Set the lowest visible value and highest visible value on the horizontal axis",
            )

        if isinstance(y_min, float) and isinstance(y_max, float):
            plot_bottom, plot_top = col1.slider(
                label="Bottom and top values for the vertical axis",
                min_value=y_min,
                max_value=y_max,
                value=(y_min, y_max),
                key="bottom_top_slider",
                help="Set the lowest visible value and highest visible value on the vertical axis",
            )
        if isinstance(slice_min, float) and isinstance(slice_max, float):
            slice_value = col1.slider(
                label="Slice value",
                min_value=slice_min,
                max_value=slice_max,
                value=(slice_min + slice_max) / 2,
                key="slice_slider",
                help="Set the value of the slice axis",
            )

        pixels_across = col1.number_input(
            label="Number of horizontal pixels",
            value=500,
            help="Increasing this value increases the image resolution but also requires longer to create the image",
        )

        selected_color_map = col1.selectbox(
            label="Color map", options=colormaps(), index=82
        )  # index 81 is tab20c

        if color_by == "materials":

            cmap = cm.get_cmap(selected_color_map, len(set_mat_ids))
            initial_hex_color = []
            for i in range(cmap.N):
                rgba = cmap(i)
                # rgb2hex accepts rgb or rgba
                initial_hex_color.append(colors.rgb2hex(rgba))

            for c, id in enumerate(set_mat_ids):
                # todo add
                st.color_picker(
                    f"Color of material with id {id}",
                    key=f"mat_{id}",
                    value=initial_hex_color[c],
                )

            my_colors = {}
            for id in set_mat_ids:
                hex_color = st.session_state[f"mat_{id}"].lstrip("#")
                RGB = tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))
                my_colors[id] = RGB

        elif color_by == "cells":
            cmap = cm.get_cmap(selected_color_map, len(set_cell_ids))
            initial_hex_color = []
            for i in range(cmap.N):
                rgba = cmap(i)
                # rgb2hex accepts rgb or rgba
                initial_hex_color.append(colors.rgb2hex(rgba))

            for c, (cell_id, cell_name) in enumerate(zip(set_cell_ids, all_cell_names)):
                if cell_name in ["", None]:
                    cell_name = "not set"
                st.color_picker(
                    f"Color of cell id {cell_id}, cell name {cell_name}",
                    key=f"cell_{cell_id}",
                    value=initial_hex_color[c],
                )

            my_colors = {0: (1, 1, 1)}  # adding entry for void cells
            for id in set_cell_ids:
                hex_color = st.session_state[f"cell_{id}"].lstrip("#")
                RGB = tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))
                my_colors[id] = RGB

        title = col1.text_input(
            "Plot title",
            help="Optionally set your own title for the plot",
            value=f"Slice through OpenMC geometry with view direction {view_direction}",
        )

        if (
            isinstance(plot_left, float)
            and isinstance(plot_right, float)
            and isinstance(plot_top, float)
            and isinstance(plot_bottom, float)
        ):
            if color_by == "cells":
                color_data_slice = my_geometry.get_slice_of_cell_ids(
                    view_direction=view_direction,
                    plot_left=plot_left,
                    plot_right=plot_right,
                    plot_top=plot_top,
                    plot_bottom=plot_bottom,
                    pixels_across=pixels_across,
                    slice_value=slice_value,
                )
            elif color_by == "materials":
                color_data_slice = my_geometry.get_slice_of_material_ids(
                    view_direction=view_direction,
                    plot_left=plot_left,
                    plot_right=plot_right,
                    plot_top=plot_top,
                    plot_bottom=plot_bottom,
                    pixels_across=pixels_across,
                    slice_value=slice_value,
                )

            (xlabel, ylabel) = my_geometry.get_axis_labels(
                view_direction=view_direction
            )
            if outline is not None:
                # gets unique levels for outlines contour plot
                # this can be avoided if outline is the same as the color data
                if outline == color_by:
                    outline_data_slice = color_data_slice
                elif outline == "cells":
                    outline_data_slice = my_geometry.get_slice_of_cell_ids(
                        view_direction=view_direction,
                        plot_left=plot_left,
                        plot_right=plot_right,
                        plot_top=plot_top,
                        plot_bottom=plot_bottom,
                        pixels_across=pixels_across,
                        slice_value=slice_value,
                    )
                elif outline == "materials":
                    outline_data_slice = my_geometry.get_slice_of_material_ids(
                        view_direction=view_direction,
                        plot_left=plot_left,
                        plot_right=plot_right,
                        plot_top=plot_top,
                        plot_bottom=plot_bottom,
                        pixels_across=pixels_across,
                        slice_value=slice_value,
                    )
                else:
                    raise ValueError(
                        f"outline can only be cells or materials, not {outline}"
                    )

            if backend == "matplotlib":

                extent = my_geometry.get_plot_extent(
                    plot_left,
                    plot_right,
                    plot_bottom,
                    plot_top,
                    slice_value,
                    bb,
                    view_direction,
                )[
                    :-1
                ]  # slice value is returned in the function so removing with -1

                bounds = list(my_colors.keys())
                color_values = list(my_colors.values())

                mat_cmap = colors.ListedColormap(color_values)
                # our material ids are set to be 1 and 2. void space is 0
                # this +1 is needed as the bounds must be larger that the value to include the values
                bounds.append(bounds[-1] + 1)

                mat_norm = colors.BoundaryNorm(bounds, mat_cmap.N)

                plt.imshow(
                    color_data_slice,
                    extent=extent,
                    interpolation="none",
                    norm=mat_norm,  # needed for colors
                    cmap=mat_cmap,  # needed for colors
                )

                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                plt.title(title)

                if outline is not None:
                    levels = np.unique(
                        [item for sublist in outline_data_slice for item in sublist]
                    )
                    plt.contour(
                        outline_data_slice,
                        origin="upper",
                        colors="k",
                        linestyles="solid",
                        levels=levels,
                        linewidths=0.5,
                        extent=extent,
                    )

                plt.savefig("openmc_plot_geometry_image.png")
                col2.pyplot(plt)
                # col2.image("openmc_plot_geometry_image.png", use_column_width="always")

                with open("openmc_plot_geometry_image.png", "rb") as file:
                    col1.download_button(
                        label="Download image",
                        data=file,
                        file_name="openmc_plot_geometry_image.png",
                        mime="image/png",
                    )
            else:

                data = [
                    go.Heatmap(
                        z=color_data_slice,
                        showscale=False,
                        colorscale="viridis",
                        x0=plot_left,
                        dx=abs(plot_left - plot_right) / (len(color_data_slice[0]) - 1),
                        y0=plot_bottom,
                        dy=abs(plot_bottom - plot_top) / (len(color_data_slice) - 1),
                        # colorbar=dict(title=dict(side="right", text=cbar_label)),
                        # text = material_ids,
                        # hovertemplate=
                        # # 'material ID = %{z}<br>'+
                        # "Cell ID = %{z}<br>" +
                        # # '<br>%{text}<br>'+
                        # xlabel[:2].title()
                        # + ": %{x} cm<br>"
                        # + ylabel[:2].title()
                        # + ": %{y} cm<br>",
                    )
                ]

                if outline is not None:

                    data.append(
                        go.Contour(
                            z=outline_data_slice,
                            x0=plot_left,
                            dx=abs(plot_left - plot_right)
                            / (len(outline_data_slice[0]) - 1),
                            y0=plot_bottom,
                            dy=abs(plot_bottom - plot_top)
                            / (len(outline_data_slice) - 1),
                            contours_coloring="lines",
                            line_width=1,
                            colorscale=[[0, "rgb(0, 0, 0)"], [1.0, "rgb(0, 0, 0)"]],
                            showscale=False,
                        )
                    )

                plot = go.Figure(data=data)

                plot.update_layout(
                    xaxis={"title": xlabel},
                    # reversed autorange is required to avoid image needing rotation/flipping in plotly
                    yaxis={"title": ylabel, "autorange": "reversed"},
                    title=title,
                    autosize=False,
                    height=800,
                )
                plot.update_yaxes(
                    scaleanchor="x",
                    scaleratio=1,
                )

                plot.write_html("openmc_plot_geometry_image.html")

                with open("openmc_plot_geometry_image.html", "rb") as file:
                    col1.download_button(
                        label="Download image",
                        data=file,
                        file_name="openmc_plot_geometry_image.html",
                        mime=None,
                    )
                col2.plotly_chart(plot, use_container_width=True)

            col2.write("Model info")
            col2.write(f"Material IDS found {set_mat_ids}")
            col2.write(f"Material names found {set_mat_names}")
            col2.write(f"Cell IDS found {set_cell_ids}")
            col2.write(f"Cell names found {set_cell_names}")
            col2.write(
                f"Bounding box lower left x={bb[0][0]} y={bb[0][1]} z={bb[0][2]}"
            )
            col2.write(
                f"Bounding box upper right x={bb[1][0]} y={bb[1][1]} z={bb[1][2]}"
            )


if __name__ == "__main__":
    main()
