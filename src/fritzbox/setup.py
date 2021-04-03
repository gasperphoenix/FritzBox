from setuptools import setup, find_packages

import _info

setup(
    name         = _info.__package_name__,
    version      = _info.__version__,
    license      = _info.__license__,
    author       = _info.__author__,
    author_email = _info.__email__,
    url          = _info.__url__,
    description  = _info.__package_desc__,
    package_dir  = {"" : "src"},
    py_modules   = ["fritzbox.FBCore", "fritzbox.FBPresence", "fritzbox.FBHomeAuto"]
    )
