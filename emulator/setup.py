from setuptools import find_packages, setup

setup(
    name="slothpu",
    version="0.0.1",
    url="https://github.com/freesurfer-rge/slothpu",
    packages=find_packages(),
    install_requires=["bitarray", "urwid"],
)
