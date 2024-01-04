from pathlib import Path
from setuptools import setup, find_packages

version_dict = {}
with open(Path(__file__).parents[0] / "mdbrew/__version__.py") as this_v:
    exec(this_v.read(), version_dict)
version = version_dict["__version__"]
del version_dict

setup(
    name="mdbrew",
    version=version,
    author="Knu",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/minu928/mdbrew",
    install_requies=[
        "numpy>=1.19.0",
        "pandas>=2.0.0",
        "matplotlib>=1.0.0",
        "tqdm>=1.0.0",
        "scipy",
    ],
    description="Postprocessing tools for the Molecular Dynamics simulation",
    packages=find_packages(),
    keywords=["MD", "LAMMPS", "GROMACS"],
    python_requires=">=3.8",
    package_data={"": ["*"]},
    zip_safe=False,
)
