"""
Setup script for Quantum Snake Mobile
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="quantum-snake-mobile",
    version="1.0.0",
    author="Quantum Snake Developer",
    author_email="developer@quantumsnake.com",
    description="A mobile adaptation of Quantum Snake game with touch controls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quantum-snake-mobile",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "quantum-snake=quantum_snake_mobile.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "quantum_snake_mobile": [
            "resources/sounds/*.wav",
            "resources/fonts/*.ttf",
            "resources/images/*.png",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=5.0.0",
        ],
        "android": [
            "buildozer>=1.5.0",
            "cython>=0.29.0",
        ],
    },
)