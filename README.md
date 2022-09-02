Extends OpenMC to provides convienent plotting methods.
This is done by Monkey Patching OpenMC to provide additional functionality to the base classes.
One benefit of this is the user can continue to work with the familiar OpenMC classes and they simply get additional functionality.
Another benefit is that if any of these functions ever become popular enough to include in OpenMC then it could be done with a simple copy paste into the existing class structure.
Plotly figures or MatPlotLib figures are returned for user customization.

# Plotting pulse schedule

All the Integrator classes have been extended to include a ```.plot_pulse_schedule()``` method.

This method plots the source rate as a function of time.

This is useful when wanting to visually display a pulse schedule used in an depletion / activation study.

Additional methods provided

```python
openmc.deplete.PredictorIntegrator.plot_pulse_schedule()
openmc.deplete.CECMIntegrator.plot_pulse_schedule()
openmc.deplete.CF4Integrator.plot_pulse_schedule()
openmc.deplete.CELIIntegrator.plot_pulse_schedule()
openmc.deplete.EPCRK4Integrator.plot_pulse_schedule()
openmc.deplete.LEQIIntegrator.plot_pulse_schedule()
openmc.deplete.SICELIIntegrator.plot_pulse_schedule()
openmc.deplete.SILEQIIntegrator.plot_pulse_schedule()
```

# Plotting activation or atoms as a function of time

The ```openmc.deplete.Results()``` class has been extended to include a ```plot_atoms_vs_time()``` method and a ```plot_activity_vs_time``` method.

These methods plot atoms or activity as a function of time.
These plots optionally include a breakdown of the dominant nuclides.

Additional methods provided

```python
openmc.deplete.Results.plot_atoms_vs_time()
openmc.deplete.Results.plot_activity_vs_time()
```

# Plotting activation or atoms on an isotope chart

The ```openmc.Material()``` class has been extended to include a ```plot_isotope_chart_of_activity()``` method and  ```plot_isotope_chart_of_atoms()``` method.

This method plots the material atoms or the material activity on an isotope chart.

I started making isotope plots back in 2010 so nice to finally distribute this :smile:

Additional methods provided

```python
openmc.Material.plot_isotope_chart_of_atoms()
openmc.Material.plot_isotope_chart_of_activity()
```
