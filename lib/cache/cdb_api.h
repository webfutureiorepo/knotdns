/*  Copyright (C) CZ.NIC, z.s.p.o. <knot-resolver@labs.nic.cz>
 *  SPDX-License-Identifier: GPL-3.0-or-later
*/

#pragma once

#include <stdbool.h>
#include <stdint.h>

#include <libknot/db/db.h>

/* Cache options. */
struct kr_cdb_opts {
	const char *path; /*!< Cache URI path. */
	size_t maxsize;   /*!< Suggested cache size in bytes; pass 0 to keep unchanged/default. */
	bool is_cache;    /*!< Some behavior changes based on use case.  TODO: details. */
};

struct kr_cdb_stats {
	uint64_t open;
	uint64_t close;
	uint64_t count;
	uint64_t count_entries;
	uint64_t clear;
	uint64_t commit;
	uint64_t read;
	uint64_t read_miss;
	uint64_t write;
	uint64_t remove;
	uint64_t remove_miss;
	uint64_t match;
	uint64_t match_miss;
	uint64_t read_leq;
	uint64_t read_leq_miss;
	uint64_t read_less;
	double usage_percent;
};

/*! Pointer to a cache structure.
 *
 * This struct is opaque and never defined; the purpose is to get better
 * type safety than with void *.
 */
typedef struct kr_cdb *kr_cdb_pt;

/*! Cache database API.
  * This is a simplified version of generic DB API from libknot,
  * that is tailored to caching purposes.
  */
struct kr_cdb_api {
	const char *name;

	/* Context operations */

	int (*open)(kr_cdb_pt *db, struct kr_cdb_stats *stat, struct kr_cdb_opts *opts, knot_mm_t *mm);
	void (*close)(kr_cdb_pt db, struct kr_cdb_stats *stat);
	int (*count)(kr_cdb_pt db, struct kr_cdb_stats *stat);
	int (*clear)(kr_cdb_pt db, struct kr_cdb_stats *stat);

	/** Run after a row of operations to release transaction/lock if needed.
	 * \param accept_rw whether the RW transaction should accept changes (commit vs. abort)
	 * \param reset_ro whether the RO transaction should be ended (newest data next time)
	 * \return error code - accepting RW transactions can fail with LMDB.
	 */
	int (*commit)(kr_cdb_pt db, struct kr_cdb_stats *stat, bool accept_rw, bool reset_ro);

	/* Data access */

	int (*read)(kr_cdb_pt db, struct kr_cdb_stats *stat,
			const knot_db_val_t *key, knot_db_val_t *val, int maxcount);
	int (*write)(kr_cdb_pt db, struct kr_cdb_stats *stat, const knot_db_val_t *key,
			knot_db_val_t *val, int maxcount);

	/** Remove maxcount keys.
	 * \returns the number of successfully removed keys or the first error code
	 * It returns on first error, but ENOENT is not considered an error. */
	int (*remove)(kr_cdb_pt db, struct kr_cdb_stats *stat,
			knot_db_val_t keys[], int maxcount);

	/* Specialised operations */

	/** Find key-value pairs that are prefixed by the given key, limited by maxcount.
	 * \return the number of pairs or negative error. */
	int (*match)(kr_cdb_pt db, struct kr_cdb_stats *stat,
			knot_db_val_t *key, knot_db_val_t keyval[][2], int maxcount);

	/** Less-or-equal search (lexicographic ordering).
	 * On successful return, key->data and val->data point to DB-owned data.
	 * return: 0 for equality, > 0 for less, < 0 kr_error */
	int (*read_leq)(kr_cdb_pt db, struct kr_cdb_stats *stat,
			knot_db_val_t *key, knot_db_val_t *val);

	/** Less-than search (lexicographic ordering).
	 * On successful return, key->data and val->data point to DB-owned data.
	 * return: > 0 for less, < 0 kr_error */
	int (*read_less)(kr_cdb_pt db, struct kr_cdb_stats *stat,
			knot_db_val_t *key, knot_db_val_t *val);

	/** Return estimated space usage (0--100). */
	double (*usage_percent)(kr_cdb_pt db);

	/** Return the current cache size limit in bytes; could be cached by check_health(). */
	size_t (*get_maxsize)(kr_cdb_pt db);

	/** Perform maintenance.
	 * In LMDB case it checks whether data.mdb is still the same
	 * and reopens it if it isn't; it errors out if the file doesn't exist anymore.
	 * \return 0 if OK, 1 if reopened OK, < 0 kr_error */
	int (*check_health)(kr_cdb_pt db, struct kr_cdb_stats *stat);


	/** Start iterating; return the first *val with *key.
	 *
	 * This only makes sense if !is_cache.
	 * TODO: it only works inside RO transactions for now.
	 */
	int (*it_first)(kr_cdb_pt db, struct kr_cdb_stats *stat,
			const knot_db_val_t *key, knot_db_val_t *val);
	/** Advance to the next *val with the same key. */
	int (*it_next)(kr_cdb_pt db, struct kr_cdb_stats *stat, knot_db_val_t *val);
};
