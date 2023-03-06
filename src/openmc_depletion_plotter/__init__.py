try:
    # this works for python 3.7 and lower
    from importlib.metadata import version, PackageNotFoundError
except (ModuleNotFoundError, ImportError):
    # this works for python 3.8 and higher
    from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("openmc_depletion_plotter")
except PackageNotFoundError:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)

__all__ = ["__version__"]

# from .core import plot_isotope_chart_of_atoms
# from .core import plot_isotope_chart_of_activity
# from .core import plot_activity_vs_time
# from .core import plot_specific_activity_vs_time
# from .core import plot_atoms_vs_time
from .utils import get_atoms_activity_from_material
from .utils import find_most_abundant_nuclides_in_material
from .utils import find_most_abundant_nuclides_in_materials
from .utils import get_nuclide_atom_densities_from_materials
from .utils import find_most_active_nuclides_in_material
from .utils import find_most_active_nuclides_in_materials
from .utils import get_nuclide_activities_from_materials
from .utils import get_atoms_from_material
from .utils import create_base_plot
from .utils import add_stables
from .utils import update_axis_range_partial_chart
from .utils import update_axis_range_full_chart
from .utils import add_scale_buttons


from .materials import *
from .integrators import *
from .results import *
