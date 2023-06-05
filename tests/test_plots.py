import openmc
import openmc_depletion_plotter
import plotly
import openmc.deplete
import math


#TODO plot
# openmc.deplete.PredictorIntegrator plot_pulse_schedule

# openmc.deplete.Results.plot_atoms_vs_time()
# openmc.deplete.Results.plot_activity_vs_time()

def test_default_isotope_charts():
    my_mat = openmc.Material()
    my_mat.add_element("Fe", 1)
    my_mat.add_nuclide("Co60", 1)
    my_mat.set_density('g/cm3', 1)
    my_mat.volume = 1

    plot = my_mat.plot_isotope_chart_of_atoms()
    assert isinstance(plot, plotly.graph_objs._figure.Figure)

    plot = my_mat.plot_isotope_chart_of_activity()
    assert isinstance(plot, plotly.graph_objs._figure.Figure)


def test_default_time_plots():

    # makes a simple material from Silver
    my_material = openmc.Material() 
    my_material.add_element('Ag', 1, percent_type='ao')
    my_material.set_density('g/cm3', 10.49)

    sphere_radius = 100
    volume_of_sphere = (4/3) * math.pi * math.pow(sphere_radius, 3)
    my_material.volume = volume_of_sphere  # a volume is needed so openmc can find the number of atoms in the cell/material
    my_material.depletable = True  # depletable = True is needed to tell openmc to update the material with each time step

    materials = openmc.Materials([my_material])
    materials.export_to_xml()

    # GEOMETRY

    # surfaces
    sph1 = openmc.Sphere(r=sphere_radius, boundary_type='vacuum')

    # cells, makes a simple sphere cell
    shield_cell = openmc.Cell(region=-sph1)
    shield_cell.fill = my_material

    # sets the geometry to the universe that contains just the one cell
    universe = openmc.Universe(cells=[shield_cell])
    geometry = openmc.Geometry(universe)

    # creates a 14MeV neutron point source
    source = openmc.Source()
    source.space = openmc.stats.Point((0, 0, 0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Discrete([14e6], [1])
    source.particles = 'neutron'

    # SETTINGS

    # Instantiate a Settings object
    settings = openmc.Settings()
    settings.batches = 2
    settings.inactive = 0
    settings.particles = 10000
    settings.source = source
    settings.run_mode = 'fixed source'

    model = openmc.model.Model(geometry, materials, settings)

    operator = openmc.deplete.CoupledOperator(
        model=model,
        normalization_mode="source-rate",  # set for fixed source simulation, otherwise defaults to fission simulation
        dilute_initial=0,  # set to zero to avoid adding small amounts of isotopes, defaults to adding small amounts of fissionable isotopes
        reduce_chain=True,  # reduced to only the isotopes present in depletable materials and their possible progeny
        reduce_chain_level=5,
    )

    # We define timesteps together with the source rate to make it clearer
    timesteps_and_source_rates = [
        (24, 1e20),
        (24, 0),
        (24, 0),
    ]

    # Uses list Python comprehension to get the timesteps and source_rates separately
    timesteps = [item[0] for item in timesteps_and_source_rates]
    source_rates = [item[1] for item in timesteps_and_source_rates]

    integrator = openmc.deplete.PredictorIntegrator(
        operator=operator,
        timesteps=timesteps,
        source_rates=source_rates
    )

    integrator.integrate()

    results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")

    plot = results.plot_atoms_vs_time(excluded_material=my_material)
    assert isinstance(plot, plotly.graph_objs._figure.Figure)

    plot = results.plot_activity_vs_time()
    assert isinstance(plot, plotly.graph_objs._figure.Figure)

    plot = results.plot_decay_heat_vs_time()
    assert isinstance(plot, plotly.graph_objs._figure.Figure)
