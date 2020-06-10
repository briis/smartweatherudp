# List of Changes

### Version 0.1.7
* Added support for the Tempest Weather System

### Version 0.1.3
* Added `manifest.json` to ensure compliance with Home Assistant >= 0.92.x. 
* Changed the Custom Updater setup, to ensure that it works with multiple files going forward. You will need to re-download `sensor.py`, `__init__.py` and `manifest.json` 

### Version 0.1.1
* Icons for Battery devices now reflect the current state of the Battery Charge. When new Batteries are inserted the Voltage is typically around 3.2V to 3.3V. And by experience the Unit stops working at around 2.3V +/- 0.1V. So the Icon stage reflects that Interval
* Fixed documentation error in README.md, listing the wrong sensors

### Version 0.1.0
* Initial Release.
