"""Sensors for the smartweatherudp integration."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import Any

from pyweatherflowudp.calc import Quantity
from pyweatherflowudp.const import EVENT_RAPID_WIND, UNIT_MINUTES
from pyweatherflowudp.device import (
    EVENT_OBSERVATION,
    EVENT_STATUS_UPDATE,
    WeatherFlowDevice,
)
import voluptuous as vol

from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    PLATFORM_SCHEMA,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
    CONF_NAME,
    DEGREE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_TIMESTAMP,
    DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS,
    DEVICE_CLASS_VOLTAGE,
    ELECTRIC_POTENTIAL_VOLT,
    ENTITY_CATEGORY_DIAGNOSTIC,
    IRRADIATION_WATTS_PER_SQUARE_METER,
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    LENGTH_MILLIMETERS,
    LIGHT_LUX,
    PERCENTAGE,
    PRECIPITATION_INCHES,
    PRECIPITATION_INCHES_PER_HOUR,
    PRECIPITATION_MILLIMETERS_PER_HOUR,
    PRESSURE_INHG,
    PRESSURE_MBAR,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_MILES_PER_HOUR,
    TEMP_CELSIUS,
    UV_INDEX,
)
from homeassistant.core import Callable, HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, StateType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONCENTRATION_KILOGRAMS_PER_CUBIC_METER = "kg/m³"
CONCENTRATION_POUNDS_PER_CUBIC_FOOT = "lbs/ft³"

QUANTITY_KILOMETERS_PER_HOUR = "kph"
QUANTITY_MILLIMETERS_PER_HOUR = "mm/hr"
QUANTITY_INCHES_PER_HOUR = "in/hr"

IMPERIAL_UNIT_MAP = {
    CONCENTRATION_KILOGRAMS_PER_CUBIC_METER: CONCENTRATION_POUNDS_PER_CUBIC_FOOT,
    LENGTH_KILOMETERS: LENGTH_MILES,
    LENGTH_MILLIMETERS: PRECIPITATION_INCHES,
    PRECIPITATION_MILLIMETERS_PER_HOUR: PRECIPITATION_INCHES_PER_HOUR,
    PRESSURE_MBAR: PRESSURE_INHG,
    SPEED_KILOMETERS_PER_HOUR: SPEED_MILES_PER_HOUR,
}

# Deprecated configuration.yaml
DEPRECATED_CONF_WIND_UNIT = "wind_unit"
DEPRECATED_SENSOR_TYPES = [
    "temperature",
    "dewpoint",
    "feels_like",
    "heat_index",
    "wind_chill",
    "wind_speed",
    "wind_bearing",
    "wind_speed_rapid",
    "wind_bearing_rapid",
    "wind_gust",
    "wind_lull",
    "wind_direction",
    "precipitation",
    "precipitation_rate",
    "humidity",
    "pressure",
    "uv",
    "solar_radiation",
    "illuminance",
    "lightning_count",
    "airbattery",
    "skybattery",
]


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(
            CONF_MONITORED_CONDITIONS, default=DEPRECATED_SENSOR_TYPES
        ): vol.All(cv.ensure_list, [vol.In(DEPRECATED_SENSOR_TYPES)]),
        vol.Optional(DEPRECATED_CONF_WIND_UNIT, default="ms"): cv.string,
        vol.Optional(CONF_HOST, default="0.0.0.0"): cv.string,
        vol.Optional(CONF_NAME, default=DOMAIN): cv.string,
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: dict[str, Any] | None = None,
) -> None:
    """Import smartweatherudp configuration from YAML."""
    _LOGGER.warning(
        "Configuration of the smartweatherudp platform in YAML is deprecated and will be "
        "removed in a future version; Your existing configuration has been imported into "
        "the UI automatically and can safely be removed from your configuration.yaml file"
    )
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_IMPORT},
            data=config,
        )
    )


@dataclass
class WeatherFlowSensorEntityDescription(SensorEntityDescription):
    """Describes a WeatherFlow sensor entity description."""

    attr: str | None = None
    conversion_fn: Callable[[Quantity], datetime | StateType] | None = None
    decimals: int | None = None
    event_subscriptions: list[str] = field(default_factory=lambda: [EVENT_OBSERVATION])
    value_fn: Callable[[Quantity], datetime | StateType] | None = None


@dataclass
class WeatherFlowTemperatureSensorEntityDescription(WeatherFlowSensorEntityDescription):
    """Describes a WeatherFlow temperature sensor entity description."""

    def __post_init__(self) -> None:
        """Post initialisation processing."""
        self.native_unit_of_measurement = TEMP_CELSIUS
        self.device_class = DEVICE_CLASS_TEMPERATURE
        self.state_class = STATE_CLASS_MEASUREMENT
        self.decimals = 1
        super().__post_init__()


@dataclass
class WeatherFlowWindSensorEntityDescription(WeatherFlowSensorEntityDescription):
    """Describes a WeatherFlow wind sensor entity description."""

    def __post_init__(self) -> None:
        """Post initialisation processing."""
        self.icon = "mdi:weather-windy"
        self.native_unit_of_measurement = SPEED_KILOMETERS_PER_HOUR
        self.state_class = STATE_CLASS_MEASUREMENT
        self.conversion_fn = lambda attr: attr.to(SPEED_MILES_PER_HOUR)
        self.decimals = 2
        self.value_fn = lambda attr: attr.to(QUANTITY_KILOMETERS_PER_HOUR)
        super().__post_init__()


SENSORS: tuple[WeatherFlowSensorEntityDescription, ...] = (
    WeatherFlowTemperatureSensorEntityDescription(
        key="air_temperature",
        name="Temperature",
    ),
    WeatherFlowSensorEntityDescription(
        key="air_density",
        name="Air Density",
        native_unit_of_measurement=CONCENTRATION_KILOGRAMS_PER_CUBIC_METER,
        device_class=DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS,
        state_class=STATE_CLASS_MEASUREMENT,
        conversion_fn=lambda attr: attr.to(CONCENTRATION_POUNDS_PER_CUBIC_FOOT),
        decimals=5,
    ),
    WeatherFlowTemperatureSensorEntityDescription(
        key="dew_point_temperature",
        name="Dew Point",
    ),
    WeatherFlowSensorEntityDescription(
        key="battery",
        name="Battery Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    WeatherFlowTemperatureSensorEntityDescription(
        key="feels_like_temperature",
        name="Feels Like",
    ),
    WeatherFlowSensorEntityDescription(
        key="illuminance",
        name="Illuminance",
        native_unit_of_measurement=LIGHT_LUX,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="lightning_strike_average_distance",
        name="Lightning Average Distance",
        icon="mdi:lightning-bolt",
        native_unit_of_measurement=LENGTH_KILOMETERS,
        conversion_fn=lambda attr: attr.to(LENGTH_MILES),
        decimals=2,
    ),
    WeatherFlowSensorEntityDescription(
        key="lightning_strike_count",
        name="Lightning Count",
        icon="mdi:lightning-bolt",
    ),
    WeatherFlowSensorEntityDescription(
        key="rain_amount",
        name="Rain Amount",
        icon="mdi:weather-rainy",
        native_unit_of_measurement=LENGTH_MILLIMETERS,
        state_class=STATE_CLASS_TOTAL,
        attr="rain_amount_previous_minute",
        conversion_fn=lambda attr: (attr * UNIT_MINUTES).to(PRECIPITATION_INCHES),
        decimals=2,
        value_fn=lambda attr: (attr * UNIT_MINUTES).to(LENGTH_MILLIMETERS),
    ),
    WeatherFlowSensorEntityDescription(
        key="rain_rate",
        name="Rain Rate",
        icon="mdi:weather-rainy",
        native_unit_of_measurement=PRECIPITATION_MILLIMETERS_PER_HOUR,
        attr="rain_amount_previous_minute",
        conversion_fn=lambda attr: attr.to(QUANTITY_INCHES_PER_HOUR),
        decimals=2,
        value_fn=lambda attr: attr.to(QUANTITY_MILLIMETERS_PER_HOUR),
    ),
    WeatherFlowSensorEntityDescription(
        key="relative_humidity",
        name="Humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_HUMIDITY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="rssi",
        name="RSSI",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_registry_enabled_default=False,
        event_subscriptions=[EVENT_STATUS_UPDATE],
    ),
    WeatherFlowSensorEntityDescription(
        key="station_pressure",
        name="Station Pressure",
        native_unit_of_measurement=PRESSURE_MBAR,
        device_class=DEVICE_CLASS_PRESSURE,
        state_class=STATE_CLASS_MEASUREMENT,
        conversion_fn=lambda attr: attr.to(PRESSURE_INHG),
        decimals=5,
    ),
    WeatherFlowSensorEntityDescription(
        key="solar_radiation",
        name="Solar Radiation",
        native_unit_of_measurement=IRRADIATION_WATTS_PER_SQUARE_METER,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="up_since",
        name="Up Since",
        device_class=DEVICE_CLASS_TIMESTAMP,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        entity_registry_enabled_default=False,
        event_subscriptions=[EVENT_STATUS_UPDATE],
    ),
    WeatherFlowSensorEntityDescription(
        key="uv",
        name="UV",
        native_unit_of_measurement=UV_INDEX,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    WeatherFlowSensorEntityDescription(
        key="vapor_pressure",
        name="Vapor Pressure",
        native_unit_of_measurement=PRESSURE_MBAR,
        device_class=DEVICE_CLASS_PRESSURE,
        state_class=STATE_CLASS_MEASUREMENT,
        conversion_fn=lambda attr: attr.to(PRESSURE_INHG),
        decimals=5,
    ),
    WeatherFlowTemperatureSensorEntityDescription(
        key="wet_bulb_temperature",
        name="Wet Bulb Temperature",
    ),
    WeatherFlowWindSensorEntityDescription(
        key="wind_average",
        name="Wind Average",
    ),
    WeatherFlowSensorEntityDescription(
        key="wind_direction",
        name="Wind Direction",
        icon="mdi:compass-outline",
        native_unit_of_measurement=DEGREE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    WeatherFlowWindSensorEntityDescription(
        key="wind_gust",
        name="Wind Gust",
    ),
    WeatherFlowWindSensorEntityDescription(
        key="wind_lull",
        name="Wind Lull",
    ),
    WeatherFlowWindSensorEntityDescription(
        key="wind_speed",
        name="Wind Speed",
        event_subscriptions=[EVENT_RAPID_WIND, EVENT_OBSERVATION],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up WeatherFlow sensors using config entry."""

    @callback
    def async_add_sensor(device: WeatherFlowDevice) -> None:
        """Add WeatherFlow sensor."""
        async_add_entities(
            WeatherFlowSensorEntity(device, description, hass.config.units.is_metric)
            for description in SENSORS
            if getattr(
                device,
                description.key if description.attr is None else description.attr,
                None,
            )
            is not None
        )

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            f"{DOMAIN}_{config_entry.entry_id}_add_{SENSOR_DOMAIN}",
            async_add_sensor,
        )
    )


