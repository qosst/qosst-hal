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
Module for synchronised ADC and DAC.
"""
import abc
from typing import List

import numpy as np

from qosst_hal.base import QOSSTHardware


class GenericDACADC(QOSSTHardware, abc.ABC):
    """Generic class for DACADC.

    A DACADC should implement:

    * `open`: open connection with the device.
    * `close`: close connection with the device.
    * `set_parameters`: set the parameters.
    * `load_dac_data`: load the DAC data.
    * `get_adc_data`: get the ADC data.
    * `start`: start the emission.
    * `stop`: stop the emission.
    """

    @abc.abstractmethod
    def set_parameters(self, **_kwargs) -> None:
        """Set the parameters."""

    @abc.abstractmethod
    def load_dac_data(self, data: List[np.ndarray]) -> None:
        """Load the data to the DAC.

        Args:
            data (List[np.ndarray]): list of array for data (one array per channel).
        """

    @abc.abstractmethod
    def get_adc_data(self) -> List[np.ndarray]:
        """Get the data from the ADC

        Returns:
            List[np.ndarray]: list of array for data (one arrya per channel).
        """

    @abc.abstractmethod
    def start(self) -> None:
        """Start the emission."""

    @abc.abstractmethod
    def stop(self) -> None:
        """Stop the emission."""

    def __str__(self) -> str:
        return "Generic DAC"


class FakeDACADC(GenericDACADC):
    """
    Fake DACADC to be used as a default class.
    """

    def open(self) -> None:
        """
        Open the fake hardware (do nothing).
        """

    def close(self) -> None:
        """
        Close the fake hardware (do nothing).
        """

    def set_parameters(self, **_kwargs) -> None:
        """
        Set the parameters for the fake hardware (do nothing).
        """

    def load_dac_data(self, data: List[np.ndarray]) -> None:
        """
        Load the DAC data. This actually does nothing for the fake hardware.

        Args:
            data (List[np.ndarray]): data to load in the DAC.
        """

    def get_adc_data(self) -> List[np.ndarray]:
        """
        Return the acquired data, In this case, it always return an empty list.

        Returns:
            List[np.ndarray]: an empty list.
        """
        return []

    def start(self) -> None:
        """
        Start DAC and ADC for the fake hardware (do nothing).
        """

    def stop(self) -> None:
        """
        Stop DAC and ADC for the fake hardware (do nothing).
        """
