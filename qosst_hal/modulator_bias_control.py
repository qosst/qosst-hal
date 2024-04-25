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
Module for Automatic Bias Controller.
"""
import abc
from typing import Any

from qosst_hal.base import QOSSTHardware


class GenericModulatorBiasController(QOSSTHardware, abc.ABC):
    """Generic ModulatorBiasController

    Each modulator bias controller should implement:

    * `lock` : lock the modulator to its working state, and set to low noise mode.
    * `open` : open the modulator bias controller.
    * `close` : close the modulator bias controller.
    """

    def __init__(self, _location: Any, **_kwargs) -> None:
        """
        All parameters are ignored.
        """

    @abc.abstractmethod
    def lock(self, **_kwargs) -> None:
        """
        Set the modulator to its working state. This funciton should only finish when the
        bias controller is ready to work.
        """


class FakeModulatorBiasController(GenericModulatorBiasController):
    """
    Fake modulator bias controller.
    """

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
        Close the fake hardware (do nothing).
        """

    def lock(self, **_kwargs) -> None:
        """
        Lock the fake hardware (do nothing).
        """
