from setuptools import setup, find_packages

setup(
    name="autoeda-pro",
    version="1.0.0",
    author="Chirag Sharma",
    description="Automated EDA tool that analyzes datasets and scores data quality",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ChiragSharma2026/autoeda-pro",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
        "scikit-learn",
        "streamlit",
    ],
    entry_points={
        "console_scripts": [
            "autoeda=autoeda.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)