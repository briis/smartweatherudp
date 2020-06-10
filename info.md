# Smart Weather UDP for Home Assistant
This a *custom component* for [Home Assistant](https://www.home-assistant.io/). It reads real-time data using the UDP protocol from a Smart Weather weather station produced by *WeatherFlow*.

It will create several `sensor` entities for each weather reading like Temperature, Precipitation, Rain etc. 

The `smartweather` component uses the [WeatherFlow](https://weatherflow.github.io/SmartWeather/api/udp/v119/) UDP API to retrieve current data for a local WeatherStation.

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
