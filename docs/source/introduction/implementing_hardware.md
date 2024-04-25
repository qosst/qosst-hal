# Implementing your own hardware class

## General idea

The general idea is that the `qosst-hal` package provides abstract classes with the required commands. Hence, to implement a new hardware, one first needs to find the appropriate abstract class, and then to create a new class that inherits from the abstract class. Then several methods need to be implemented: it always includes `__init__`, `open` and `close` and the rest depends on the class chosen, as described later on this page.

Here is an exemple of a voltmeter with communication using serial

```{code-block} python
import logging

from qosst_hal.utils import need_modules
from qosst_hal.voltmeter import GenericVoltMeter

logger = logging.getLogger(__name__)

try:
    import serial
except ImportError:
    logger.warning("serial was not imported.")


@need_modules("serial")
class SerialVoltmeter(GenericVoltMeter):
    serial: "serial.Serial"  #: The serial object.

    port: str  #: The USB communication port.
    baudrate: int  #: The baud rate for the serial communication.
    sleep_time: float  #: Sleep time when making requests.
    timeout: float  #: Serial timeout.

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 0.05,
    ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def open(self) -> None:
        self.serial = serial.Serial(
            port=self.port, baudrate=self.baudrate, timeout=self.timeout
        )

    def close(self):
        self.serial.close()

    def _read_serial(self) -> str:
        output = self.serial.read_until("\r")
        return output.decode()

    def _write_serial(self, message: str) -> int:
        return self.serial.write(str(message + "\r").encode())

    def _request_serial(self, message: str) -> str:
        self._write_serial(message)
        time.sleep(self.sleep_time)
        return self._read_serial()

    def get_voltage(self) -> float:
        return float(self._request_serial)
```

The `need_module` decorator is explained at the end of this page.
## QOSSTHardware

Every other abstract class of the HAL inherits from the abstract class {py:class}`qosst_hal.base.QOSSTHardware`. This abstract class plan for two abstract methods `open` and `close`.

**This means that any hardware in QOSST must have an open and a close method**.

The parameters for the communication are passed through the init method. Then the `open` method has to initiate the communication and the `close` method has to terminate it.

The other methods depend on the type of hardware and are described below.

## Required methods
### ADC

Base class : {py:class}`qosst_hal.adc.GenericADC` ({doc}`API link <../api/adc>`).

ADC classes mut implement the following methods:

* `__init__(self, location, channels, **kwargs)`: the parameters are the location of the device (or device ID) and the list of channels to acquire from. This can also take extra arguments.
* `set_acquisition_parameters`: set the acquisition parameters, like the rate and the acquisition time.
* `arm_acquisiton(self)`: prepare the device for acquisition.
* `trigger(self)`: trigger the acquisition.
* `stop_acquisiton(self)`: stop the acquisition.
* `get_data(self)`: return the data, as a list of numpy arrays, one for each channel.

### Amperemeter

Base class : {py:class}`qosst_hal.amperemeter.GenericAmpereMeter` ({doc}`API link <../api/amperemeter>`).

Amperemeter classes must implement the following methods:

* `__init__(self, location, **kwargs)`: the parameter is the location of the device. This can also take extra parameters.
* `get_current(self)`: return the current current.

### DAC

Base class : {py:class}`qosst_hal.dac.GenericDAC` ({doc}`API link <../api/dac>`).

DAC classes mut implement the following methods:

* `__init__(self, location, channels, **kwargs)`: the parameters are the location of the device (or device ID) and the list of channels to acquire from. This can also take extra arguments.
* `set_emission_parameters(self, **kwargs)`: to set the emission parameters like the rate or the amplitude.
* `load_data(self, data)`: to load the data into the DAC where data is a list of numpy arrays, one for each channel.
* `start_emission(self)`: start the emission of the data.
* `stop_emission(self)`: stop the emission of the data.

### DACADC

Base class : {py:class}`qosst_hal.dacadc.GenericDACADC` ({doc}`API link <../api/dacadc>`).

DACADC classes mut implement the following methods;

* `__init__(self, dac_location, adc_location, **kwargs)`: the parameters are the location of the dac device and te location of the adc device. (or device ID). This can also take extra arguments.
* `set_parameters`: set the acquisition emission parameters, like the rate and the acquisition time.
* `get_adc_data(self)`: return the data, as a list of numpy arrays, one for each channel.
* `load_dac_data(self, data)`: to load the data into the DAC where data is a list of numpy arrays, one for each channel.
* `start(self)`: start the emission of the data.
* `stop(self)`: stop the emission of the data.

### Laser

Base class : {py:class}`qosst_hal.laser.GenericLaser` ({doc}`API link <../api/laser>`).

