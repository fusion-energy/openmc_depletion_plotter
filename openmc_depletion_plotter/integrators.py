
import openmc
import openmc.deplete

from openmc.deplete.results import _get_time_as


import copy
from itertools import repeat

from openmc.deplete.abc import Integrator, SIIntegrator, OperatorResult, add_params
from openmc.deplete._matrix_funcs import (
    cf4_f1, cf4_f2, cf4_f3, cf4_f4, celi_f1, celi_f2,
    leqi_f1, leqi_f2, leqi_f3, leqi_f4, rk4_f1, rk4_f4
)

__all__ = [
    "PredictorIntegrator", "CECMIntegrator", "CF4Integrator",
    "CELIIntegrator", "EPCRK4Integrator", "LEQIIntegrator",
    "SICELIIntegrator", "SILEQIIntegrator"]


@add_params
class IntegratorWithPlotting(openmc.deplete.abc.Integrator):
    r"""Extends the openmc.deplete Integrator to add a plot method which plots
    the pulse schedule.
    """
    _num_stages = 1

    def __call__(self, conc, rates, dt, source_rate, _i=None):
        """Perform the integration across one time step

        Parameters
        ----------
        conc : numpy.ndarray
            Initial concentrations for all nuclides in [atom]
        rates : openmc.deplete.ReactionRates
            Reaction rates from operator
        dt : float
            Time in [s] for the entire depletion interval
        source_rate : float
            Power in [W] or source rate in [neutron/sec]
        _i : int or None
            Iteration index. Not used

        Returns
        -------
        proc_time : float
            Time spent in CRAM routines for all materials in [s]
        conc_list : list of numpy.ndarray
            Concentrations at end of interval
        op_results : empty list
            Kept for consistency with API. No intermediate calls to
            operator with predictor

        """
        proc_time, conc_end = self._timed_deplete(conc, rates, dt)
        return proc_time, [conc_end], []

    def plot(self, timestep_units: str = 's'):
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

        fig, axes = plt.subplots(2, 1,  gridspec_kw={'height_ratios': [3, 1]})

        # adds space between the plots to avoid overlapping x label
        fig.subplots_adjust(hspace=.4)

        axes[0].set_ylabel('Neutron source rate [n/s]')
        axes[0].set_xlabel(f'Time [{timestep_units}]')
        axes[0].stairs(self.source_rates, linear_time_steps, linewidth=2)

        for timestep in linear_time_steps:
            x_vals = [timestep, timestep]
            y_vals = [0, 1]  # arbitrary heights selected as axis has no y scale
            axes[1].plot(x_vals, y_vals, '-', color='red')

        axes[1].set_xlabel(f'Timesteps [{timestep_units}]')
        axes[1].set_ylim(0, 1)
        axes[1].get_yaxis().set_visible(False)

        return fig
