from setuptools import setup, find_packages

setup(
    name="PGTKernelbasic",
    version="0.23.4",
    author="Your Name",
    description="Lightweight UI framework for Pygame",
    packages=find_packages(),
    install_requires=["pygame>=2.5.0", "miniaudio"],
    python_requires=">=3.8",
)