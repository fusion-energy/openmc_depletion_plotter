import openmc
import openmc.deplete
import openmc_depletion_plotter


results = openmc.deplete.Results.from_hdf5("depletion_results.h5")

# the original simulate irradiated Silver (Ag)
# We don't want to include the stable Silver nuclides in the plot
# this makes a material from Silver so that it can be excluded from plots
my_unirradiated_material = openmc.Material()
my_unirradiated_material.add_element("Ag", 1)

# plots the atoms (nuclides) as a function of time
plot = results.plot_atoms_vs_time(
    excluded_material=my_unirradiated_material, time_units="s"
)
plot.show()

# plots the atoms activity in Bq/g as a function of time
plot = results.plot_activity_vs_time(
    excluded_material=my_unirradiated_material, time_units="s"
)
plot.show()
