from setuptools import setup, find_packages

setup(
    name="aircraft_maintenance_system",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.32.0",
        "pandas>=2.1.3",
        "numpy>=1.26.2",
        "plotly>=5.18.0",
        "scikit-learn>=1.3.2",
    ],
)