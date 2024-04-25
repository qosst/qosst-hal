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
Module holding classes for amperemeters.
"""
import abc
import logging
from typing import Any

from qosst_hal.base import QOSSTHardware

logger = logging.getLogger(__name__)


class GenericAmpereMeter(QOSSTHardware, abc.ABC):
    """
    Generic AmpereMeter.

    Each amperemeter must have:

    * `get_current` : get the current for the amperemeter.
    * `open` : open the amperemeter
    * `close` : close the amperemeter
    """

    @abc.abstractmethod
    def get_current(self, **_kwargs) -> float:
        """Get the current current.

        Returns:
            float: the current current.
        """


class FakeAmpereMeter(GenericAmpereMeter):
    """
    Fake AmpereMeter.

    Always return 0 when get_current is called.
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

    def get_current(self, **_kwargs) -> float:
        """
        Return the measured current. In the case of the fake hardware, always return 0.0.

        Returns:
            float: always 0.0 for the fake hardware.
        """
        return 0.0
