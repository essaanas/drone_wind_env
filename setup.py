from setuptools import setup, find_packages

setup(
    name="drone_wind_env",
    version="0.1.0",
    description="A custom Gymnasium drone environment with wind disturbance.",
    author="Essa Anas",
    packages=find_packages(),
    install_requires=[
        "gymnasium>=0.29",
        "numpy>=1.24",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
