import logging
from typing import Iterable, List

from knot_resolver_manager import compat
from knot_resolver_manager.kresd_controller.base import BaseKresdController

from . import dbus_api as systemd

logger = logging.getLogger(__name__)


class SystemdKresdController(BaseKresdController):
    async def is_running(self) -> bool:
        raise NotImplementedError()

    async def start(self):
        await compat.asyncio.to_thread(systemd.start_unit, f"kresd@{self.id}.service")

    async def stop(self):
        await compat.asyncio.to_thread(systemd.stop_unit, f"kresd@{self.id}.service")

    async def restart(self):
        await compat.asyncio.to_thread(systemd.restart_unit, f"kresd@{self.id}.service")

    @staticmethod
    async def is_controller_available() -> bool:
        try:
            _ = await compat.asyncio.to_thread(systemd.list_units)
            return True
        except BaseException:  # we want every possible exception to be caught
            logger.warning("systemd DBus API backend failed to initialize", exc_info=True)
            return False

    @staticmethod
    async def get_all_running_instances() -> Iterable["BaseKresdController"]:
        res: List[SystemdKresdController] = []
        units = await compat.asyncio.to_thread(systemd.list_units)
        for unit in units:
            u: str = unit
            if u.startswith("kresd@") and u.endswith(".service"):
                iden = u.replace("kresd@", "").replace(".service", "")
                res.append(SystemdKresdController(kresd_id=iden))
        return res