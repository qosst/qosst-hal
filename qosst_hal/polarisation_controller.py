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
PolarisationController module for qosst-hal.
"""
import abc
from typing import Any
from enum import Enum

from qosst_hal.base import QOSSTHardware


class PolarisationControllerChannel(Enum):
    """
    Channels for a fairly regular polarisation controller
    composed of a quarter wave plate, followed by an half
    wave plate, followed by another quarte wave plate.
    """

    QWP_1 = "Quarter Wave Plate 1"  #: Quarter Wave Plate (QWP) 1.
    HWP = "Half Wave Plate"  #: Half Wave Plate (HWP).
    QWP_2 = "Quarter Wave Plate 2"  #: Quarter Wave Plate (QWP) 1.


class GenericPolarisationController(QOSSTHardware, abc.ABC):
    """
    A Generic Polarisation controller class.

    A polarisation controler should implement the following methods:

    * `move_by`: move the channel by the given increment.
    * `move_to`: move the channel to the given position.
    * `open`: open the hardware.
    * `close`: close the hardware.
    """

    def __init__(self, _location: Any, **_kwargs) -> None:
        """
        All parameters are ignored.
        """

    @abc.abstractmethod
    def move_by(
        self,
        increment: float,
        channel: PolarisationControllerChannel = PolarisationControllerChannel.HWP,
    ):
        """Move the designated channel by the increment. The increment unit will depend on the hardware.

        Args:
            increment (float): value to move by.
            channel (PolarisationControllerChannel, optional): channel of the polarisation controller to move. Defaults to PolarisationControllerChannel.HWP.
        """

    @abc.abstractmethod
    def move_to(
        self,
        position: float,
        channel: PolarisationControllerChannel = PolarisationControllerChannel.HWP,
    ):
        """Move the designated channel to the position. The position unit will depend on the hardware.

        Args:
            position (float): value to move to.
            channel (PolarisationControllerChannel, optional): channel of the polarisation controller to move. Defaults to PolarisationControllerChannel.HWP.
        """

    @abc.abstractmethod
    def home(self):
        """
        Move the polarisation controller to its home position.
        """

    @abc.abstractmethod
    def get_position(
        self,
        channel: PolarisationControllerChannel = PolarisationControllerChannel.HWP,
    ) -> float:
        """Return the current position of the channel given in parameter. The unit will depend on the hardware.

        Args:
            channel (PolarisationControllerChannel, optional): channel of the polarisation controller to get. Defaults to PolarisationControllerChannel.HWP.

        Returns:
            float: position of the channel.
        """

    def __str__(self) -> str:
        return "Generic Polarisation Controller"


class FakePolarisationController(GenericPolarisationController):
    """
    Fake Polarisation Controller, to use as a dummy.
    """

    def open(self) -> None:
        """
        Open the fake hardware (do nothing).
        """

    def move_by(
        self,
        increment: float,
        channel: PolarisationControllerChannel = PolarisationControllerChannel.HWP,
    ):
        """Move the designated channel by the increment. The increment unit will depend on the hardware.

        In the case of the fake hardware, do nothing.

        Args:
            increment (float): value to move by.
            channel (PolarisationControllerChannel, optional): channel of the polarisation controller to move. Defaults to PolarisationControllerChannel.HWP.
        """

    def move_to(
        self,
        position: float,
        channel: PolarisationControllerChannel = PolarisationControllerChannel.HWP,
    ):
        """Move the designated channel to the position. The position unit will depend on the hardware.

        In the case of the fake hardware, do nothing.

        Args:
            position (float): value to move to.
            channel (PolarisationControllerChannel, optional): channel of the polarisation controller to move. Defaults to PolarisationControllerChannel.HWP.
        """

    def home(self):
        """
        Do nothing (Fake hardware).
        """

    def get_position(
        self,
        channel: PolarisationControllerChannel = PolarisationControllerChannel.HWP,
    ) -> float:
        """Return the position for the channel. In this case always return 0 (Fake hardware).

        Args:
            channel (PolarisationControllerChannel, optional): channel to get the position from. Defaults to PolarisationControllerChannel.HWP.

        Returns:
            float: this fake hardware always returns 0.
        """
        return 0.0

    def close(self) -> None:
        """
        Close the fake hardware (do nothing).
        """

    def __str__(self) -> str:
        return "Fake Polarisation Controller"
