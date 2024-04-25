# Welcome to qosst-hal's documentation!

```{image} _static/logo.png
:width: 200px
:name: landing-page-logo
:align: center
```

QOSST HAL, HAL for Hardware Abstraction Layer, holds the interface class for the different hardware used in the QOSST software.

This project is part of [QOSST](https://github.com/qosst).

```{warning}

This package only provides the abstract classes for the abstraction layer and does not provide any actual implementation of the hardware. Will some implementations might have been release, they are not part of this software.
```

```{toctree}
---
caption: Introduction
---
introduction/getting_started.md
introduction/role_hal.md
introduction/implementing_hardware.md
```

```{toctree}
---
caption: API
maxdepth: 1
---
api/base.md
api/adc.md
api/amperemeter.md
api/dac.md
api/dacadc.md
api/laser.md
api/modulator_bias_control.md
api/polarisation_controller.md
api/powermeter.md
api/powersupply.md
api/switch.md
api/voa.md
api/voltmeter.md
api/utils.md
```

```{toctree}
---
caption: Community
maxdepth: 1
---
community/contributing.md
community/license.md
```
