# WeatherFlow Local for Home Assistant

This a _custom component_ for [Home Assistant](https://www.home-assistant.io/). It reads real-time data using the [UDP protocol](https://weatherflow.github.io/Tempest/api/udp/v171/) from a _WeatherFlow_ weather station.

It will create a device with several `sensor` entities for each weather reading like Temperature, Humidity, Station Pressure, UV, etc that is associated with it.

## Configuration

There is a config flow for this integration. After installing the custom component:

1. Go to **Configuration**->**Integrations**
2. Click **+ ADD INTEGRATION** to setup a new integration
3. Search for **WeatherFlow - Local** and click on it
4. You will be guided through the rest of the setup process via the config flow
   - This will initially try to find devices by listening to UDP messages on `0.0.0.0`. If no devices are found, it will then ask you to enter a host address to try to listen on. Default is `0.0.0.0` but you can enter any host IP. Typically used if your Weather Station is on a different subnet than Home Assistant.
