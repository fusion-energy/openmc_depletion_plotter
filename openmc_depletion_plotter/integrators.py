"""Monkey patches all the openmc Integrator classes to add a plot_pulse_schedule method"""

import openmc
import openmc.deplete

# from openmc.deplete.results import _get_time_as
# import is causing an error
# ImportError: cannot import name '_get_time_as' from 'openmc.deplete.results' (/usr/local/lib/python3.9/dist-packages/openmc/deplete/results.py)
# temporary solution is to include function here
def _get_time_as(seconds, units):
    if units == "d":
        return seconds / (60 * 60 * 24)
    elif units == "h":
        return seconds / (60 * 60)
    elif units == "min":
        return seconds / 60
    else:
        return seconds

def plot_pulse_schedule(self, timestep_units: str = "s"):
    """Plots the source strength as a function of time and the depletion
    timesteps on an adjacent subplot.
    Parameters
    ----------
    timestep_units : {'s', 'min', 'h', 'd', 'a', 'MWd/kg'}
        Units for values specified in the `timesteps` argument. 's' means
        seconds, 'min' means minutes, 'h' means hours, 'a' means Julian
        years and 'MWd/kg' indicates that the values are given in burnup
        (MW-d of energy deposited per kilogram of initial heavy metal).
    Returns
    -------
    matplotlib.figure.Figure
        Resulting image
    """

    import matplotlib.pyplot as plt

    current_time = 0
    linear_time_steps = [0]

    for time_step in self.timesteps:
        current_time += _get_time_as(time_step, timestep_units)
        linear_time_steps.append(current_time)

    fig, axes = plt.subplots(2, 1, gridspec_kw={"height_ratios": [3, 1]})

    # adds space between the plots to avoid overlapping x label
    fig.subplots_adjust(hspace=0.4)

    axes[0].set_ylabel("Neutron source rate [n/s]")
    axes[0].set_xlabel(f"Time [{timestep_units}]")
    axes[0].stairs(self.source_rates, linear_time_steps, linewidth=2)

    for timestep in linear_time_steps:
        x_vals = [timestep, timestep]
        y_vals = [0, 1]  # arbitrary heights selected as axis has no y scale
        axes[1].plot(x_vals, y_vals, "-", color="red")

    axes[1].set_xlabel(f"Timesteps [{timestep_units}]")
    axes[1].set_ylim(0, 1)
    axes[1].get_yaxis().set_visible(False)

    return fig


openmc.deplete.PredictorIntegrator.plot_pulse_schedule = plot_pulse_schedule
openmc.deplete.CECMIntegrator.plot_pulse_schedule = plot_pulse_schedule
openmc.deplete.CF4Integrator.plot_pulse_schedule = plot_pulse_schedule
openmc.deplete.CELIIntegrator.plot_pulse_schedule = plot_pulse_schedule
openmc.deplete.EPCRK4Integrator.plot_pulse_schedule = plot_pulse_schedule
openmc.deplete.LEQIIntegrator.plot_pulse_schedule = plot_pulse_schedule
openmc.deplete.SICELIIntegrator.plot_pulse_schedule = plot_pulse_schedule
openmc.deplete.SILEQIIntegrator.plot_pulse_schedule = plot_pulse_schedule
