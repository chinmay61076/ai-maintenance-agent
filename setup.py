from setuptools import setup, find_packages

setup(
    name="ai_maintenance_agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'numpy',
        'plotly'
    ]
)
