from openmc_depletion_plotter import plot_materials
import openmc

my_mat = openmc.Material()
my_mat.add_element('Fe', 1)
my_mat.add_element('Li', 0.5)
my_mat.add_element('Be', 0.5)
my_mat.add_element('Al', 0.5)
my_mat.add_element('B', 0.5)
my_mat.add_element('Co', 0.5)
my_mat.set_density('g/cm3', 7.7)
my_mat.volume = 1


my_mat_2 = openmc.Material()
my_mat_2.add_element('Fe', 1)
my_mat_2.add_element('Li', 0.5)
my_mat_2.add_element('C', 0.5)
my_mat_2.add_element('Al', 0.5)
my_mat_2.add_element('Ni', 0.5)
my_mat_2.add_element('Co', 0.5)
my_mat_2.set_density('g/cm3', 7.7)
my_mat_2.volume = 1

plot_materials(
    [my_mat, my_mat_2],
    filenames=['my_mat_1.png', 'my_mat_2.png']
)
