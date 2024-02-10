import setuptools
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

required = [
    "requests>=2.31.0",
    "setuptools>=69.0.3"
    "sv_ttk>=2.5.5"
]

setuptools.setup(
    name="pyDDHQAPI",
    version="0.3.2",
    author="Miles Kleiber",
    author_email="milesjkleiber@gmail.com",
    description="Request and Filter data with DecisionDeskHQ's v3 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "pyDDHQAPI"},
    packages=setuptools.find_packages(include=["pyDDHQAPI", "pyDDHQAPI.*"]),
    include_package_data=True,
    install_requires=required,
    python_requires=">=3.7",
)