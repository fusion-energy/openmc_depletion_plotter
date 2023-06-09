
import openmc
import openmc_depletion_plotter
import openmc.deplete
import math
from pathlib import Path

# these should be set to where you have the chain and cross section file saved
openmc.config['cross_sections'] = Path(__file__).parents[2]/'tests'/'cross_sections.xml'
openmc.config['chain_file'] = Path(__file__).parents[2]/'tests'/'chain-nndc-b7.1.xml'

# makes a simple material
my_material = openmc.Material()
my_material.add_nuclide('Fe56', 71.17, percent_type='ao')
my_material.set_density('g/cm3', 7.9)

sphere_radius = 100
volume_of_sphere = (4/3) * math.pi * math.pow(sphere_radius, 3)
my_material.volume = volume_of_sphere  # a volume is needed so openmc can find the number of atoms in the cell/material
my_material.depletable = True  # depletable = True is needed to tell openmc to update the material with each time step

materials = openmc.Materials([my_material])
materials.export_to_xml()

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
    (5*60, 1.116E+10),
    (5*60, 0),
    (5*60, 0),
    (5*60, 0),
]

# Uses list Python comprehension to get the timesteps and source_rates separately
timesteps = [item[0] for item in timesteps_and_source_rates]
source_rates = [item[1] for item in timesteps_and_source_rates]

integrator = openmc.deplete.PredictorIntegrator(
    operator=operator,
    timesteps=timesteps,
    source_rates=source_rates,
    timestep_units='s'
)

integrator.integrate()

results = openmc.deplete.ResultsList.from_hdf5("depletion_results.h5")

plot = results.plot_decay_heat_vs_time(
    x_scale='log',
    y_scale='log',
    excluded_material=my_material,
    show_top=10
)
plot.show()

plot.write_html('decay_heat.html')
