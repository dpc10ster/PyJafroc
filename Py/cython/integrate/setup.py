from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Integrate app',
    ext_modules = cythonize("integrate_cy.pyx"),
    zip_safe=False,
)