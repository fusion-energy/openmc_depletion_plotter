import openmc

def find_most_abundant_nuclides_in_material(
    material,
    how_many=1,
    exclude=None,
):
    non_excluded_nucs=[]
    for key, value in material.get_nuclide_atom_densities().items():
        if exclude:
            if key not in exclude:
                non_excluded_nucs.append(value)
        else:
            non_excluded_nucs.append(value)

    sorted_nucs = sorted(non_excluded_nucs, key=lambda x: x[1],reverse=True)

    return [y[0] for y in sorted_nucs]


def find_most_abundant_nuclides_in_materials(
    materials,
    how_many=1,
    exclude=None,
):
    non_excluded_nucs={}

    for material in materials:
        for key, value in material.get_nuclide_atom_densities().items():
            if exclude:
                if key not in exclude:
                    if key not in non_excluded_nucs.keys():
                        non_excluded_nucs[key] = value[1]
                    else:
                        non_excluded_nucs[key] += value[1]

            else:
                # print(key, value)
                if key not in non_excluded_nucs.keys():
                    non_excluded_nucs[key] = value[1]
                else:
                    non_excluded_nucs[key] += value[1]
                    # non_excluded_nucs.append(value)

    sorted_nucs = sorted(non_excluded_nucs, key=lambda x: x[1], reverse=True)

    # print(non_excluded_nucs)
    return sorted_nucs

    # return [y[0] for y in sorted_nucs]

# my_mat = openmc.Material()
# my_mat.add_element('Fe', 1)
# my_mat.add_element('Li', 0.5)
# nucs = find_most_abundant_nuclides_in_material(
#         material=my_mat
#     )
# print(nucs)