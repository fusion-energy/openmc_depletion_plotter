import openmc
import openmc.deplete
import openmc_depletion_plotter  # adds plotting methods to the material class

unirradiated_material = openmc.Material()
unirradiated_material.set_density("g/cm3", 10)
unirradiated_material.volume = 1
elements_up_to_plutonium = [
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
]
for element in elements_up_to_plutonium:
    unirradiated_material.add_element(element, 1)

plotly_figure = unirradiated_material.plot_isotope_chart_of_atoms()
plotly_figure.write_html("fission_material_isotope_chart.html")
plotly_figure.write_image("fission_material_isotope_chart.png")
plotly_figure.show()


results = openmc.deplete.Results.from_hdf5("depletion_results.h5")
irradiated_material = results.export_to_materials(-1)[0]

plotly_figure = irradiated_material.plot_isotope_chart_of_activity()
plotly_figure.write_html("fission_activity_on_isotope_chart.html")
plotly_figure.write_image("fission_activity_on_isotope_chart.png")
plotly_figure.show()

plotly_figure_2 = irradiated_material.plot_isotope_chart_of_atoms()
plotly_figure_2.write_html("fission_atoms_on_isotope_chart.html")
plotly_figure_2.write_image("fission_atoms_on_isotope_chart.png")
plotly_figure_2.show()
