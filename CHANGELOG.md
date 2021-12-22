# List of Changes

## Version 2021.12.5

- Bump pyweatherflowudp to 1.2.0 - [Changelog](https://github.com/briis/pyweatherflowudp/blob/main/CHANGELOG.md)

## Version 2021.12.4

- Bump pyweatherflowudp to 1.1.2 - [Changelog](https://github.com/briis/pyweatherflowudp/blob/main/CHANGELOG.md)

## Version 2021.12.3

- Add an additional debug log when setting up sensors

## Version 2021.12.2

- Bump pyweatherflowudp to 1.1.1 to better handle future firmware revisions

## Version 2021.12.1

- Round temperature values to one decimal

## Version 2021.12.0

### Breaking Changes

- configuration.yaml setup has been deprecated
  - previous configuration.yaml entries should be migrated automatically to a config entry by this release and then can be safely deleted
- entity ids have changed to `sensor.<device_type>_<serial_number>_<attribute>`
- removes heat index and wind chill since they are incorporated in the "feels like" temperature

### What's New

- Setup is now supported via the UI so there is no need to modify the configuration.yaml (as it has been deprecated)
- Devices are now created based on the type (hub, air, sky, or tempest) with relevant data points
- Migrated from pysmartweatherudp to pyweatherflowudp
- Data points are refreshed only when the device sends an update that corresponds to that attribute
  - wind speed every 3 seconds or so
  - temperature, humidity, pressure, etc every minute

## Version 0.1.8

- Add required version number to home assistant manifest

## Version 0.1.7

- Added support for the Tempest Weather System

## Version 0.1.3

- Added `manifest.json` to ensure compliance with Home Assistant >= 0.92.x.
- Changed the Custom Updater setup, to ensure that it works with multiple files going forward. You will need to re-download `sensor.py`, `__init__.py` and `manifest.json`

## Version 0.1.1

- Icons for Battery devices now reflect the current state of the Battery Charge. When new Batteries are inserted the Voltage is typically around 3.2V to 3.3V. And by experience the Unit stops working at around 2.3V +/- 0.1V. So the Icon stage reflects that Interval
- Fixed documentation error in README.md, listing the wrong sensors

## Version 0.1.0

- Initial Release.
