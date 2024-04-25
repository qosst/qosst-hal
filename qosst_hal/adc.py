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
Classes for Analog to Digital Converters.
"""
import abc
import logging
from typing import Any, List

import numpy as np

from qosst_hal.base import QOSSTHardware

logger = logging.getLogger(__name__)


class GenericADC(QOSSTHardware, abc.ABC):
    """
    Generic abstract class Analog to Digital converter.

    It should implement:

    * `set_acquisition_parameters` : set the acquisition parameters.
    * `arm_acquisition` : after this call, the acquisition should be ready to be done on trigger.
    * `stop_acquisition` : stop the acquisition.
    * `trigger` : trigger the acquisition after an arm.
    * `get_data` : return the data from the ADC.
    """

    @abc.abstractmethod
    def set_acquisition_parameters(self, **kwargs) -> None:
        """
        Set the required acquisition paramters.

        The parameters depend on the precise function you are using.
        """

    @abc.abstractmethod
    def arm_acquisition(self) -> None:
        """
        Arm the acquisition.

        This means that the acquistion should a be trigger away from being started.
        """

    @abc.abstractmethod
    def stop_acquisition(self) -> None:
        """
        Stop the acquisition.

        If this is done before the trigger and after the arm_acquisiton, this
        should cancer the arm.
        """

    @abc.abstractmethod
    def trigger(self) -> None:
        """
        Trigger the acquisition.
        """

    def _convert(self, data: np.ndarray) -> np.ndarray:
        """
        Convert data from the output of the DAC to a voltage value. This should be
        used in get_data so get_data actually returns the good value.

        Args:
            data (np.ndarray): input data.

        Returns:
            np.ndarray: converted data.
        """
        return data

    @abc.abstractmethod
    def get_data(self) -> List[np.ndarray]:
        """
        Get the data, that is returned as a list
        of numpy arrays.

        Each numy array correspond to a channel in the
        same order given for the configuration of the channel.

        The data should be returned in voltage.

        Returns:
            List[np.ndarray]: the list of output for each channel.
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        return "Generic ADC"


class FakeADC(GenericADC):
    """
    Fake ADC that returns random data.

    The data is drawn from a normal distribuution of mean 0
    and variance that can be given as an extra args to
    the get_data function. By default the variance is 1.
    """

    channels: List[Any]  #: List of channels.
    acquisition_time: float  #: Duration of acquisition, in seconds.
    target_rate: float  #: Target sampling rate, in Hz.

    def __init__(self, _dev_id: Any, channels: List[Any], *_args, **_kwargs) -> None:
        """
        Args:
            _dev_id (Any): ignored parameter.
            channels (List[Any]): list of "channels" (will be used to know how many elements should be returned).
        """
        self.channels = channels

    def open(self) -> None:
        """
        Open the fake hardware (do nothing).
        """

    def close(self) -> None:
        """
        Close the fake hardware (do nothing).
        """

    def set_acquisition_parameters(self, **kwargs) -> None:
        """
        Set the acquisiton parameters.

        Args:
            acquisition_time (float): acquisition time in seconds.
            target_rate (float): target rate in Hz.
        """
        acquisition_time = kwargs.get("acquisition_time", 0)
        target_rate = kwargs.get("target_rate", 0)
        self._set_acquisition_parameters(acquisition_time, target_rate)

    def _set_acquisition_parameters(
        self, acquisition_time: float, target_rate: float
    ) -> None:
        """
        Actually set the acquisition parameters.

        Args:
            acquisition_time (float): acquisition time in seconds.
            target_rate (float): target rate in Hz.
        """
        self.acquisition_time = acquisition_time
        self.target_rate = target_rate

    def arm_acquisition(self) -> None:
        """
        Arm acquisitiion for the fake hardware (do nothing).
        """

    def stop_acquisition(self) -> None:
        """
        Stop the acquisition for the fake hardware (do nothing).
        """

    def trigger(self) -> None:
        """
        Trigger the acquisition for the fake hardware (do nothing).
        """

    def _convert(self, data: np.ndarray) -> np.ndarray:
        """
        Convert the data of the fake hardware (i.e. do nothing and return the original data).

        Args:
            data (np.ndarray): data to convert.

        Returns:
            np.ndarray: converted data (original data in this case).
        """
        return data

    def get_data(self, **kwargs) -> List[np.ndarray]:
        """
        Get the data, that is returned as a list
        of numpy arrays.

        Each numy array correspond to a channel in the
        same order given for the configuration of the channel.

        The data should be returned in voltage.

        Args:
            var (float, optional): variance of the normal distribution. Defaults to 1.

        Returns:
            List[np.ndarray]: the list of output for each channel.
        """
        if "var" in kwargs:
            var = kwargs.pop("var")
        else:
            var = 1
        return [
            self._convert(
                np.random.normal(
                    loc=0.0,
                    scale=np.sqrt(var),
                    size=int(self.acquisition_time * self.target_rate),
                )
            )
            for _ in self.channels
        ]

    def __str__(self) -> str:
        return "Generic ADC"


class LoadingADC(GenericADC):
    """
    An ADC class loading the data from files.
    """

    paths: List[str]  #: Path to look the data for
    data: List[np.ndarray]  #: The data
    channels: List[Any]  #: List of channels

    def __init__(self, _dev_id: Any, channels: List[Any], *_args, **_kwargs) -> None:
        """
        Args:
            _dev_id (Any): ignored parameter.
            channels (List[Any]): list of "channels" (will be used to know how many elements should be returned).
        """
        self.channels = channels

    def open(self) -> None:
        """
        Open the fake hardware (do nothing).
        """

    def close(self) -> None:
        """
        Close the fake hardware (do nothing).
        """

    def set_acquisition_parameters(self, **kwargs) -> None:
        """
        Set the acquisition parameters.

        Args:
            paths (List[str]): list of paths to load the data from (on path per channel).
        """
        paths = kwargs.get("paths", [])
        self._set_acquisition_parameters(paths)

    def _set_acquisition_parameters(self, paths: List[str]) -> None:
        """
        Actually set the acquistion parameters.

        Args:
            paths (List[str]): list of paths to load the data from (on path per channel).
        """
        self.paths = paths

    def arm_acquisition(self) -> None:
        """
        Arm the acquisition for the fake hardware (do nothing).
        """

    def stop_acquisition(self) -> None:
        """
        Stop the acquisition for the fake hardware (do nothing).
        """

    def trigger(self) -> None:
        """
        Trigger the acquisition.
        This actually loads the data from the files.
        """
        self.data = [np.load(path) for path in self.paths]

    def _convert(self, data: np.ndarray) -> np.ndarray:
        """
        Convert the data of the fake hardware (i.e. do nothing and return the original data).

        Args:
            data (np.ndarray): data to convert.

        Returns:
            np.ndarray: converted data (original data in this case).
        """
        return data

    def get_data(self) -> List[np.ndarray]:
        """
        Return the loaded data.

        Returns:
            List[np.ndarray]: list of the loaded data for each channel.
        """
        return [self._convert(data) for data in self.data]

    def __str__(self) -> str:
        return "Loading ADC"
