import openmc
import openmc.deplete
import openmc_depletion_plotter
import matplotlib.pyplot as plt


# a minimal material is needed to pass to the model
material = openmc.Material()
material.add_nuclide("Fe59", 1)
material.volume = 100
material.depletable = True
materials = openmc.Materials([material])

# a minimal model is needed to pass to the operator
model = openmc.Model()
model.materials = materials

# a minimal operator is needed to pass to the integrator
operator = openmc.deplete.Operator(
    model=model, chain_file="chain-nndc-b7.1.xml", normalization_mode="source-rate"
)


timesteps_and_source_rates = [
    (21600, 5e19),  # 6 hour small pulse
    (60 * 60 * 24, 0),  # one day of cooling
    (21600, 5e19),  # 6 hour small pulse
    (60 * 60 * 24, 0),  # one day of cooling
    (10800, 1e20),  # 3 hour big pulse
    (60 * 60 * 24 * 2, 0),  # two days of cooling
    (10800, 1e20),  # 3 hour big pulse
    (60 * 60 * 12, 0),  # half day of cooling
    (60 * 60 * 12, 0),  # half day of cooling
    (60 * 60 * 12, 0),  # half day of cooling
    (60 * 60 * 12, 0),  # half day of cooling
    (60 * 60 * 24, 0),  # one day of cooling
    (60 * 60 * 24, 0),  # one day of cooling
    (60 * 60 * 24, 0),  # one day of cooling
    (60 * 60 * 24, 0),  # one day of cooling
]

integrator = openmc.deplete.PredictorIntegrator(
    operator=operator,
    timesteps=[item[0] for item in timesteps_and_source_rates],
    source_rates=[item[1] for item in timesteps_and_source_rates],
)

integrator.plot_pulse_schedule()
plt.savefig("pulse_single_shot.png")
plt.show()
