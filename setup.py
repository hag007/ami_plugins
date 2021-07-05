from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()


setup(
    name='ami_plugins_hagai',
    version="0.1",
    author="Hagai Levi",
    author_email="hagai.levi.007@gmail.com",
    description='AMI plugins',
    url='https://github.com/hag007/AMI_plugins',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    packages = find_packages(),
    package_data={'': ['*']},
    include_package_data=True,
    install_requires=[
        'networkx==2.4',
        'numpy==1.18.1',
        'scipy==1.4.1',
        'pandas==1.0.1',
        'statsmodels==0.11.0',
        'goatools==0.9.9'],
    entry_points = {
        "console_scripts": [
            "go_enrichment=src.runner:main"
        ]
    }

)
