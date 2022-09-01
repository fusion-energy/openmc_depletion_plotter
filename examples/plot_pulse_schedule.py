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


# arbitrary lists provided here, but this would be defined by the the pulse schedule (maintenance, waste, single shot)
source_rates = [1e21] + [0] * 24  # single pulse followed by 0 neutrons
time_steps = [1] + [3600] * 24  # one second followed by 1 hour periods for 24 hours

integrator = openmc.deplete.PredictorIntegrator(
    operator=operator,
    timesteps=time_steps,
    source_rates=source_rates,
    timestep_units="d",
)
integrator.plot_pulse_schedule()
plt.savefig("pulse_single_shot.png")
plt.show()
