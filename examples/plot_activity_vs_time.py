import openmc
import openmc.deplete
import openmc_depletion_plotter
from pathlib import Path


output_dir = "/home/jshimwell/activation_example/outputs_Aluminum_maintenance"
results = openmc.deplete.Results.from_hdf5(Path(output_dir) / "depletion_results.h5")

# plot = results.plot_activity_vs_time()
# plot.show()
plot = results.plot_atoms_vs_time()
plot.show()


# def load_data(output_dir, time_units="d"):

#     results = openmc.deplete.Results.from_hdf5(Path(output_dir) / "depletion_results.h5")
#     time_steps = results.get_times(time_units=time_units)

#     unirradiated_material = openmc.Summary(str(Path(output_dir) / "summary.h5")).materials[0]

#     all_materials = []
#     for counter, step in enumerate(time_steps):
#         materials = results.export_to_materials(counter)[
#             0
#         ]  # zero index as one material in problem
#         all_materials.append(materials)
#     openmc_materials = openmc.Materials(all_materials)

#     return openmc_materials, time_steps, unirradiated_material

# openmc_materials, time_steps, unirradiated_material = load_data("/home/jshimwell/activation_example/outputs_Aluminum_maintenance")

# openmc_materials[0].plot_isotope_atom_chart()