Laser classes mut implement the following methods:

* `__init__(self, location, **kwargs)`: the main parameter is the location of the device but this can also take extra args.
* `set_parameters(**kwargs)`: set the parameters of the laser like power and frequency. The parameters will depend on the laser.
* `enable(self)`: enable the laser.
* `disable(disable)`: disable the laser. 

### Modulator bias controller

Base class : {py:class}`qosst_hal.modulator_bias_control.GenericModulatorBiasController` ({doc}`API link <../api/modulator_bias_control>`).

Modulator bias controller classes must implement the following methods:

* `__init__(self, location, **kwargs)`: the main parameter is the location of the device but this can also take extra args.
* `lock(self)`: lock the IQ modulator to is functioning point.

### Polarisation Controller

Base class : {py:class}`qosst_hal.polarisation_controller.GenericPolarisationController` ({doc}`API link <../api/polarisation_controller>`).

Polarisation controller classes must implement the following methods:

* `__init__(self, location, **kwargs)`: the main parameter is the location of the device but this can also take extra args.
* `home(self)`: return the polarisation controller to its home position.
* `get_position(self, channel)`: get the current position of one channel (where channel is an instance of {py:class}`qosst_hal.polarisation_controller.PolarisationControllerChannel`).
* `move_by(self, increment, channel)`: move the channel by the increment (where channel is an instance of {py:class}`qosst_hal.polarisation_controller.PolarisationControllerChannel`).
* `move_to(self, position, channel)`: move the channel to the position (where channel is an instance of {py:class}`qosst_hal.polarisation_controller.PolarisationControllerChannel`).

### Powermeter

Base class : {py:class}`qosst_hal.powermeter.GenericPowerMeter` ({doc}`API link <../api/powermeter>`).

Powermeter classes must implement the following methods:

* `__init__(self, location, **kwargs)`: the main parameter is the location of the device but this can also take extra args.
* `read(self)`: read the current value of the powermeter and return it.

### Powersupply

Base class : {py:class}`qosst_hal.powersupply.GenericPowerSupply` ({doc}`API link<../api/powersupply>`).

Powersupply classes must implement the following methods:

* `__init__(self, location, **kwargs)`: the main parameter is the location of the device but this can also take extra args.
* `set_voltage(self, channel)`: set the target voltage on the channel.
* `set_intensity(self, channel)`: set the maximal current on the channel.
* `output(self, status, channel)`: set on (`status=True`) or off (`status=False`) the channel.

### Switch

Base class : {py:class}`qosst_hal.switch.GenericSwitch` ({doc}`API link <../api/switch>`).

Switch classes must implement the following methods:

* `__init__(self, location, **kwargs)`: the main parameter is the location of the device but this can also take extra args.
* `set_state(self, state)`: switch the switch to the required state.
* `read_state(self)`: read the state and return it. If the state cannot be returned, then it should be saved as an attribute.

### VOA

Base class : {py:class}`qosst_hal.voa.GenericVOA` ({doc}`API link <../api/voa>`).

VOA classes must implement the following methods:

* `__init__(self, location, **kwargs)`: the main parameter is the location of the device but this can also take extra args.
* `set_value(self, value)`: set the value to the VOA.

### Voltmeter

Base class : {py:class}`qosst_hal.voltmeter.GenericVoltMeter` ({doc}`API link <../api/voltmeter>`).

Voltmeter classes must implement the following methods:

* `__init__(self, location, **kwargs)`: the main parameter is the location of the device but this can also take extra args.
* `get_voltage(self)`: read the current value of the voltmeter and return it.

## need_modules

{py:func}`qosst_hal.utils.need_modules` is a class decorator. This decorator will test if the modules that are passed as parameters are available. If they are, then nothing is done, but if at least one is missing, then the class will be replaced by a class that cannot be instantiated.

For instance, if the module `installed_module` is installed, but not the module `not_installed_module`:

```{code-block} python

from qosst_hal.utils import need_modules

try:
    import installed_module
except ImportError:
    pass

@need_modules("installed_module")
class MyClass:
    pass
```

```{code-block} python

from qosst_hal.utils import need_modules

try:
    import not_installed_module
except ImportError:
    pass

@need_modules("not_installed_module")
class MyClass:
    pass
```

are bot valid codes. However, trying to actually use the class with

```{code-block} python

m = MyClass()
```

will only work in the first case, and raise an exception in the second case:

```{code-block} text

TypeError: You are trying to use the class MyClass which requires the optional modules : ('not_installed_module',) and at least one is not installed.
```

This allows to import modules even if all the optional dependencies are not present, as long as the class with optional dependency is not used.
