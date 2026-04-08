# setup.py
from setuptools import setup, find_packages
import os

# Đọc README.md cho long_description
with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Đọc requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="PGTKernelBasic",  # Tên unique trên PyPi
    version="Build23",          # Match với Build 22 của bạn
    author="Your Name",
    author_email="tranngoctung.chess@gmail.com",
    description="A lightweight Pygame wrapper for Pygame with advance feature",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tranngoctungchess-bit/PygameTools.git",  # GitHub repo
    packages=find_packages(include=['Kernel', 'Kernel.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.5.0",  # Dependency chính
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)