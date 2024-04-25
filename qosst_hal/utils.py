# qosst-hal - Hardware Abstraction Layer module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2021-2024 Yoann Piétri

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Module with utils functions for qosst-hal.
"""
import pkgutil
import importlib
import sys
import inspect
from pathlib import Path
from importlib.util import find_spec
from typing import Callable, Type, Dict, List

from qosst_hal.base import QOSSTHardware


def list_hardware(package: str) -> Dict[str, List[str]]:
    """
    Return the list of classes inheriting from QOSSTHardware
    (except QOSSTHardware) as a Dict of list of str in the package. The key corresponds
    to the module name and the list to the list of hardware classes.

    Args:
        module (str): name of the package to inspect.

    Returns:
        Dict[str, List[str]]: dict containing the list of hardwares for each submodule.
    """
    res: Dict[str, List[str]] = {}
    # First, list all submodules
    try:
        loaded_package = importlib.import_module(package)
    except ModuleNotFoundError:
        return res

    assert loaded_package.__file__ is not None

    submodules = [
        name
        for _, name, _ in pkgutil.iter_modules(
            [str(Path(loaded_package.__file__).parent)]
        )
    ]

    # Now for each submodule, import it and print the classes
    for submodule in submodules:
        res[submodule] = []
        importlib.import_module(f"{package}.{submodule}")
        for name, obj in inspect.getmembers(sys.modules[f"{package}.{submodule}"]):
            if (
                inspect.isclass(obj)
                and issubclass(obj, QOSSTHardware)
                and obj != QOSSTHardware
            ):
                res[submodule].append(name)
    return res


def list_hardware_str(package: str) -> str:
    """
    Return the list of classes inheriting from QOSSTHardware
    (except QOSSTHardware) as a a str.

    Args:
        package (str): name of the package to inspect.

    Returns:
        str: str containing the list of hardwares for each submodule.
    """
    res = f"Hardware of package {package}\n\n"
    hardware = list_hardware(package)

    # Now for each submodule, import it and print the classes
    for submodule, submodule_hardware in hardware.items():
        if submodule_hardware:
            res += submodule + "\n"
            res += "-" * len(submodule) + "\n"
            for name in submodule_hardware:
                res += f"* {name}\n"
            res += "\n"
    return res


#########################
## WAIT BEFORE LEAVING ##
#########################

# This function seems weird, and actually is.
# To quote a python advanced user : "it's so beautiful and so nasty"
# For those who want to understand what this is doing, and to use it,
# the docstirng of the function will include those information.
#
# If you want a better understanding however, it's just below :
# What is a decorator ?
# In Python, a decorator (or wrapper) are special functions that are used
# with a @ before a function or a class. Example :
# @wrapper
# def myfunc(a, b):
#   return a+b
#
# wrapper will be define like
# def wrapper(func):
#   def newfunc(a, b):
#       return a*b
#
# And if you try to run myfunc(3,4) you will end with 12 and not 7.
# The wrapper is modifying the function (in this case, it's even
# completely replacing the function).
# So a wrapper is a function that takes a function as its unique parameter
# and returning a function.
# You can also do wrappers with class, with the same concept.
#
# Here we want to have a wrapper with the following behavior :
# 1. If all the modules needed for the class are available, the class is returned (identity)
# 2. If one or several modules needed are missing, we return a class
#  that will throw an exception at initialization
#
# Why not raising the exception in the execution of the wrapper ?
# This is because wrappers are executed at the same time as imports,
# and we want to be able to import a module even if some
# functions in it will not be able to run.
#
# Now, how do we know the modules needed ? We could try that to get them dynamically
# from the module, but the simplest it to pass it as parameters.
#
# But wrapper only takes one parameter which is the class...
# So we need a decorator generator.
# It will take the modules in parameters, and will return
# the associated decorator (which is a function).
# So in the end, we have a function taking modules as arguments,
# that will return a function, taking a class as an argument and returning a class.
#
# This would be a valid usage :
# from cvqkd_hal.utils import need_modules
#
# @need_modules("scipy")
# def Class:
#   def __init__(self):
#       print(scipy.constants.c)
#
# WARNING : THIS WILL NOT WORK WITH FUNCTIONS


def need_modules(*modules: str) -> Callable:
    """
    Decorator generator.

    This will generate a decorator ensuring that the needed modules are
    loadable before starting the execution of class methods.

    Args:
        modules (str): needed modules (``*args``)

    Here is a usage example :

    .. code-block:: python

        from cvqkd_hal.utils import need_modules

        @need_modules("scipy", "numpy")
        def Class:
            def __init__(self):
                print(scipy.constants.c)
                print(numpy.__version__)
    """

    def decorator(initial_class: Type) -> Type:
        """
        The actual decorator.

        If all the modules are here the initial class is returned.
        Otherwise, it will return a class that will fail when trying
        to be initialized.
        """
        res = True
        for module in modules:
            res = res and find_spec(module) is not None

        if not res:
            name = initial_class.__name__

            # pylint: disable=too-few-public-methods
            class ReplacementClass(initial_class):
                """
                This class raises an exception if it gets initialized.
                """

                def __init__(self, *_args, **_kwargs):
                    """
                    Raises:
                        TypeError: prevent using a class with a missing dependency.
                    """
                    raise TypeError(
                        f"You are trying to use the class {name} which requires the optional \
                            modules : {modules} and at least one is not installed."
                    )

            return ReplacementClass
        return initial_class

    return decorator
