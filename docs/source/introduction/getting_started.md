# Getting started
## Hardware requirements

### Operating System

The QOSST suite does not required a particular software and should work on Windows (tested), Linux (tested) and Mac (not tested).

The actual operating system requirement will come down to the hardware used for the experiment since some of them don't have interfaces with Linux.

### Python version

QOSST if officially supporting any python version 3.9 or above.

## Installing the software

There are several ways of installing the software, either by using the PyPi repositories or using the source.

```{note}
You usually don't have to install the qosst-hal package manually as it shipped with qosst-alice and qosst-bob. If you however need it, the installation are given below.
```

To install the `qosst-core` package via pip,

```{prompt} bash

pip install qosst-hal
```

Alternatively, you can clone the repository at [https://github.com/qosst/qosst-hal](https://github.com/qosst/qosst-hal) and install it by source.