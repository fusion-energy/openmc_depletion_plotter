import xml.etree.ElementTree as ET
from pathlib import Path
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import openmc
import streamlit as st
from matplotlib import colors
from pylab import cm, colormaps  # *
import numpy as np

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

            🔗 This package forms part of a more [comprehensive openmc plot](https://github.com/fusion-energy/openmc_plot) package where geometry, tallies, slices, etc can be plotted and is hosted on [xsplot.com](https://www.xsplot.com/) .
        """
    )
    st.write("<br>", unsafe_allow_html=True)


def main():
    header()

    st.write(
        """
            👉 Carry out an OpenMC depletion simulation to generate ```depletion_results.h5``` file and ```maerials.xml``` file.

        """
        # Not got a h5 file handy, right mouse 🖱️ click and save these links
        # [ example 1 ](https://fusion-energy.github.io/openmc_depletion_plottter/examples/csg_tokamak/geometry.xml),
        # [ example 2 ](https://fusion-energy.github.io/openmc_depletion_plottter/examples/csg_cylinder_box/geometry.xml)
    )

    depletion_file = st.file_uploader(
        "Select your depletion results h5 file", type=["h5"]
    )
    materials_file = st.file_uploader("Select your materials.xml file", type=["xml"])

    results = None

    if depletion_file is None:
        new_title = '<center><p style="font-family:sans-serif; color:Red; font-size: 30px;">Select your depletion results h5 file</p></center>'
        st.markdown(new_title, unsafe_allow_html=True)
    if materials_file is None:
        new_title = '<center><p style="font-family:sans-serif; color:Red; font-size: 30px;">Select your materials.xml file</p></center>'
        st.markdown(new_title, unsafe_allow_html=True)

    if depletion_file is not None and materials_file is not None:

        save_uploadedfile(depletion_file)
        save_uploadedfile(materials_file)
        results = openmc.deplete.Results.from_hdf5(depletion_file.name)
        all_pristine_mats = openmc.Materials().from_xml(materials_file.name)
        number_of_depleted_materials = results[0].n_mat

    if results:
        print("results is set to something so attempting to plot")

        acitivity_or_atoms = st.sidebar.selectbox(
            label="Plot",
            options=("activity", "number of atoms"),
            index=0,
            key="acitivity_or_atoms",
            help="",
        )
        backend = st.sidebar.selectbox(
            label="Ploting backend",
            options=("matplotlib", "plotly"),
            index=0,
            key="geometry_ploting_backend",
            help="Create png images with MatPlotLib or HTML plots with Plotly",
        )
        time_units = st.sidebar.selectbox(
            label="Time units",
            options=("s", "min", "h", "d", "a"),
            index=0,
            key="time_units",
            help="The time units to use on the Y aixs, seconds minutes, hours, days or years",
        )
        x_scale = st.sidebar.selectbox(
            label="X scale",
            options=("linear", "log"),
            index=0,
            key="x_scale",
            help="The axis scale to use for the X axis",
        )
        y_scale = st.sidebar.selectbox(
            label="Y scale",
            options=("linear", "log"),
            index=0,
            key="y_scale",
            help="The axis scale to use for the Y axis",
        )

        show_top = st.sidebar.number_input(
            value=10,
            label="Show top",
            key="show_top",
            help=f"The maximum number of nuclides to plot starting with the largest {acitivity_or_atoms}",
        )

        if acitivity_or_atoms == "activity":
            activity_units = st.sidebar.selectbox(
                label="Activity units",
                options=("Bq", "Bq/g", "Bq/cm3"),
                index=0,
                key="activity_units",
                help="",
            )
            # todo horizontal_lines

        if number_of_depleted_materials == 1:
            material_index = 0
        elif number_of_depleted_materials > 1:
            material_index = st.sidebar.number_input(
                value=0,
                label="Material index",
                key="material_index",
                help="",
            )
        else:
            raise ValueError("there are no depleted materials in the first time step")
        # bug with threshold as it cuts too much
        # threshold = st.sidebar.number_input(
        #     value=0.,
        #     label="Threshold",
        #     key="threshold",
        #     help="",
        # )

        include_total = st.sidebar.radio(
            "Include total",
            options=(True, False),
            help="Add a line to the plot showing the total (or sum) of all other lines.",
        )
        excluded_material = st.sidebar.radio(
            "Exclude nuclides from undepleted material",
            options=(True, False),
            help="Allows nuclides in the orginal material to be excluded so that the nuclides created during depletion can be clearly shown.",
        )

        if excluded_material:
            material_to_exclude = all_pristine_mats[material_index]
        else:
            material_to_exclude = None

        if acitivity_or_atoms == "activity":
            plot = results.plot_activity_vs_time(
                # todo allow no materials to be excluded
                excluded_material=material_to_exclude,
                time_units=time_units,
                units=activity_units,
                x_scale=x_scale,
                y_scale=y_scale,
                plotting_backend=backend,
                # horizontal_lines # TODO
                # x_axis_title has default
                # title has default
                # horizontal_lines
                show_top=show_top,
                # threshold
                material_index=material_index,
                include_total=include_total,
                path=materials_file.name,
            )
        else:
            plot = results.plot_atoms_vs_time(
                # todo allow no materials to be excluded
                excluded_material=material_to_exclude,
                time_units=time_units,
                # x_axis_title=f'Time [{time_units}]', this the default already
                # title="Number of of nuclides in material", this is the default
                x_scale=x_scale,
                y_scale=y_scale,
                plotting_backend=backend,
                path=materials_file.name,
                include_total=include_total,
                show_top=show_top,
                material_index=material_index
                # threshold=threshold # looks like there is a bug with threshold
            )

        if backend == "matplotlib":
            st.pyplot(plot)
        else:
            # remove log line selector
            plot.layout["updatemenus"] = []
            st.plotly_chart(plot)


if __name__ == "__main__":
    main()
