# qosst-hal - Hardware Abstraction Layer module of the Quantum Open Software for Secure Transmissions.
# Copyright (C) 2024 Thomas Liege
# Copyright (C) 2024 Yoann Piétri

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
Module holding classes for the Power Supply.
"""
import abc
import logging
from typing import Any

from qosst_hal.base import QOSSTHardware

logger = logging.getLogger(__name__)


class GenericPowerSupply(QOSSTHardware, abc.ABC):
    """
    Generic Power Supply.

    Each Power Supply must have:

    * `set_voltage` : set the voltage of the power supply.
    * `set_intensity` : set the intensity of the power supply.
    * `output` : output the voltage/intensity
    """

    @abc.abstractmethod
    def set_voltage(self, voltage_value: float, channel: Any) -> None:
        """Set the voltage.

        Args:
            value (float): Voltage value in some predefined unit.
            channel (Any): channel to use.
        """

    @abc.abstractmethod
    def set_intensity(self, intensity_value: float, channel: Any) -> None:
        """Set the intensity.

        Args:
            value (float): Intensity value in some predefined unit.
            channel (Any): channel to use.
        """

    @abc.abstractmethod
    def output(self, status: int, channel: Any) -> None:
        """Output the voltage and intensity in a channel.

        Args:
            status (int): status of the output.
            channel (Any): channel to use.
        """


class FakePowerSupply(GenericPowerSupply):
    """
    Fake PowerSupply.

    """

    def __init__(self, _location: Any, **_kwargs):
        """
        Args:
            _location (Any): ignored parameter.
        """

    def open(self) -> None:
        """
        Open the fake hardware (do nothing).
        """

    def close(self) -> None:
        """
        Close the fake hardware (do nothing).
        """

    def set_voltage(self, voltage_value: float, channel: int = 1) -> None:
        """
        Set the value.

        Args:
            voltage_value (float): value to be set.
            channel (int): channel to use.
        """

    def set_intensity(self, intensity_value: float, channel: int = 1) -> None:
        """
        Set the value.

        Args:
            intensity_value (float): value to be set.
            channel (int): channel to use.
        """

    def output(self, status: int, channel: int = 1) -> None:
        """
        Output the values.

        Args:
            status (int): status of the output.
            channel (int): channel to use.
        """
