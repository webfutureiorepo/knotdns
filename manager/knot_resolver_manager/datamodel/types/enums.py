from typing_extensions import Literal

# Policy actions
PolicyActionEnum = Literal[
    # Nonchain actions
    "pass",
    "deny",
    "drop",
    "refuse",
    "tc",
    "reroute",
    "answer",
    # Chain actions
    "mirror",
    "forward",
    "stub",
    "debug-always",
    "debug-cache-miss",
    "qtrace",
    "reqtrace",
]

# FLAGS from https://www.knot-resolver.cz/documentation/latest/lib.html?highlight=options#c.kr_qflags
PolicyFlagEnum = Literal[
    "no-minimize",
    "no-ipv4",
    "no-ipv6",
    "tcp",
    "resolved",
    "await-ipv4",
    "await-ipv6",
    "await-cut",
    "no-edns",
    "cached",
    "no-cache",
    "expiring",
    "allow_local",
    "dnssec-want",
    "dnssec-bogus",
    "dnssec-insecure",
    "dnssec-cd",
    "stub",
    "always-cut",
    "dnssec-wexpand",
    "permissive",
    "strict",
    "badcookie-again",
    "cname",
    "reorder-rr",
    "trace",
    "no-0x20",
    "dnssec-nods",
    "dnssec-optout",
    "nonauth",
    "forward",
    "dns64-mark",
    "cache-tried",
    "no-ns-found",
    "pkt-is-sane",
    "dns64-disable",
]

# DNS records from 'kres.type' table
DNSRecordTypeEnum = Literal[
    "A",
    "A6",
    "AAAA",
    "AFSDB",
    "ANY",
    "APL",
    "ATMA",
    "AVC",
    "AXFR",
    "CAA",
    "CDNSKEY",
    "CDS",
    "CERT",
    "CNAME",
    "CSYNC",
    "DHCID",
    "DLV",
    "DNAME",
    "DNSKEY",
    "DOA",
    "DS",
    "EID",
    "EUI48",
    "EUI64",
    "GID",
    "GPOS",
    "HINFO",
    "HIP",
    "HTTPS",
    "IPSECKEY",
    "ISDN",
    "IXFR",
    "KEY",
    "KX",
    "L32",
    "L64",
    "LOC",
    "LP",
    "MAILA",
    "MAILB",
    "MB",
    "MD",
    "MF",
    "MG",
    "MINFO",
    "MR",
    "MX",
    "NAPTR",
    "NID",
    "NIMLOC",
    "NINFO",
    "NS",
    "NSAP",
    "NSAP-PTR",
    "NSEC",
    "NSEC3",
    "NSEC3PARAM",
    "NULL",
    "NXT",
    "OPENPGPKEY",
    "OPT",
    "PTR",
    "PX",
    "RKEY",
    "RP",
    "RRSIG",
    "RT",
    "SIG",
    "SINK",
    "SMIMEA",
    "SOA",
    "SPF",
    "SRV",
    "SSHFP",
    "SVCB",
    "TA",
    "TALINK",
    "TKEY",
    "TLSA",
    "TSIG",
    "TXT",
    "UID",
    "UINFO",
    "UNSPEC",
    "URI",
    "WKS",
    "X25",
    "ZONEMD",
]
