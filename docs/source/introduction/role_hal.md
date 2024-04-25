# Role of the HAL

The role of the Hardware Abstraction Layer is to provide a unified interface for the different hardware that are used in a CV-QKD setup.

Indeed, the way to communicate with an instrument usually greatly depends on the instrument itself, meaning that changing one instrument would require to change the interacting code. If this code is directly integrated in the main code, then changing the hardware is difficult and time consuming and in general this method doesn't allow for so much flexibility.

```{figure} ../_static/schema_hal.png
---
align: center
---
Role of the Hardware Abstraction Layer
```

As an alternative, an abstraction layer was made in QOSST, to provide interface for:

* Analog-to-Digital Converters (ADC);
* Amperemeters;
* Digital-to-Analog Converters (DAC);
* DAC and ADC simultaneous;
* Lasers;
* Modulation Bias Controllers;
* Polarisation Controllers;
* Powermeters;
* Power supplies;
* Switches (optical switches);
* Variable Optical Attenuators (VOA);
* Voltmeters.

Let's take the example of a Variable Optical Attenuator (VOA) for instance. Some VOA can be controlled by applying a voltage, and we could also imagine having a VOA with a complete board with USB or ethernet communication. For the first one, we could write a code communicating with a power supply that would set the voltage, and for the second one, a code communicating using the communication protocol of the board. The role of the HAL is to provide guidelines so that all the inheriting class will have a `set_value` method that can simply be used will every VOA.

This simple example would look like the following in python;

```{code-block} python

from qosst_hal.voa import GenericVOA

class MyVoltageVOA(GenericVOA):

    def __init__(self, location):
        # Save parameters

    def open(self):
        # Open the communication with the power supply

    def close(self):
        # Close the communication with the power supply

    def set_value(self, value: float):
        # Apply the value to the power supply,
        # Value might be understood as the voltage to apply, or
        # at the target attenuation, that would have to be reversed using 
        # the characterisation. This is a choice of the implementation.

class MyBoardVOA(GenericVOA):
    def __init__(self, location):
        # Save parameters

    def open(self):
        # Open the communication with the board

    def close(self):
        # Close the communication with the board

    def set_value(self, value: float):
        # Use the specific board communication on the VOA.
```

In any case, while the actual implementation will look different, the usage of the classes will be very similar:

```{code-block} python
my_voa = MyVoltageVOA("COM4") # or my_voa = MyBoardVOA("COM4")
my_voa.open()
my_voa.set_value(2)
my_voa.close()
```

This package also provides for "Fake" or dummy hardwares, that do nothing and can be used as default values:

* {py:class}`qosst_hal.adc.FakeADC`
* {py:class}`qosst_hal.amperemeter.FakeAmpereMeter`
* {py:class}`qosst_hal.dac.FakeDAC`
* {py:class}`qosst_hal.dacadc.FakeDACADC`
* {py:class}`qosst_hal.laser.FakeLaser`
* {py:class}`qosst_hal.modulator_bias_control.FakeModulatorBiasController`
* {py:class}`qosst_hal.polarisation_controller.FakePolarisationController`
* {py:class}`qosst_hal.powermeter.FakePowerMeter`
* {py:class}`qosst_hal.powersupply.FakePowerSupply`
* {py:class}`qosst_hal.switch.FakeSwitch`
* {py:class}`qosst_hal.voa.FakeVOA`
* {py:class}`qosst_hal.voltmeter.FakeVoltMeter`
