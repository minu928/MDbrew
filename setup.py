from setuptools import setup, find_packages


setup(
    name="mdbrew",
    version="2.4.2",
    author="Knu",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/MyKnu/MDbrew",
    install_requies=[
        "numpy>=1.19.0",
        "pandas>=1.0.0",
        "matplotlib>=1.0.0",
        "tqdm>=1.0.0",
        "scipy",
    ],
    description="Postprocessing tools for the MD simulation results (ex. lammps)",
    packages=find_packages(),
    keywords=["MD", "LAMMPS", "GROMACS"],
    python_requires=">=3.8",
    package_data={"": ["*"]},
    zip_safe=False,
)
