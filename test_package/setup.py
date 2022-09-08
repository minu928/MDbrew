from setuptools import setup, find_packages

setup(
    name="test_MDbrew",
    version="1.1.1",
    author="Knu",
    author_email="k1alty@naver.com",
    url="https://github.com/MyKnu/MDbrew",
    install_requies=[],
    description="Postprocessing tools for the MD simulation results (ex. lammps)",
    packages=find_packages(),
    keywords=["MD", "LAMMPS"],
    python_requires=">=3",
    package_data={},
    zip_safe=False,
)
