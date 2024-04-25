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
PowerMeter module for qosst-hal.
"""
import abc
import logging

from qosst_hal.base import QOSSTHardware

logger = logging.getLogger(__name__)


class GenericPowerMeter(QOSSTHardware, abc.ABC):
    """A Generic PowerMeter should have the following fonction:

    * `open`: open the powermeter
    * `close`: close the powermeter
    * `read`: read the current value
    """

    def __init__(self, *_args, **_kwargs) -> None:
        """
        All parameters are ignored.
        """

    @abc.abstractmethod
    def read(self) -> float:
        """Read the current value.

        Returns:
            float: current value of the powermeter.
        """

    def __str__(self) -> str:
        return "Generic PowerMeter"


class FakePowerMeter(GenericPowerMeter):
    """Fake PowerMeter, to be used as a dummy PowerMeter."""

    def __init__(self, *_args, **_kwargs) -> None:
        """
        All args are ignored.
        """

    def open(self) -> None:
        """
        Open the fake hardware (do nothing).
        """

    def close(self) -> None:
        """
        Close the fake hardware (do nothing).
        """

    def read(self) -> float:
        """
        Read the power from the fake hardware. Always return 1e-6.

        Returns:
            float: always 1e-6 for the fake hardware.
        """
        return 1e-6

    def __str__(self) -> str:
        return "Fake Power Meter"
