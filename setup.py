from setuptools import setup, find_packages

setup(
    name = "fritzbox",
    version = "0.3",
    license = "GNU General Public License v3.0, 29 June 2007",
    author = "Dennis Jung, Dipl.-Ing. (FH)",
    author_email = "Dennis.Jung@stressfrei-arbeiten.com",
    url = "https://github.com/gasperphoenix/FritzBox",
    description = "This package provides an interface for interaction with an AVM FritzBox",
    package_dir = {"" : "src"},
    py_modules = ["fritzbox.FBCore", "fritzbox.FBPresence", "fritzbox.FBHomeAuto"]
    )
