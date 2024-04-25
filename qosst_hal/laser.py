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
LASER module for qosst-hal.
"""
import abc
from typing import Any

from qosst_hal.base import QOSSTHardware


class GenericLaser(QOSSTHardware, abc.ABC):
    """Class for Generic Laser.

    A Laser Class should implement:

    * `open`: open connection with the laser.
    * `close`: close connection with the laser.
    * `set_parameters`: set the different parameter of the laser.
    * `enable`: start the laser with the given parameters.
    * `disable`: disable the emission.
    """

    def __init__(self, _location: Any, **_kwargs) -> None:
        """
        All parameters are ignored.
        """

    @abc.abstractmethod
    def set_parameters(self, **_kwargs) -> None:
        """
        Set the parameters of the laser. Refer to specific classes to know which parameters they accept.
        """

    @abc.abstractmethod
    def enable(self) -> None:
        """
        Start the emission of the laser with the parameters set in `set_parameters`.

        This also disables all possible loops to reach low noise levels.
        """

    @abc.abstractmethod
    def disable(self) -> None:
        """
        Stop the emission of the laser.
        """

    def __str__(self) -> str:
        return "Abstract LASER"


class FakeLaser(GenericLaser):
    """Fake laser, to be used as a dummy laser."""

    def __init__(self, _location: Any, **_kwargs) -> None:
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
        Close the fake hardware (do nothing)
        """

    def set_parameters(self, **_kwargs) -> None:
        """
        Set the parameters for the fake hardware (do nothing).
        """

    def enable(self) -> None:
        """
        Enable the fake hardware (do nothing).
        """

    def disable(self) -> None:
        """
        Disable the fake hardware (do nothing).
        """

    def __str__(self) -> str:
        return "Fake laser"
