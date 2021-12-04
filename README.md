# WeatherFlow Local for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

![WeatherFlow Logo](https://github.com/briis/hass-SmartWeather/blob/master/images/weatherflow.png)

This a _custom component_ for [Home Assistant](https://www.home-assistant.io/). It reads real-time data using the [UDP protocol](https://weatherflow.github.io/Tempest/api/udp/v171/) from a _WeatherFlow_ weather station.

It will create a device with several `sensor` entities for each weather reading like Temperature, Humidity, Station Pressure, UV, etc that is associated with it.

**Notes:**

As this component listens for UDP broadcasts, in can take up to 1 minute before all sensors have gotten a value after restart of Home Assistant

## Installation

This Integration can be installed in two ways:

**HACS Installation**

Add the following to the Custom Repository under `Settings` in HACS:

`briis/smartweatherudp` and choose `Ìntegration` as Category

**Manual Installation**

1. If you don't already have a `custom_components` directory in your Home Assistant config directory, create it.
2. Copy the `smartweatherudp` folder under `custom_components` into the `custom_components` folder on Home Assistant.
3. Or using Git, go to the `custom_components` directory and enter:<br/>`git clone https://github.com/briis/smartweatherudp.git`

## Track Updates

If installed via HACS, updates are flagged automatically. Otherwise, you will have to manually update as described in the manual installation steps above.

## Configuration

There is a config flow for this integration. After installing the custom component:

1. Go to **Configuration**->**Integrations**
2. Click **+ ADD INTEGRATION** to setup a new integration
3. Search for **WeatherFlow - Local** and click on it
4. You will be guided through the rest of the setup process via the config flow
   - This will initially try to find devices by listening to UDP messages on `0.0.0.0`. If no devices are found, it will then ask you to enter a host address to try to listen on. Default is `0.0.0.0` but you can enter any host IP. Typically used if your Weather Station is on a different subnet than Home Assistant.

## Available Sensors\*

| Name                       | Description                                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| Air Density                | The current air density.                                                                                |
| Dew Point                  | The atmospheric temperature below which water droplets begin to condense and dew can form.              |
| Feels Like                 | How the temperature feels on the skin. A combination of heat index, wind chill and current temperature. |
| Humidity                   | The relative humidity.                                                                                  |
| Illuminance                | The current brightness.                                                                                 |
| Lightning Average Distance | The average distance detected for lightning.                                                            |
| Lightning Count            | The count of lightning strikes.                                                                         |
| Rain Amount                | The rain amount over the past minute.                                                                   |
| Rain Rate                  | The current rain rate based on the past minute.                                                         |
| Solar Radiation            | The current Solar Radiation measured in W/m².                                                           |
| Station Pressure           | The current barometric pressure.                                                                        |
| Temperature                | The current air temperature.                                                                            |
| UV                         | The UV index.                                                                                           |
| Vapor Pressure             | The current vapor pressure.                                                                             |
| Wet Bulb Temperature       | The current wet bulb temperature.                                                                       |
| Wind Average               | The average wind speed over the past minute.                                                            |
| Wind Direction             | The wind direction.                                                                                     |
| Wind Gust                  | The wind gust speed.                                                                                    |
| Wind Lull                  | The wind lull speed.                                                                                    |
| Wind Speed                 | The current wind speed.                                                                                 |
| Battery                    | The current battery voltage of the sensor.                                                              |
| RSSI                       | The received signal strength indication of the device.                                                  |
| Up Since                   | The UTC datetime the device last came online.                                                           |

\* depends on the device
