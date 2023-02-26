from setuptools import setup
from src import __version__, __author__


def get_file(nm: str) -> list:
    with open(nm) as file:
        return file.readlines()


setup(
    name="smartBetika",
    packages=["smartBetika"],
    version=__version__,
    install_requires=get_file("requirements.txt"),
    url="https://github.com/Simatwa/smartBetika",
    license="MIT-FPA",
    author=__author__,
    author_email="benycarl8@gmail.com",
    maintainer="Smartwa Caleb",
    maintainer_email="smartwacaleb@gmail.com",
    description="Football-Punter's favorite girlfriend - based on Betika platform!",
    long_description="\n".join(get_file("README.md")),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
        "Topic :: Games/Entertainment",
    ],
    keywords=[
        "Football",
        "Predictions",
        "Betting API",
        "Soccer predictions",
        "Football Predictions",
    ],
    entry_points={
        "console_scripts": ["betika = smartBetika.betika:betika"],
    },
)
