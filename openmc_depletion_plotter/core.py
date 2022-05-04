import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

stables=['H1','H2','He3','He4','Li6','Li7','Be9','B10','B11','C12','C13','C14','N14','N15','O16','F19','Ne20','Ne21','Ne22','Na23','Mg24','Mg25','Mg26','Al27','Si28','Si29','Si30','P31','S32','S33','S34','S36','Cl35','Cl37','Ar36','Ar38','Ar40','K39','K40','K41','Ca40','Ca42','Ca43','Ca44','Ca46','Ca48','Sc45','Ti46','Ti47','Ti48','Ti49','Ti50','V50','V51','Cr50','Cr52','Cr53','Cr54','Mn55','Fe54','Fe56','Fe57','Fe58','Co59','Ni58','Ni60','Ni61','Ni62','Ni64','Cu63','Cu65','Zn64','Zn66','Zn67','Zn68','Zn70','Ga69','Ga71','Ge70','Ge72','Ge73','Ge74','Ge76','As75','Se74','Se76','Se77','Se78','Se80','Se82','Br79','Br81','Kr78','Kr80','Kr82','Kr83','Kr84','Kr86','Rb85','Rb87','Sr84','Sr86','Sr87','Sr88','Y89','Zr90','Zr91','Zr92','Zr94','Zr96','Nb93','Mo92','Mo94','Mo95','Mo96','Mo97','Mo98','Mo100','Ru96','Ru98','Ru99','Ru100','Ru101','Ru102','Ru104','Rh103','Pd102','Pd104','Pd105','Pd106','Pd108','Pd110','Ag107','Ag109','Cd106','Cd108','Cd110','Cd111','Cd112','Cd113','Cd114','Cd116','In113','In115','Sn112','Sn114','Sn115','Sn116','Sn117','Sn118','Sn119','Sn120','Sn122','Sn124','Sb121','Sb123','Te120','Te122','Te123','Te124','Te125','Te126','Te128','Te130','I127','Xe124','Xe126','Xe128','Xe129','Xe130','Xe131','Xe132','Xe134','Xe136','Cs133','Ba130','Ba132','Ba134','Ba135','Ba136','Ba137','Ba138','La138','La139','Ce136','Ce138','Ce140','Ce142','Pr141','Nd142','Nd143','Nd144','Nd145','Nd146','Nd148','Nd150','Sm144','Sm147','Sm148','Sm149','Sm150','Sm152','Sm154','Eu151','Eu153','Gd152','Gd154','Gd155','Gd156','Gd157','Gd158','Gd160','Tb159','Dy156','Dy158','Dy160','Dy161','Dy162','Dy163','Dy164','Ho165','Er162','Er164','Er166','Er167','Er168','Er170','Tm169','Yb168','Yb170','Yb171','Yb172','Yb173','Yb174','Yb176','Lu175','Lu176','Hf174','Hf176','Hf177','Hf178','Hf179','Hf180','Ta180','Ta181','W180','W182','W183','W184','W186','Re185','Re187','Os184','Os186','Os187','Os188','Os189','Os190','Os192','Ir191','Ir193','Pt190','Pt192','Pt194','Pt195','Pt196','Pt198','Au197','Hg196','Hg198','Hg199','Hg200','Hg201','Hg202','Hg204','Tl203','Tl205','Pb204','Pb206','Pb207','Pb208','Bi209','Th232','Pa231','U234','U235','U238']

number_of_protons_in_axis = 10
number_of_neutrons_in_axis = 8

neutrons = range(number_of_neutrons_in_axis)
proton = range(number_of_protons_in_axis)

isotope_chart = np.array([[0]*number_of_protons_in_axis]*number_of_neutrons_in_axis)

# harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
#                     [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
#                     [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
#                     [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
#                     [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
#                     [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
#                     [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])

# neutron 1 , proton 7 has a intensity of 1
isotope_chart[1][7]=1
print(isotope_chart)

fig, ax = plt.subplots()
im = ax.imshow(isotope_chart)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(proton)), labels=proton)
ax.set_yticks(np.arange(len(neutrons)), labels=neutrons)

# Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#          rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for j in range(number_of_protons_in_axis):
    for i in range(number_of_neutrons_in_axis):
        print(i,j, isotope_chart[i, j])
        text = ax.text(j, i, isotope_chart[i, j],
                       ha="center", va="center", color="w")

plt.gca().invert_yaxis()

ax.set_title("Number of atoms in material")
ax.set_xlabel("Number of protons")
ax.set_ylabel("Number of neutrons")

# trim the axis to desired elements, bounding box
# ax1.set_xlim(0,4)

fig.tight_layout()
plt.show()

# get_nuclide_densities()
# get_nuclide_atom_densities()