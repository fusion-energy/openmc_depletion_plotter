from openmc_depletion_plotter import plot_material
import openmc

my_mat = openmc.Material()
my_mat.add_element('Fe', 1)
my_mat.add_element('Li', 0.5)
my_mat.add_element('Be', 0.5)
my_mat.add_element('Al', 0.5)
my_mat.add_element('B', 0.5)
my_mat.add_element('Co', 0.5)
my_mat.add_element('Cs', 0.5)
my_mat.add_nuclide('Fe60', 0.1)
my_mat.add_nuclide('Fe61',0.2)
my_mat.add_nuclide('Fe62',0.3)
my_mat.set_density('g/cm3', 7.7)
my_mat.volume = 1

plotly_figure = plot_material(my_mat)

plotly_figure.write_html('my_mat_on_isotope_chart.html')
plotly_figure.write_image('my_mat_on_isotope_chart.png')
plotly_figure.show()