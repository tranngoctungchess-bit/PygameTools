from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pgtools",
    version="0.7.0",
    author="Tung",
    author_email="tranngoctung.chess@gmail.com",
    description="Kernel UI layout tools for Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tranngoctungchess-bit/PygameTools",
    packages=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'': ['*.py']},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.0.0",
    ],
)