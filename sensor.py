
import datetime
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import ENTITY_ID_FORMAT, PLATFORM_SCHEMA
from homeassistant.const import (ATTR_ATTRIBUTION, CONF_MONITORED_CONDITIONS,
                                 CONF_NAME, DEVICE_CLASS_HUMIDITY,
                                 DEVICE_CLASS_ILLUMINANCE,
                                 DEVICE_CLASS_PRESSURE,
                                 DEVICE_CLASS_TEMPERATURE,
                                 DEVICE_CLASS_BATTERY,
                                 TEMP_CELSIUS, UNIT_UV_INDEX)
from homeassistant.helpers.entity import Entity, generate_entity_id

REQUIREMENTS = ['pysmartweatherudp==0.1.5']

__version__ = "0.1.1"

DOMAIN = 'smartweatherudp'

ATTRIBUTION = 'Powered by a Smart Homer Weather Station via UDP'

CONF_WIND_UNIT = 'wind_unit'

_LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 50222

ATTR_LAST_UPDATE = 'last_update'
ATTR_LIGHTNING_DETECTED = 'last_detected'
ATTR_LIGHTNING_DISTANCE = 'lightning_distance'

# Sensor types are defined like: Name, Metric unit, icon, device class, Imperial unit
SENSOR_TYPES = {
    'temperature': ['Temperature', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'dewpoint': ['Dewpoint', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'feels_like': ['Feels Like', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'heat_index': ['Heat Index', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'wind_chill': ['Wind Chill', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'wind_speed': ['Wind Speed', 'm/s', 'mdi:weather-windy', None, 'mph'],
    'wind_bearing': ['Wind Bearing', '°', 'mdi:compass-outline', None, None],
    'wind_speed_rapid': ['Wind Speed Realtime', 'm/s', 'mdi:weather-windy', None, 'mph'],
    'wind_bearing_rapid': ['Wind Bearing Realtime', '°', 'mdi:compass-outline', None, None],
    'wind_gust': ['Wind Gust', 'm/s', 'mdi:weather-windy', None, 'mph'],
    'wind_lull': ['Wind Lull', 'm/s', 'mdi:weather-windy', None, 'mph'],
    'wind_direction': ['Wind Direction', None, 'mdi:compass-outline', None, None],
    'precipitation': ['Rain today', 'mm', 'mdi:weather-rainy', None, 'in'],
    'precipitation_rate': ['Rain rate', 'mm/h', 'mdi:weather-pouring', None, 'in/h'],
    'humidity': ['Humidity', '%', 'mdi:water-percent', DEVICE_CLASS_HUMIDITY, None],
    'pressure': ['Pressure', 'hPa', 'mdi:gauge', DEVICE_CLASS_PRESSURE, 'inHg'],
    'uv': ['UV', UNIT_UV_INDEX,'mdi:weather-sunny', None, None],
    'solar_radiation': ['Solar Radiation', 'W/m2', 'mdi:solar-power', None, None],
    'illuminance': ['Illuminance', 'Lx', 'mdi:brightness-5', DEVICE_CLASS_ILLUMINANCE, None],
    'lightning_count': ['Lightning Count', None, 'mdi:flash', None, None],
    'airbattery': ['AIR Battery', 'V', 'mdi:battery', DEVICE_CLASS_BATTERY, None],
    'skybattery': ['SKY Battery', 'V', 'mdi:battery', DEVICE_CLASS_BATTERY, None]
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MONITORED_CONDITIONS, default=list(SENSOR_TYPES)):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_WIND_UNIT, default='ms'): cv.string,
    vol.Optional(CONF_NAME, default=DOMAIN): cv.string
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the SmartWeather sensor platform."""
    from pysmartweatherudp import SWReceiver

    unit_system = 'metric' if hass.config.units.is_metric else 'imperial'

    module = SWReceiver(DEFAULT_HOST, DEFAULT_PORT, unit_system)
    module.start()

    name = config.get(CONF_NAME)
    wind_unit = config.get(CONF_WIND_UNIT)

    sensors = []
    for variable in config[CONF_MONITORED_CONDITIONS]:
        sensors.append(SmartWeatherReceiver(hass, module, variable, name, unit_system, wind_unit))
        _LOGGER.debug("Sensor added: %s", variable)

    add_entities(sensors, True)

class SmartWeatherReceiver(Entity):

    def __init__(self, hass, module, sensor, name, unit_system, wind_unit):
        """Initialize the sensor."""
        self._sensor = sensor
        self._unit_system = unit_system
        self._wind_unit = wind_unit

        self._name = SENSOR_TYPES[self._sensor][0]
        self.entity_id = generate_entity_id(ENTITY_ID_FORMAT, '{} {}'.format(name, SENSOR_TYPES[self._sensor][0]), hass=hass)

        self._data = None
        self._state = None

        module.registerCallback(self._update_callback)

    def _update_callback(self, data):
        self._data = data

        _LOGGER.debug("Data received: %s %s %s %s", data.type, data.timestamp, data.precipitation, data.temperature)

        self.schedule_update_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        if hasattr(self._data, self._sensor):
            variable = getattr(self._data, self._sensor)
            if not (variable is None):
                if SENSOR_TYPES[self._sensor][1] == 'm/s':
                    return round(variable*3.6,1) \
                        if self._wind_unit == 'kmh' \
                        else variable
                else:
                    return variable
        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self._unit_system == 'imperial' and not (SENSOR_TYPES[self._sensor][4] is None):
            return SENSOR_TYPES[self._sensor][4]
        else:
            if SENSOR_TYPES[self._sensor][1] == 'm/s':
                return 'km/h' \
                    if self._wind_unit == 'kmh' \
                    else SENSOR_TYPES[self._sensor][1]
            else:
                return SENSOR_TYPES[self._sensor][1]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        if 'Battery' in self._name:
            if hasattr(self._data, self._sensor):
                voltage = float(getattr(self._data, self._sensor))
                if not (voltage is None):
                    if voltage < 2.3:
                        return 'mdi:battery-alert'
                    elif voltage < 2.4:
                        return 'mdi:battery-10'
                    elif voltage < 2.5:
                        return 'mdi:battery-20'
                    elif voltage < 2.6:
                        return 'mdi:battery-30'
                    elif voltage < 2.7:
                        return 'mdi:battery-40'
                    elif voltage < 2.8:
                        return 'mdi:battery-50'
                    elif voltage < 2.9:
                        return 'mdi:battery-60'
                    elif voltage < 3.0:
                        return 'mdi:battery-70'
                    elif voltage < 3.1:
                        return 'mdi:battery-80'
                    elif voltage < 3.2:
                        return 'mdi:battery-90'
                    else:
                        return 'mdi:battery'
            return 'mdi:battery'
        else:
            return SENSOR_TYPES[self._sensor][2]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._sensor][3]

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        #_LOGGER.debug(dir(self._data))
        attr = {}
        attr[ATTR_ATTRIBUTION] = ATTRIBUTION
        if hasattr(self._data, 'timestamp'):
            attr[ATTR_LAST_UPDATE] = datetime.datetime.fromtimestamp(self._data.timestamp).strftime('%Y-%m-%d %H:%M:%S')

        if self._name.lower() == "lightning count":
            distance_unit = 'mi' if self._unit_system == 'imperial' else 'km'
            if hasattr(self._data, 'lightning_time'):
                attr[ATTR_LIGHTNING_DETECTED] = self._data.lightning_time
            if hasattr(self._data, 'lightning_distance'):
                attr[ATTR_LIGHTNING_DISTANCE] = "{} {}".format(self._data.lightning_distance, distance_unit)

        return attr

    @property
    def should_poll(self) -> bool:
        """Entity should not be polled."""
        return False

    @property
    def force_update(self) -> bool:
        """SmartWeatherUDP should force updates. Repeated states have meaning."""
        return True
