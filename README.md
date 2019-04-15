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


