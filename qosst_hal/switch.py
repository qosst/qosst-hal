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
Module holding classes for optical switches.
"""
import abc
from typing import Any
import logging

from qosst_hal.base import QOSSTHardware

logger = logging.getLogger(__name__)


class GenericSwitch(QOSSTHardware, abc.ABC):
    """
    A generic switch.

    A switch should implement the following methods:
    * `open`: open the switch
    * `close`: close the switch
    * `set_state`: set the switch to the given state.
    * `read_state`: read the current state. If it cannot be queried, it should be saved as an attribute.
    """

    def __init__(self, _location: Any, **kwargs):
        """
        All parameters are ignored.
        """

    @abc.abstractmethod
    def set_state(self, state: int) -> None:
        """Set the switch to the given state.

        Args:
            state (int): state to which the switch should be set.
        """

    @abc.abstractmethod
    def read_state(self) -> int:
        """Read the current state of the switch.

        If it cannot be queried, it should be saved as an attribute.

        Returns:
            int: current state of the switch.
        """

    def __str__(self) -> str:
        return "Generic Switch"


class FakeSwitch(GenericSwitch):
    """Fake switch, to use as a dummy switch."""

    def __init__(self, _location: Any, **kwargs):
        """
        Args:
            _location (Any): ignored parameter.
        """

    def open(self):
        """
        Open the fake hardware (do nothing).
        """

    def close(self):
        """
        Close the fake hardware (do nothing).
        """

    def set_state(self, state: int):
        """
        Set the state for the fake hardware (do nothing).

        Args:
            state (Any): ignored parameter.
        """

    def read_state(self) -> int:
        """
        Return the state of the fake hardware (always return 0).

        Returns:
            int: always return 0 for the fake hardware.
        """
        return 0

    def __str__(self) -> str:
        return "Fake Switch"
