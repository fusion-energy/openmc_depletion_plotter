"""Simulates depletion on a geometry with a material to make an output file
that is used by the examples."""

import openmc
import openmc.deplete


model = openmc.Model()

material = openmc.Material()
elements_up_to_plutonium = [
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
]
for element in elements_up_to_plutonium:
    material.add_element(element, 1)
material.add_element("U", 100)

material.set_density("g/cm3", 10)
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
my_source.energy = openmc.stats.Discrete([2.5e6], [1])

# specifies the simulation computational intensity
settings = openmc.Settings()
settings.batches = 2
settings.particles = 100000
settings.inactive = 0
settings.run_mode = "fixed source"
settings.source = my_source

model.settings = settings

# This chain file was made with the run python generate_tendl_chain.py from the openmc-dev/data repo
# this tells openmc the decay paths between isotopes including probabilities of different routes and half lives
chain_filename = "chain-nndc-b7.1.xml"
openmc.deplete.Chain.from_xml(chain_filename)

operator = openmc.deplete.Operator(
    model=model,
    chain_file=chain_filename,
    normalization_mode="source-rate",
    # dilute_initial=0,
    # reduce_chain=True,
    # reduce_chain_level=5,
)

# a single pulse of neutrons
integrator = openmc.deplete.PredictorIntegrator(
    operator=operator,
    timesteps=[1],
    timestep_units="a",
    source_rates=[1e22],
)

# this runs the openmc simulation
integrator.integrate()
