from openmc_depletion_plotter import plot_materials
import openmc

my_mat = openmc.Material()
my_mat.add_element('Fe', 1)
my_mat.add_element('Li', 0.5)
my_mat.add_element('Be', 0.5)
my_mat.add_element('Al', 0.5)
my_mat.add_element('B', 0.5)
my_mat.add_element('Bi', 0.5)
my_mat.add_element('Co', 0.5)
my_mat.set_density('g/cm3', 7.7)
my_mat.volume = 1

plot_materials(my_mat)
