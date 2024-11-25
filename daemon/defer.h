/*  Copyright (C) CZ.NIC, z.s.p.o. <knot-resolver@labs.nic.cz>
 *  SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <stdbool.h>
#include "lib/defines.h"
#include "lib/utils.h"
#include "lib/kru.h"

/// Initialize defer, incl. shared memory with KRU, excl. idle.
KR_EXPORT
int defer_init(const char *mmap_file, int cpus);

/// Initialize idle.
int defer_init_idle(uv_loop_t *loop);

/// Deinitialize shared memory.
void defer_deinit(void);

/// Increment KRU counters by the given time.
void defer_charge(uint64_t nsec, union kr_sockaddr *addr, bool stream);

typedef struct {
	bool is_accounting; /// whether currently accounting the time to someone
	union kr_sockaddr addr; /// request source (to which we account) or AF_UNSPEC if unknown yet
	bool stream;
	uint64_t stamp; /// monotonic nanoseconds, probably won't wrap
} defer_sample_state_t;
extern defer_sample_state_t defer_sample_state;

extern struct defer *defer;  /// skip sampling/deferring if NULL
extern bool defer_initialized; /// defer_init was called, possibly keeping defer disabled


// TODO: reconsider `static inline` cases below

#include <time.h>
static inline uint64_t defer_get_stamp(void)
{
	struct timespec now_ts = {0};
	clock_gettime(CLOCK_THREAD_CPUTIME_ID, &now_ts);
	return now_ts.tv_nsec + 1000*1000*1000 * (uint64_t)now_ts.tv_sec;
}

/// Annotate the work currently being accounted by an IP address.
static inline void defer_sample_addr(const union kr_sockaddr *addr, bool stream)
{
	if (!defer || kr_fails_assert(addr)) return;
	if (!defer_sample_state.is_accounting) return;

	if (defer_sample_state.addr.ip.sa_family != AF_UNSPEC) {
		// TODO: this costs performance, so only in some debug mode?
		kr_assert(kr_sockaddr_cmp(&addr->ip, &defer_sample_state.addr.ip) == kr_ok());
		return;
	}

	switch (addr->ip.sa_family) {
	case AF_INET:
		defer_sample_state.addr.ip4 = addr->ip4;
		break;
	case AF_INET6:
		defer_sample_state.addr.ip6 = addr->ip6;
		break;
	default:
		defer_sample_state.addr.ip.sa_family = AF_UNSPEC;
		break;
	}
	defer_sample_state.stream = stream;
}

/// Internal; start accounting work at specified timestamp.
static inline void defer_sample_start_stamp(uint64_t stamp)
{
	if (!defer) return;
	kr_assert(!defer_sample_state.is_accounting);
	defer_sample_state.is_accounting = true;
	defer_sample_state.stamp = stamp;
	defer_sample_state.addr.ip.sa_family = AF_UNSPEC;
}

/// Internal; stop accounting work at specified timestamp and charge the source if applicable.
static inline void defer_sample_stop_stamp(uint64_t stamp)
{
	if (!defer) return;
	kr_assert(defer_sample_state.is_accounting);
	defer_sample_state.is_accounting = false;

	if (defer_sample_state.addr.ip.sa_family == AF_UNSPEC) return;

	const uint64_t elapsed = stamp - defer_sample_state.stamp;
	if (elapsed == 0) return;

	// TODO: some queries of internal origin have suspicioiusly high numbers.
	// We won't be really accounting those, but it might suggest some other issue.

	defer_charge(elapsed, &defer_sample_state.addr, defer_sample_state.stream);
}

/// Start accounting work; optionally save state of current accounting.
/// Current state can be saved only after having an address assigned.
static inline void defer_sample_start(defer_sample_state_t *prev_state_out) {
	if (!defer) return;
	uint64_t stamp = defer_get_stamp();

	// suspend
	if (prev_state_out) {
		*prev_state_out = defer_sample_state;  // TODO stamp is not needed
		if (defer_sample_state.is_accounting)
			defer_sample_stop_stamp(stamp);
	}

	// start
	defer_sample_start_stamp(stamp);
}

/// Stop accounting and start it again.
static inline void defer_sample_restart(void) {
	if (!defer) return;
	uint64_t stamp = defer_get_stamp();

	// stop
	defer_sample_stop_stamp(stamp);

	// start
	defer_sample_start_stamp(stamp);
}

/// Stop accounting and charge the source if applicable; optionally resume previous accounting.
static inline void defer_sample_stop(defer_sample_state_t *prev_state, bool reuse_last_stamp) {
	if (!defer) return;
	uint64_t stamp = reuse_last_stamp ? defer_sample_state.stamp : defer_get_stamp();

	// stop
	defer_sample_stop_stamp(stamp);

	// resume
	if (prev_state) {
		defer_sample_state = *prev_state;
		defer_sample_state.stamp = stamp;
	}
}
