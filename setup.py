from setuptools import setup, find_packages

setup(
    name='netrackclient',
    version='0.0.1',
    description="Client library for Netrack API",
    packages=find_packages(),
    entry_points = {
        "console_scripts": ["netrack = netrackclient.shell.run:main"],
    },
    zip_safe=False,
)
