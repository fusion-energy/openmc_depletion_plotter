from openmc_depletion_plotter import find_most_abundant_nuclides_in_material
from openmc_depletion_plotter import find_most_abundant_nuclides_in_materials
from openmc_depletion_plotter import find_most_active_nuclides_in_material
from openmc_depletion_plotter import find_most_active_nuclides_in_materials
from openmc_depletion_plotter import get_nuclide_atom_densities_from_materials
import openmc


def test_find_nuclides_iron():

    my_mat = openmc.Material()
    my_mat.add_element("Fe", 1)

    nucs = find_most_abundant_nuclides_in_material(material=my_mat)

    assert nucs == ["Fe56", "Fe54", "Fe57", "Fe58"]


def test_find_nuclides_lithium():

    my_mat = openmc.Material()
    my_mat.add_element("Li", 1)

    nucs = find_most_abundant_nuclides_in_material(material=my_mat)

    assert nucs == ["Li7", "Li6"]


def test_find_nuclides_lithium_enriched():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Li6", 1)
    my_mat.add_nuclide("Li7", 0.5)

    nucs = find_most_abundant_nuclides_in_material(material=my_mat)

    assert nucs == ["Li6", "Li7"]


def test_find_nuclides_iron_single_exclusion():

    my_mat = openmc.Material()
    my_mat.add_element("Fe", 1)

    nucs = find_most_abundant_nuclides_in_material(material=my_mat, exclude=["Fe56"])

    assert nucs == ["Fe54", "Fe57", "Fe58"]


def test_find_nuclides_iron_multiple_exclusion():

    my_mat = openmc.Material()
    my_mat.add_element("Fe", 1)

    nucs = find_most_abundant_nuclides_in_material(
        material=my_mat, exclude=["Fe56", "Fe57"]
    )

    assert nucs == ["Fe54", "Fe58"]


def test_two_identical_materials():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Li6", 1)
    my_mat.add_nuclide("Li7", 0.5)

    my_mat_2 = openmc.Material()
    my_mat_2.add_nuclide("Li6", 1)
    my_mat_2.add_nuclide("Li7", 0.5)

    nucs = find_most_abundant_nuclides_in_materials(
        materials=[my_mat, my_mat_2],
    )

    assert nucs == ["Li6", "Li7"]


def test_two_similar_materials():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Li6", 0.5)
    my_mat.add_nuclide("Li7", 0.5)

    my_mat_2 = openmc.Material()
    my_mat_2.add_nuclide("Li6", 0.6)
    my_mat_2.add_nuclide("Li7", 0.7)

    nucs = find_most_abundant_nuclides_in_materials(
        materials=[my_mat, my_mat_2],
    )

    assert nucs == ["Li7", "Li6"]


def test_openmc_material():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Li6", 0.5)
    my_mat.add_nuclide("Li7", 0.5)

    my_mat_2 = openmc.Material()
    my_mat_2.add_nuclide("Fe56", 0.6)
    my_mat_2.add_nuclide("Be9", 0.6)

    nucs = find_most_abundant_nuclides_in_materials(
        materials=[my_mat, my_mat_2], exclude=my_mat
    )

    assert nucs == ["Fe56", "Be9"]


def test_openmc_material_shared_isotope():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Li6", 0.5)
    my_mat.add_nuclide("Li7", 0.5)

    my_mat_2 = openmc.Material()
    my_mat_2.add_nuclide("Fe56", 0.6)
    my_mat_2.add_nuclide("Li7", 0.6)

    nucs = find_most_abundant_nuclides_in_materials(
        materials=[my_mat, my_mat_2], exclude=my_mat
    )

    assert nucs == ["Fe56"]


def test_get_nuclide_atom_densities_from_materials():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Li6", 0.5)
    my_mat.add_nuclide("Li7", 0.5)

    my_mat_2 = openmc.Material()
    my_mat_2.add_nuclide("Fe56", 0.6)
    my_mat_2.add_nuclide("Li7", 0.6)

    nucs = get_nuclide_atom_densities_from_materials(
        nuclides=["Li6", "Fe56"], materials=[my_mat, my_mat_2]
    )

    assert list(nucs.keys()) == ["Li6", "Fe56"]

    # first material
    assert isinstance(nucs["Li6"][0], float)
    assert isinstance(nucs["Fe56"][0], float)

    # second material
    assert isinstance(nucs["Li6"][1], float)
    assert isinstance(nucs["Fe56"][1], float)


def test_find_most_active_nuclides_in_material():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Li6", 0.5)
    my_mat.add_nuclide("Li7", 0.5)
    my_mat.add_nuclide("U236", 0.5)  # unstable
    my_mat.volume = 1

    assert find_most_active_nuclides_in_material(material=my_mat, units="Bq") == [
        "U236"
    ]
    assert find_most_active_nuclides_in_material(material=my_mat, units="Bq/g") == [
        "U236"
    ]


def test_find_most_active_nuclides_in_materials():

    my_mat = openmc.Material()
    my_mat.add_nuclide("Li6", 0.5)
    my_mat.add_nuclide("Li7", 0.5)
    my_mat.add_nuclide("U236", 0.5)  # unstable
    my_mat.volume = 1

    my_mat2 = openmc.Material()
    my_mat2.add_nuclide("Li6", 0.5)
    my_mat2.add_nuclide("Li7", 0.5)
    my_mat2.add_nuclide("U238", 0.5)  # unstable
    my_mat2.volume = 1

    assert find_most_active_nuclides_in_materials(
        materials=[my_mat, my_mat2], units="Bq"
    ) == ["U236", "U238"]
    assert find_most_active_nuclides_in_materials(
        materials=[my_mat, my_mat2], units="Bq/g"
    ) == ["U236", "U238"]
