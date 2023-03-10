from typing import List, Optional

from knot_resolver_manager.datamodel.types import Dir, DomainName, File, SizeUnit, TimeUnit
from knot_resolver_manager.utils.modeling import ConfigSchema


class PrefillSchema(ConfigSchema):
    """
    Prefill the cache periodically by importing zone data obtained over HTTP.

    ---
    origin: Origin for the imported data. Cache prefilling is only supported for the root zone ('.').
    url: URL of the zone data to be imported.
    refresh_interval: Time interval between consecutive refreshes of the imported zone data.
    ca_file: Path to the file containing a CA certificate bundle that is used to authenticate the HTTPS connection.
    """

    origin: DomainName
    url: str
    refresh_interval: TimeUnit = TimeUnit("1d")
    ca_file: Optional[File] = None

    def _validate(self) -> None:
        if str(self.origin) != ".":
            raise ValueError("cache prefilling is not yet supported for non-root zones")


class CacheSchema(ConfigSchema):
    """
    DNS resolver cache configuration.

    ---
    garbage_collector: Automatically use garbage collector to periodically clear cache.
    storage: Cache storage of the DNS resolver.
    size_max: Maximum size of the cache.
    ttl_min: Minimum time-to-live for the cache entries.
    ttl_max: Maximum time-to-live for the cache entries.
    ns_timeout: Time interval for which a nameserver address will be ignored after determining that it does not return (useful) answers.
    prefill: Prefill the cache periodically by importing zone data obtained over HTTP.
    """

    garbage_collector: bool = True
    storage: Dir = Dir("/var/cache/knot-resolver")
    size_max: SizeUnit = SizeUnit("100M")
    ttl_min: TimeUnit = TimeUnit("5s")
    ttl_max: TimeUnit = TimeUnit("6d")
    ns_timeout: TimeUnit = TimeUnit("1000ms")
    prefill: Optional[List[PrefillSchema]] = None

    def _validate(self):
        if self.ttl_min.seconds() >= self.ttl_max.seconds():
            raise ValueError("'ttl-max' must be larger then 'ttl-min'")
