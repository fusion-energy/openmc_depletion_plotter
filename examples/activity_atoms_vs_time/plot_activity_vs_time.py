import openmc
import openmc.deplete
import openmc_depletion_plotter  # adds plot_atoms_vs_time and plot_activity_vs_time methods to openmc.deplete.Results


results = openmc.deplete.Results.from_hdf5("depletion_results.h5")


# plots the atoms activity in Bq/g as a function of time
plot = results.plot_activity_vs_time(
    time_units="s",
    units="Bq/g",
    plotting_backend="plotly",
)
plot.show()
plot.write_html("activity_vs_time_silver_activation.html")
plot.write_image("activity_vs_time_silver_activation.png")


# plots the atoms activity in Bq/g as a function of time
plot = results.plot_activity_vs_time(
    time_units="s",
    units="Bq/g",
    plotting_backend="matplotlib",
    show_top=2,  # only Ag108 and Ag110 will be shown
)
# plot.show()
plot.savefig("activity_vs_time_silver_activation.png")
