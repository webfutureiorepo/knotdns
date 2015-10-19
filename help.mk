info:
	$(info )
	$(info Target:     Knot DNS Resolver $(MAJOR).$(MINOR).$(PATCH)-$(PLATFORM))
	$(info Compiler:   $(CC) $(BUILD_CFLAGS))
	$(info Linker:     $(LD) $(BUILD_LDFLAGS))
	$(info PREFIX:     $(PREFIX))
	$(info BINDIR:     $(BINDIR))
	$(info LIBDIR:     $(LIBDIR))
	$(info INCLUDEDIR: $(INCLUDEDIR))
	$(info MODULEDIR:  $(MODULEDIR))
	$(info )
	$(info Dependencies)
	$(info ------------)
	$(info [$(HAS_libknot)] libknot (lib))
	$(info [$(HAS_lua)] LuaJIT (daemon))
	$(info [$(HAS_libuv)] libuv (daemon))
	$(info )
	$(info Optional)
	$(info --------)
	$(info [$(HAS_doxygen)] doxygen (doc))
	$(info [$(HAS_go)] Go (modules/go))
	$(info [$(HAS_libmemcached)] libmemcached (modules/memcached))
	$(info [$(HAS_hiredis)] hiredis (modules/redis))
	$(info [$(HAS_cmocka)] cmocka (tests/unit))
	$(info [$(HAS_python)] Python (tests/integration))
	$(info [$(HAS_socket_wrapper)] socket_wrapper (lib))
	$(info )
