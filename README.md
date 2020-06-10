# Smart Weather UDP for Home Assistant
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

![WeatherFlow Logo](https://github.com/briis/hass-SmartWeather/blob/master/images/weatherflow.png)<br>
This a *custom component* for [Home Assistant](https://www.home-assistant.io/). It reads real-time data using the UDP protocol from a Smart Weather weather station produced by *WeatherFlow*.

**V0.1.7 - Now has support for the Tempest Weather System!**<br>
The Tempest Weather System combines the functionality of the AIR and SKY units into a single device. 

It will create several `sensor` entities for each weather reading like Temperature, Precipitation, Rain etc. 

The `smartweather` component uses the [WeatherFlow](https://weatherflow.github.io/SmartWeather/api/udp/v105/) UDP API to retrieve current data for a local WeatherStation.

**Notes:** 
1. As this component listens for UDP broadcasts, in can take up to 1 minute before all sensors have gotten a value after restart of Home Assistant
2. Precipitation values broadcasted from the unit is always current precipitation rate. That means that the value in the sensor *precipitation* is a calculated value. So if the system is restartet during the day, the value will be reset to 0. As long as the system is running this should be correct.
3. My setup is 1 AIR unit and 1 SKY unit. This component is only designed to work with one of each unit. But I would be glad to know what happens if you have more than one of each unit connected to the same base.

## Installation
This Integration can be installed in two ways:

**HACS Installation**<br>
Add the following to the Custom Repository under `Settings` in HACS:<br>
`briis/smartweatherudp` and choose `Ìntegration` as Category

**Manuel Installation**<br>
1. If you don't already have a `custom_components` directory in your config directory, create it, and then create a directory called `smartweatherudp`under that.
2. Copy `__init__.py`, `manifest.json` and `sensor.py` from this repository in to the *smartweatherudp* folder. 
3. or using Git, go to the `custom_components` directory and enter:<br>
`git clone https://github.com/briis/smartweatherudp.git`

## Track Updates
If installed via HACS, updates are flagged automatically. If you did a manual installation this custom component can be tracked with the help of the [Custom Updater](https://github.com/custom-components/custom_updater) component.

In your configuration.yaml file add the following:
```yaml
custom_updater:
component_urls:
  - https://raw.githubusercontent.com/briis/smartweatherudp/master/custom_updater.json
```

## Configuration
Edit your *configuration.yaml* file and add the *smartweather sensor* component to the file:<br>
**Note** If you don't add `monitored_conditions` then all sensors will be created.

```yaml
# Example configuration.yaml entry
sensor:
  - platform: smartweatherudp
    host: 0.0.0.0
    wind_unit: kmh
    monitored_conditions:
      - temperature
      - dewpoint
      - feels_like
      - heat_index
      - wind_chill
      - wind_speed
      - wind_bearing
      - wind_speed_rapid
      - wind_bearing_rapid
      - wind_gust
      - wind_lull
      - wind_direction
      - precipitation
      - precipitation_rate
      - humidity
      - pressure
      - uv
      - solar_radiation
      - illuminance
      - lightning_count
      - airbattery
      - skybattery
```
#### Configuration Variables
**wind_unit**<br>
(string)(optional) If Home Assistant Unit System is *metric*, specify `kmh` to get units in km/h. Else this has no effect.<br>
Default Value: m/s if Home Assistant Unit System is *metric*, and mph if Unit System is *imperial*

**host**<br>
(string)(optional) Default is `0.0.0.0` but you can enter any host IP. Typically used if your Weather Station is on a different Subnet than Home Assistant.

**name**<br>
(string)(Optional) Additional name for the sensors.<br>
Default value: SmartWeather

**monitored_conditions**<br>
(list)(optional) Sensors to display in the frontend.<br>
Default: All Sensors are displayed
* **temperature** - Current temperature
* **dewpoint** - Dewpoint. The atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form
* **feels_like** - How the temperature Feels Like. A combination of Heat Index and Wind Chill
* **heat_index** - A temperature measurement combining Humidity and temperature. How hot does it feel. Only used when temperature is above 26.67°C (80°F)
* **wind_chill** - How cold does it feel. Only used if temperature is below 10°C (50°F)
* **wind_speed** - Average Wind Speed in the last minute
* **wind_bearing** - Average Wind bearing in degrees for the last minute (Example: 287°)
* **wind_speed_rapid** - Current Wind Speed (Updated every 3 seconds)
* **wind_bearing_rapid** - Current Wind Bearing in degrees (Updated every 3 seconds)
* **wind_gust** - Highest Wind Speed in the last minute
* **wind_lull** - Lowest Wind Speed in the last minute
* **wind_direction** - Average Wind bearing as directional text for the last minute (Example: NNW)
* **precipitation** - Precipitation since midnight
* **precipitation_rate** - The current precipitation rate - 0 if it is not raining
* **humidity** - Current humidity in %
* **pressure** - Current barometric pressure, taking in to account the position of the station
* **uv** - The UV index
* **solar_radiation** - The current Solar Radiation measured in W/m2
* **illuminance** - Shows the brightness in Lux
* **lightning_count** - Shows the numbers of lightning strikes for last minute. Attributes of this sensor has more Lightning information.
* **airbattery** - The current voltage of the attached AIR unit 
* **skybattery** - The current voltage of the attached SKY unit

NOTE:  The Tempest Weather System will return its battery voltage in BOTH the airbattery and skybattery sensors

