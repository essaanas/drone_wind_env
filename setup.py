from setuptools import setup, find_packages

setup(
    name="drone_wind_env",
    version="0.1.0",
    description="DroneWind Gymnasium environment with per-student variability and wind disturbance.",
    author="Your Name / Organisation",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "gymnasium>=0.29",
        "numpy>=1.24",
    ],
    python_requires=">=3.9",
)
