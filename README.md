# Smart Weather UDP for Home Assistant
![WeatherFlow Logo](https://github.com/briis/hass-SmartWeather/blob/master/images/weatherflow.png)<br>
This a *custom component* for [Home Assistant](https://www.home-assistant.io/). It reads real-time data using the UDP protocol from a Smart Weather weather station produced by *WeatherFlow*.

It will create several `sensor` entities for each weather reading like Temperature, Precipitation, Rain etc. 

The `smartweather` component uses the [WeatherFlow](https://weatherflow.github.io/SmartWeather/api/udp/v105/) UDP API to retrieve current data for a local WeatherStation.

## Installation
1. If you don't already have a `custom_components` directory in your config directory, create it, and then create a directory called `smartweatherudp`under that.
2. Copy all the files from this repository in to the *smartweatherudp* folder. Remember to maintain the directory structure.
3. or using Git, go to the `custom_components` directory and enter:<br>
`git clone https://github.com/briis/smartweatherudp.git`

## Track Updates
This custom component can be tracked with the help of the [Custom Updater](https://github.com/custom-components/custom_updater) component.

In your configuration.yaml file add the following:
```yaml
custom_updater:
component_urls:
  - https://raw.githubusercontent.com/briis/smartweatherudp/master/custom_updater.json
```

## Configuration
Edit your *configuration.yaml* file and add the *smartweather sensor* component to the file:
```yaml
# Example configuration.yaml entry
sensor:
  - platform: smartweatherudp
    monitored_conditions:
      - temperature
      - feels_like_temperature
      - heat_index
      - wind_chill
      - dewpoint
      - wind_speed
      - wind_gust
      - wind_lull
      - wind_bearing
      - wind_direction
      - precipitation
      - precipitation_rate
      - precipitation_last_1hr
      - precipitation_last_24hr
      - precipitation_yesterday
      - humidity
      - pressure
      - uv
      - solar_radiation
      - illuminance
      - lightning_count
```
#### Configuration Variables
**name**<br>
(string)(Optional) Additional name for the sensors.<br>
Default value: SmartWeather

**monitored_conditions**<br>
(list)(optional) Sensors to display in the frontend.<br>
Default: All Sensors are displayed
* **temperature** - Current temperature
* **feels_like_temperature** - How the temperature Feels Like. A combination of Heat Index and Wind Chill
* **heat_index** - A temperature measurement combining Humidity and temperature. How hot does it feel. Only used when temperature is above 26.67°C (80°F)
* **wind_chill** - How cold does it feel. Only used if temperature is below 10°C (50°F)
* **dewpoint** - Dewpoint. The atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form
* **wind_speed** - Current Wind Speed
* **wind_gust** - Highest Wind Speed in the last minute
* **wind_lull** - Lowest Wind Speed in the last minute
* **wind_bearing** - Wind bearing in degrees (Example: 287°)
* **wind_direction** - Wind bearing as directional text (Example: NNW)
* **precipitation** - Precipitation since midnight
* **precipitation_rate** - The current precipitation rate - 0 if it is not raining
* **precipitation_last_1hr** - Precipitation in the last hour
* **precipitation_last_24hr** - Precipitation in the last 24 hours.
* **precipitation_yesterday** - Precipitation yesterday
* **humidity** - Current humidity in %
* **pressure** - Current barometric pressure, taking in to account the position of the station
* **uv** - The UV index
* **solar_radiation** - The current Solar Radiation measured in W/m2
* **illuminance** - Shows the brightness in Lux
* **lightning_count** - Shows the numbers of lightning strikes for last minute. Attributes of this sensor has more Lightning information.