class WeatherFlowEntity(SensorEntity):
    """WeatherFlow entity base class."""

    def __init__(self, device: WeatherFlowDevice) -> None:
        """Initialize a WeatherFlow entity."""
        self.device = device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.device.serial_number)},
            manufacturer="WeatherFlow",
            model=self.device.model,
            name=f"{self.device.model} {self.device.serial_number}",
            sw_version=self.device.firmware_revision,
            suggested_area="Backyard",
        )


class WeatherFlowSensorEntity(WeatherFlowEntity):
    """Defines a WeatherFlow sensor entity."""

    entity_description: WeatherFlowSensorEntityDescription

    def __init__(
        self,
        device: WeatherFlowDevice,
        description: WeatherFlowSensorEntityDescription,
        is_metric: bool = True,
    ) -> None:
        """Initialize a WeatherFlow sensor entity."""
        super().__init__(device=device)
        if not is_metric and (
            (unit := IMPERIAL_UNIT_MAP.get(description.native_unit_of_measurement))
            is not None
        ):
            description.native_unit_of_measurement = unit
        self.entity_description = description
        self._attr_name = (
            f"{self.device.model} {self.device.serial_number} {description.name}"
        )
        self._attr_unique_id = f"{DOMAIN}_{self.device.serial_number}_{description.key}"
        self._attr_should_poll = False
        self.unsubscribes = []

    @property
    def last_reset(self) -> datetime | None:
        """Return the time when the sensor was last reset, if any."""
        if self.entity_description.state_class == STATE_CLASS_TOTAL:
            return self.device.last_report
        return None

    @property
    def native_value(self) -> datetime | StateType:
        """Return the state of the sensor."""
        attr = getattr(
            self.device,
            self.entity_description.key
            if self.entity_description.attr is None
            else self.entity_description.attr,
        )

        if (
            not self.hass.config.units.is_metric
            and (fn := self.entity_description.conversion_fn) is not None
        ) or (fn := self.entity_description.value_fn) is not None:
            attr = fn(attr)

        value = attr.m if isinstance(attr, Quantity) else attr
        if (decimals := self.entity_description.decimals) is not None:
            value = round(value, decimals)
        return value

    async def async_added_to_hass(self) -> None:
        """Subscribe to events."""
        self.unsubscribes = [
            self.device.on(event, lambda _: self.schedule_update_ha_state())
            for event in self.entity_description.event_subscriptions
        ]

    async def async_will_remove_from_hass(self) -> None:
        """Unsubscribe from events."""
        for unsub in self.unsubscribes:
            unsub()
