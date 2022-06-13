import openmc

def find_most_abundant_nuclides_in_material(
    material,
    how_many=1,
    exclude=None,
):
    non_excluded_nucs={}
    for key, value in material.get_nuclide_atom_densities().items():
        if exclude:
            if key not in exclude:
                non_excluded_nucs[key] = value[1]
        else:
            non_excluded_nucs[key] =value[1]

    sorted_dict = {k: v for k, v in sorted(non_excluded_nucs.items(), key=lambda item: item[1], reverse=True)}
    return list(sorted_dict.keys())


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

    sorted_dict = {k: v for k, v in sorted(non_excluded_nucs.items(), key=lambda item: item[1], reverse=True)}
    return list(sorted_dict.keys())
