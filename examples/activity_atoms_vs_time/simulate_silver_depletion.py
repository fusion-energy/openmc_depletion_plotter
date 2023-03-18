"""Simulates depletion on a geometry with a material to make an output file
that is used by the examples."""

import openmc
import openmc.deplete


model = openmc.Model()

material = openmc.Material()
material.add_element("Ag", 1)
material.set_density("g/cm3", 10.49)
material.volume = 1000.0
material.depletable = True

materials = openmc.Materials([material])
model.materials = materials

# surfaces
sph1 = openmc.Sphere(r=100, boundary_type="vacuum")

# cells, makes a simple sphere cell
shield_cell = openmc.Cell(region=-sph1)
shield_cell.fill = material
# shield_cell.volume = mat_volume

# sets the geometry to the universe that contains just the one cell
universe = openmc.Universe(cells=[shield_cell])
geometry = openmc.Geometry(universe)
model.geometry = geometry

# creates a simple isotropic neutron source in the center with 14MeV neutrons
my_source = openmc.Source()
my_source.space = openmc.stats.Point((0, 0, 0))
my_source.angle = openmc.stats.Isotropic()
my_source.energy = openmc.stats.Discrete([14e6], [1])

# specifies the simulation computational intensity
settings = openmc.Settings()
settings.batches = 2
settings.particles = 10000
settings.inactive = 0
settings.run_mode = "fixed source"
settings.source = my_source

model.settings = settings

# This chain file was made with the run python generate_tendl_chain.py from the openmc-dev/data repo
# this tells openmc the decay paths between isotopes including probabilities of different routes and half lives
chain_filename = "chain-nndc-b7.1.xml"

operator = openmc.deplete.CoupledOperator(
    model=model,
    chain_file=chain_filename,
    normalization_mode="source-rate",
    dilute_initial=0,
    reduce_chain=True,
    reduce_chain_level=5,
)
# Ag110 half life is 24 seconds
# Ag108 halflife is 145 seconds
timesteps_and_source_rates = [
    (24, 1e20),
    (24, 1e20),
    (24, 1e20),
    (24, 1e20),
    (
        24,
        1e20,
    ),  # should saturate Ag110 here as it has been irradiated for over 5 halflives
    (24, 1e20),
    (24, 1e20),
    (24, 1e20),
    (24, 1e20),
    (24, 0),
    (24, 0),
    (24, 0),
    (24, 0),
    (24, 0),
    (24, 0),
    (24, 0),
    (24, 0),
    (24, 0),
    (24, 0),
    (24, 0),
]

integrator = openmc.deplete.PredictorIntegrator(
    operator=operator,
    timesteps=[item[0] for item in timesteps_and_source_rates],
    source_rates=[item[1] for item in timesteps_and_source_rates],
)

# this runs the openmc simulation

integrator.integrate()
