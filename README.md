# qosst-hal

<center>

![QOSST Logo](qosst_logo_full.png)

<a href='https://qosst-hal.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/qosst-hal/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://github.com/qosst/qosst-hal/blob/main/LICENSE"><img alt="Github - License" src="https://img.shields.io/github/license/qosst/qosst-hal"/></a>
<a href="https://github.com/qosst/qosst-hal/releases/latest"><img alt="Github - Release" src="https://img.shields.io/github/v/release/qosst/qosst-hal"/></a>
<a href="https://pypi.org/project/qosst-hal/"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/qosst-hal"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/pylint-dev/pylint"><img alt="Linting with pylint" src="https://img.shields.io/badge/linting-pylint-yellowgreen"/></a>
<a href="https://mypy-lang.org/"><img alt="Checked with mypy" src="https://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://img.shields.io/pypi/pyversions/qosst-hal">
    <img alt="Python Version" src="https://img.shields.io/pypi/pyversions/qosst-hal">
</a>
<img alt="Docstr coverage" src=".docs_badge.svg" />
</center>
<hr/>

This project is part of [QOSST](https://github.com/qosst/qosst).

## Features

`qosst-hal` is the Hardware Abstract Layer. Its goal is to provide a unified interface for the hardware and for the higher classes in order for QOSST to be hardware-agnostic. In particular it includes abstraction layer for

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

## Installation

The module can be installed with the following command:

```console
pip install qosst-hal
```

It is also possible to install it directly from the github repository:

```console
pip install git+https://github.com/qosst/qosst-hal
```

It also possible to clone the repository before and install it with pip or poetry

```console
git clone https://github.com/qosst/qosst-hal
cd qosst-alice
poetry install
pip install .
```

## Documentation

The whole documentation can be found at https://qosst-hal.readthedocs.io/en/latest/

## Usage

`qosst-hal` is not supposed to be used as a standalone package, but should be used to code your own hardware classes. There is a tutorial in the documentation on how to code your own hardware, but the basic idea is to subclass the basic hardware class and implement the abstract method of the abstract class. Here is an example on how to do with a VOA class for instance:

```python
from qosst_hal.voa import GenericVOA

class MyVOA(GenericVOA):
    # According to the documentation, the VOA class should implement
    # open, set_value and close
    location: str
    inst: Whatever

    def __init__(self, location:str):
        self.location = location

    def open(self) -> None:
        self.inst = Whatever(self.location)

    def set_value(self, value:float) -> None:
        self.write(value)

    def close(self) -> None:
        self.inst.close()

```

The list of methods that should be implemented for each abstract class can be found in the code, or in the documentation.

Important: no actual implementations are released with QOSST.

## License

As for all submodules of QOSST, `qosst-hal` is shipped under the [Gnu General Public License v3](https://www.gnu.org/licenses/gpl-3.0.html).

## Contributing

Contribution are more than welcomed, either by reporting issues or proposing merge requests. Please check the contributing section of the [QOSST](https://github.com/qosst/qosst) project fore more information.
