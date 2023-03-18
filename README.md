[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI](https://github.com/fusion-energy/openmc_depletion_plotter/actions/workflows/ci.yml/badge.svg)](https://github.com/fusion-energy/openmc_depletion_plotter/actions/workflows/ci.yml)

Extends OpenMC to provides convenient plotting methods.
This is done by Monkey Patching OpenMC to provide additional functionality to the base classes.
One benefit of this is the user can continue to work with the familiar OpenMC classes and they simply get additional functionality.
Another benefit is that if any of these functions ever become popular enough to include in OpenMC then it could be done with a simple copy paste into the existing class structure.
Plotly figures or MatPlotLib figures are returned for user customization.


:point_right: [API Examples](https://github.com/fusion-energy/openmc_depletion_plotter/tree/main/examples)

# Install

The openmc_depletion_plotter package can be installed from PyPi with the terminal command.

```bash
pip install openmc_depletion_plotter
```

# Graphical User Interface

Once installed you can then used the API or launch the GUI.
To launch the GUI type the following command in the terminal and the browser should open with the GUI.

```
openmc_depletion_plotter
```

![openmc depletion plotter](https://user-images.githubusercontent.com/8583900/226143434-0f3d077c-1403-4efe-8318-7fc10ff00fca.gif)

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

![openmc pulse time plot](https://user-images.githubusercontent.com/8583900/188698064-9ffae002-844d-4cdf-aca2-b87d9a8f39b4.png)

# Plotting activation or atoms as a function of time

The ```openmc.deplete.Results()``` class has been extended to include a ```plot_atoms_vs_time()``` method and a ```plot_activity_vs_time``` method.

These methods plot atoms or activity as a function of time.
These plots optionally include a breakdown of the dominant nuclides.
Matplotlib or Plotly backends are available.

Additional methods provided

```python
openmc.deplete.Results.plot_atoms_vs_time()
openmc.deplete.Results.plot_activity_vs_time()
```

![openmc matplotlib activity](https://user-images.githubusercontent.com/8583900/188697525-a156c538-1d67-4efe-b19d-f34850af8b1f.png)
![openmc plotly activity](https://user-images.githubusercontent.com/8583900/188697666-13f4ed29-3293-44f7-99d2-7eabf48d54cb.png)

# Plotting activation or atoms on an isotope chart

The ```openmc.Material()``` class has been extended to include a ```plot_isotope_chart_of_activity()``` method and  ```plot_isotope_chart_of_atoms()``` method.

This method plots the material atoms or the material activity on an isotope chart.

I started making isotope plots back in 2010 so nice to finally distribute this :smile:

Additional methods provided

```python
openmc.Material.plot_isotope_chart_of_atoms()
openmc.Material.plot_isotope_chart_of_activity()
```
![openmc plotly activity](https://user-images.githubusercontent.com/8583900/188697852-962e47d2-4f41-4449-abb1-7cc0b39996e0.png)
