"""Config flow for smartweatherudp."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from async_timeout import timeout
from pyweatherflowudp.client import EVENT_DEVICE_DISCOVERED, WeatherFlowListener
from pyweatherflowudp.const import DEFAULT_HOST
from pyweatherflowudp.errors import AddressInUseError, ListenerError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = STEP_MANUAL_DATA_SCHEMA = vol.Schema(
    {vol.Required(CONF_HOST): str}
)


async def _async_has_devices(host: str = DEFAULT_HOST) -> bool:
    """Return if there are devices that can be discovered."""
    event = asyncio.Event()

    @callback
    def device_discovered():
        """Handle a discovered device."""
        event.set()

    async with WeatherFlowListener(host) as client:
        client.on(EVENT_DEVICE_DISCOVERED, lambda _: device_discovered())
        try:
            async with timeout(10):
                await event.wait()
        except asyncio.TimeoutError:
            return False

    return True


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for smartweatherudp."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        current_hosts = [
            entry.data.get(CONF_HOST) for entry in self._async_current_entries()
        ]

        if user_input is None:
            if DEFAULT_HOST in current_hosts:
                return self.async_show_form(
                    step_id="user", data_schema=STEP_USER_DATA_SCHEMA
                )
            host = DEFAULT_HOST
        else:
            host = user_input.get(CONF_HOST)

        if host in current_hosts:
            return self.async_abort(reason="single_instance_allowed")

        # Get current discovered entries.
        in_progress = self._async_in_progress()

        if not (has_devices := in_progress):
            errors = {}
            try:
                has_devices = await self.hass.async_add_job(_async_has_devices, host)
            except AddressInUseError:
                errors["base"] = "address_in_use"
            except ListenerError:
                errors["base"] = "cannot_connect"

            if errors or user_input is None:
                return self.async_show_form(
                    step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
                )

        if not has_devices:
            return self.async_abort(reason="no_devices_found")

        # Cancel other flows.
        for flow in in_progress:
            self.hass.config_entries.flow.async_abort(flow["flow_id"])

        return self.async_create_entry(
            title=f"WeatherFlow{f' ({host})' if host != DEFAULT_HOST else ''}",
            data=user_input,
        )

    async def async_step_import(self, config: dict[str, Any] | None) -> FlowResult:
        """Handle a flow initialized by import."""
        if config is None or (host := config.get(CONF_HOST)) in [
            entry.data.get(CONF_HOST) for entry in self._async_current_entries()
        ]:
            return self.async_abort(reason="single_instance_allowed")

        # Cancel other flows.
        in_progress = self._async_in_progress()
        for flow in in_progress:
            self.hass.config_entries.flow.async_abort(flow["flow_id"])

        return self.async_create_entry(
            title=f"{config.get(CONF_NAME, 'WeatherFlow')}{f' ({host})' if host != DEFAULT_HOST else ''}",
            data=config,
        )
