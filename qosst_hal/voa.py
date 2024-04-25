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
VOA module for qosst-hal.
"""
import abc
from typing import Any

from qosst_hal.base import QOSSTHardware


class GenericVOA(QOSSTHardware, abc.ABC):
    """
    A Generic VOA class.

    A VOA class should have the following methods:

    * `set_value`: set value for the VOA, in some defined units.
    * `open`: open the VOA.
    * `close`: close the VOA.
    """

    def __init__(self, _location: Any, **_kwargs) -> None:
        """
        All parameters are ignored.
        """

    @abc.abstractmethod
    def set_value(self, value: float) -> None:
        """Set VOA value

        Args:
            value (float): VOA value in some predefined unit.
        """

    def __str__(self) -> str:
        return "Generic VOA"


class FakeVOA(GenericVOA):
    """FakeVOA, to use as a dummy VOA."""

    value: float  #: Value of the VOA (no unit, as it's dummy).

    def __init__(self, _location: Any, **_kwargs) -> None:
        """
        Args:
            _location (Any): ignored parameters.
        """
        self.value = 0.0

    def open(self) -> None:
        """
        Open the fake hardware (do nothing).
        """

    def set_value(self, value: float) -> None:
        """
        Set the value.

        Args:
            value (float): value to be set.
        """
        self.value = value

    def close(self) -> None:
        """
        Close the fake hardware (do nothing).
        """

    def __str__(self) -> str:
        return f"Fake VOA (value : {self.value})"
