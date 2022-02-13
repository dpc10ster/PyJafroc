from setuptools import setup
from Cython.Build import cythonize

# update the .pyx filename below
setup(
    name='Compute app',
    ext_modules = cythonize("compute_memview.pyx", annotate=True),
    # annotate=True generates the .html file
    zip_safe=False,
)

# =============================================================================
# Then run: python setup.py build_ext --inplace in the right directory
# or python setup.py build_ext -if   (build inplace and force recompilation)
# =============================================================================
