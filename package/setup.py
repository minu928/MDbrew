from setuptools import setup, find_packages

setup(
    name="MDbrew",
    version="2.0.6",
    author="Knu",
    author_email="k1alty@naver.com",
    url="https://github.com/MyKnu/MDbrew",
    download_url="https://github.com/MyKnu/MDbrew/install_file/MDbrew-2.0.6.tar.gz",
    install_requies=[
        "numpy>=1.0.0",
        "pandas>=1.0.0",
        "matplotlib>=1.0.0",
        "tqdm>=1.0.0",
    ],
    description="Postprocessing tools for the MD simulation results (ex. lammps)",
    packages=find_packages(),
    keywords=["MD", "LAMMPS"],
    python_requires=">=3",
    package_data={},
    zip_safe=False,
)
