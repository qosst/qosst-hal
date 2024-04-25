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
DAC module for qosst-hal.
"""
from typing import List, Optional
import abc
import logging

import numpy as np

from qosst_hal.base import QOSSTHardware

logger = logging.getLogger(__name__)


class GenericDAC(QOSSTHardware, abc.ABC):
    """Generic class for DAC.

    A DAC should implement:

    * `open`: open connection with the device
    * `close`: close connection with the device
    * `set_emission_parameters`: set the emission parameters.
    * `load_data`: load data
    * `start_emission`: start the emission
    * `stop_emission`: stop the emission
    """

    @abc.abstractmethod
    def set_emission_parameters(self, **_kwargs) -> None:
        """Set the emission parameters."""

    @abc.abstractmethod
    def load_data(self, data: List[np.ndarray]) -> None:
        """Load the data to the DAC.

        Args:
            data (List[np.ndarray]): list of array for data (one array per channel).
        """

    @abc.abstractmethod
    def start_emission(self) -> None:
        """Start the emission."""

    @abc.abstractmethod
    def stop_emission(self) -> None:
        """Stop the emission."""

    def __str__(self) -> str:
        return "Generic DAC"


class FakeDAC(GenericDAC):
    """Fake DAC, to be used as a dummy DAC."""

    emission: bool  #: emission state
    data: Optional[List[np.ndarray]]  #: data

    def open(self) -> None:
        """
        Open the fake hardware (do nothing).
        """

    def close(self) -> None:
        """
        Close the fake hardware (do nothing).
        """

    def __init__(self, _location, _channels, **_kwargs) -> None:
        """
        Start with no data and emission is False.
        """
        self.emission = False
        self.data = None

    def set_emission_parameters(self, *_args, **_kwargs) -> None:
        """
        Set the emission parameters for the fake hardware (do nothing).
        """

    def load_data(self, data: List[np.ndarray]) -> None:
        """
        Load the data.

        Args:
            data (List[np.ndarray]): date to emit.
        """
        self.data = data

    def start_emission(self) -> None:
        """
        Start the emission (set emission status to True).
        """
        self.emission = True

    def stop_emission(self) -> None:
        """
        Stop the emission (set emission status to False).
        """
        self.emission = False

    def __str__(self) -> str:
        return "Fake DAC"
